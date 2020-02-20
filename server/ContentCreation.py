import tkinter as tk
import pygubu
import json

class ContentCreation:
    def __init__(self, file_path):
        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('Desktop.ui')

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('content_creation_toplevel')

        #4: Connect callbacks
        builder.connect_callbacks(self)

        #5: Get variables
        self.question_label = self.builder.get_variable("question_label")
        self.question = self.builder.get_variable("question_entry")
        self.correct_answer = self.builder.get_variable("correct_answer")
        self.wrong_entries = [self.builder.get_variable("entry_wrong1"),
                              self.builder.get_variable("entry_wrong2"),
                              self.builder.get_variable("entry_wrong3"),
                              self.builder.get_variable("entry_wrong4"),
                              self.builder.get_variable("entry_wrong5")]

        #6: Start variables for keeping track of internal state
        self.question_number = 1
        self.max_question_number = 1
        self.curr_questions = {}
        self.storage_path = file_path

    def onclick_go_back_button(self):
        if self.question_number == 1:
           return
        self.question_number -= 1
        self.question_label.set("Question " + str(self.question_number) + ":")
        self.populate_entries(self.question_number)

    def onclick_finish_questions_button(self):
        q = self.question.get()
        ans = self.correct_answer.get()
        wrongs = []
        for entry in self.wrong_entries:
            wrongs.append(entry.get())
        self.curr_questions[self.question_number] = {"question" : q, "answer" : ans, "wrong_answers" : wrongs}
        self.write_curr_questions()
        self.mainwindow.quit()

    def onclick_next_question_button(self):
        if self.question_number > self.max_question_number:
            self.max_question_number = self.question_number
        q = self.question.get()
        ans = self.correct_answer.get()
        # Store all wrong answers in 1 list
        wrongs = []
        for entry in self.wrong_entries:
            wrongs.append(entry.get())
        self.curr_questions[self.question_number] = {"question" : q, "answer" : ans, "wrong_answers" : wrongs}
        self.question_number += 1
        self.question_label.set("Question " + str(self.question_number) + ":")
        self.populate_entries(self.question_number)

    def populate_entries(self, question_number):
        if question_number <= self.max_question_number:
            self.question.set(self.curr_questions[question_number]["question"])
            self.correct_answer.set(self.curr_questions[question_number]["answer"])
            wrongs = self.curr_questions[question_number]["wrong_answers"]
            for i in range(len(wrongs)):
                wrong_ans = wrongs[i]
                self.wrong_entries[i].set(wrong_ans)
        else:
            # Clear entries
            self.question.set("")
            self.correct_answer.set("")
            for entry in self.wrong_entries:
                entry.set("")

    def write_curr_questions(self):
        write_file = open(self.storage_path, "w+")
        json.dump(self.curr_questions, write_file)


if __name__ == '__main__':
    app = Content_Creation()
    app.run()