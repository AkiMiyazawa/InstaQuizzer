import asyncio
import json
import time
import asyncio

from enum import Enum
from collections import namedtuple
from multiprocessing import Process
import datetime
from User import User
from QuestionStats import QuestionStats


HOST_NAME = '172.30.44.243'
SERVER_PORT = 1500

class MyClicker_Protocol(asyncio.Protocol):
    def __init__(self, server):
        self.server = server
    # Implementation of asyncio.Protocol class
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self._transport = transport

    def data_received(self, data):
        answer_json = data.decode()
        print('Data received: {!r}'.format(answer_json))
        parse_future = asyncio.ensure_future(self.server.parse_input(answer_json, self._transport))

class server():
    def __init__(self, pipe_from_parent):
        # Setup for class
        self._user_dict = {}
        self._transport_dict = {}
        self._log_file = "myclicker_server.log"
        self._accepting_answers = False
        self._curr_correct_answer = ""
        self._curr_question_number = -1
        self._curr_total_answers = 0
        self._curr_correct_answers = 0
        self._question_stats_dict = {}
        self._pipe = pipe_from_parent
        print("Server starting!")
        # Asyncio stuff to run server
        self._loop = asyncio.get_event_loop()
        server_coro = self._loop.create_server(lambda: MyClicker_Protocol(self), HOST_NAME, str(SERVER_PORT))
        self._loop.create_task(self.check_pipe())
        self._server = self._loop.run_until_complete(server_coro)
        print("MyClicker server running on port " + str(SERVER_PORT))
        self._loop.run_forever()

    async def parse_input(self, answer_json, curr_transport):
        if not self._accepting_answers:
            return
        try:
            curr_answer_obj= json.loads(answer_json)
        except json.JSONDecodeError:
            self._log_io("JSONDecodeError!!")
            return
        json_keys = list(curr_answer_obj.keys())
        if len(json_keys) != 2 or "user_id" not in json_keys or "answer" not in json_keys:
            self._log_io("Invalid JSON answer!")
            return
        await self._log_io('Received answer: "' + answer_json + '"')
        curr_peername = curr_transport.get_extra_info('peername')
        self._transport_dict[curr_peername] = curr_transport
        user_id = curr_answer_obj["user_id"]
        answer = curr_answer_obj["answer"]
        await self.handle_answer(user_id, answer)

    async def handle_answer(self, user_id, answer):
        # Handle storage of answer stats for user
        curr_user = self._user_dict.get(user_id)
        if curr_user is None:
            curr_user = User()
            self._user_dict[user_id] = curr_user
        # Get the users current answer to this question
        old_answer = curr_user.answers.get(self._curr_question_number)
        # If the answer is the same we don't have to change anything
        if old_answer == answer:
            return
        curr_user.answers[self._curr_question_number] = answer
        if answer == self._curr_correct_answer:
            curr_user.num_correct += 1
        if old_answer == self._curr_correct_answer:
            curr_user.num_correct -= 1

        # Handle storage of answer stats for class
        curr_question_stats = self._question_stats_dict.get(self._curr_question_number)
        if curr_question_stats is None:
            print("Resetting question stats")
            curr_question_stats = QuestionStats()

        # We always add 1 to the current answer dict
        curr_question_stats.answer_dict[answer] += 1
        # If the user did not have an answer before, note another student has answered
        if old_answer is None:
            curr_question_stats.num_answers += 1
        else:
            curr_question_stats.answer_dict[old_answer] -= 1
        # If we say the right answer, note that
        if answer == self._curr_correct_answer:
            curr_question_stats.num_correct += 1
        # If we change to a wrong answer, note that
        elif old_answer == self._curr_correct_answer:
            curr_question_stats.num_correct -= 1
        self._question_stats_dict[self._curr_question_number] = curr_question_stats

    async def check_pipe(self):
        while True:
            if self._pipe.poll():
                request = self._pipe.recv()
                print("Server received request: " + str(request))
                if request == "question_data":
                    question_stats = self._question_stats_dict.get(self._curr_question_number)
                    if question_stats is None:
                        question_stats = "NO_DATA"
                    self._pipe.send(question_stats)
                elif request == "end_server":
                    with open("user_data.json", 'a') as user_file:
                        curr_date = str(datetime.date.today())
                        for (user_id, user) in self._user_dict.items():
                            user_file.write(curr_date + " " + str(user_id) + ": Percent Correct: " + str(user.get_percent()) + " Answers: " + str(user.answers))
                    self._pipe.send("DATA_WRITTEN")
                # The above requests are the only string-type requests - all other requests are dictionary
                # requests, and thus if the request is not a dictionary, it is invalid so we ignore it
                elif type(request) != type({1 : 2}):
                    pass
                elif list(request.keys()) == ['user_data']:
                    user_id = request['user_data']
                    user_data = self._user_dict.get(user_id)
                    if user_data is None:
                        user_data = "NO_DATA"
                    self._pipe.send(user_data)
                elif list(request.keys()) == ['update_accepting_answers']:
                    self._accepting_answers = request['update_accepting_answers']
                    # If we just started accepting answers, so we want to replace the 
                    # QuestionStats for this answer if it existed
                    if self._accepting_answers:
                        try:
                            del self._question_stats_dict[self._curr_question_number]
                        except KeyError:
                            pass
                elif list(request.keys()) == ['update_question_number', 'update_correct_answer']:
                    self._curr_question_number = request['update_question_number']
                    self._curr_correct_answer = request['update_correct_answer']

            await asyncio.sleep(0.1)

    async def _log_io(self, msg):
        print("MyClicker Server: " + msg)
        with open(self._log_file, 'a') as lf:
            lf.write(str(time.time()) + ": " + msg + '\n')
