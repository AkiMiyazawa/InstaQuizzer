import tkinter as tk
import pygubu
import random
import multiprocessing
import queue
import MyClickerServer
import QuestionStats

class Presentation:
    def __init__(self, presentation_dict):
        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('Desktop.ui')
        
        #3: Create the toplevel widget.
        self.mainwindow = builder.get_object('presentation_toplevel')

        #4: Connect callbacks
        builder.connect_callbacks(self)

        #5: Get variables
        self.question_text = self.builder.get_variable("question_text_presentation")
        self.accept_answers_text = self.builder.get_variable("accept_answers_text")
        self.show_data_text = self.builder.get_variable("show_data_text")

        #6: Initialize state variables of the class
        self.showing_data = False
        self.presentation_dict = presentation_dict
        self.question_number = 1
        first_question = self.presentation_dict[self.question_number]
        # The current correct letter will be set when calling format_question_text
        self.curr_correct_letter = ""
        first_q_text = self.format_question_text(first_question, self.question_number)
        self.question_text.set(first_q_text)
        self.accepting_answers = False

        #7: Start server running to accept answers
        self.parent_pipe, child_pipe = multiprocessing.Pipe()
        self.server_process = multiprocessing.Process(target=MyClickerServer.server, args=(child_pipe,))
        self.server_process.start()
        #This ensures the server knows the right answer
        self.parent_pipe.send({'update_question_number' : self.question_number, 'update_correct_answer' : self.curr_correct_letter})

        #7: Capture delete window event so we can write the user data to a file at the
        #   end of a presentation
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.on_close_window)
        
    def on_close_window(self, event=None):
        try:
            self.parent_pipe.send("end_server")
            self.parent_pipe.recv()
            self.server_process.terminate()
        except BrokenPipeError:
            pass
        # Call destroy on toplevel to finish program
        self.mainwindow.destroy()

    def quit(self, event=None):
        self.mainwindow.quit()

    def onclick_next_presentation(self):
        try:
            question = self.presentation_dict[self.question_number+1]
        except KeyError:
            print("Question " + str(self.question_number+1) + " DNE")
            return
        self.question_number += 1
        # Note - format_question_text updates the correct answer, so we need to do this BEFORE we send the
        # curr_correct_letter to the server process
        question_text = self.format_question_text(question, self.question_number)
        self.question_text.set(question_text)
        self.parent_pipe.send({'update_question_number' : self.question_number, 'update_correct_answer' : self.curr_correct_letter})

    def onclick_back_presentation(self):
        try:
            question = self.presentation_dict[self.question_number-1]
        except KeyError:
            return
        self.question_number -= 1
        # Note - format_question_text updates the correct answer, so we need to do this BEFORE we send the
        # curr_correct_letter to the server process
        question_text = self.format_question_text(question, self.question_number)
        self.parent_pipe.send({'update_question_number' : self.question_number, 'update_correct_answer' : self.curr_correct_letter})
        self.question_text.set(question_text)

    def onclick_toggle_accept_answers(self):
        self.accepting_answers = (not self.accepting_answers)
        toggle_button_text = "Start accepting answers"
        if self.accepting_answers:
            toggle_button_text = "Stop accepting answers"
        self.parent_pipe.send({"update_accepting_answers" : self.accepting_answers})
        self.accept_answers_text.set(toggle_button_text)

    def onclick_show_data(self):
        if self.showing_data:
            self.question_text.set(self.curr_question_text)
            self.show_data_text.set("Show Question Data")
        else:
            self.parent_pipe.send("question_data")
            curr_question_stats = self.parent_pipe.recv()
            if curr_question_stats == "NO_DATA":
                return
            else:
                stats_string = self.process_question_stats(curr_question_stats)
                self.question_text.set(stats_string)
                self.show_data_text.set("Return To Question")
        self.showing_data = not self.showing_data

    def process_question_stats(self, question_stats):
        string = "Question " + str(self.question_number) + " - "
        string += "Correct Answer: " + self.curr_correct_letter + "\n"
        string += "Number of Correct Answers: " + str(question_stats.num_correct) + "\n"
        string += "Percent of class who got answer correct: " + str(round(question_stats.get_percent(), 2)) + "%\n"
        string += "Distribution:"
        for letter in ["A", "B", "C", "D", "E", "F"]:
            string += "\n" + letter + ": "
            for i in range(question_stats.answer_dict[letter]):
                string += "X"
        return string


    def format_question_text(self, question, question_number):
        curr_text = "Question " + str(question_number) + ": "
        curr_text += (question["question"] + "\n")
        # Initially set answers to only the wrong answers
        answers = question["wrong_answers"]
        for i in range(len(answers)):
            if answers[i] == "":
                answers = answers[0:i]
                break
        # Add correct answer to answer list
        correct_answer = question["answer"]
        answers.append(correct_answer)
        random.shuffle(answers)
        letters = ["A: ", "B: ", "C: ", "D: ", "E: ", "F: "]
        for i in range(len(answers)):
            if answers[i] == correct_answer:
                self.curr_correct_letter = letters[i][0]
            curr_text += letters[i] + answers[i] + "\n"
        self.curr_question_text = curr_text
        return curr_text

if __name__ == '__main__':
    app = Presentation()
    app.run()
