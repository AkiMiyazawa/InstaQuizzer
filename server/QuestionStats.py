class QuestionStats:
    def __init__(self, num_answers=0, num_correct=0, answer_dict=None):
        self.num_answers = num_answers
        self.num_correct = num_correct
        if answer_dict is None:
            self.answer_dict = {"A" : 0, "B" : 0, "C" : 0, "D": 0, "E" : 0, "F" : 0}

    def get_percent(self):
        return 100*self.num_correct/self.num_answers

    def increment_answer(ans):
        self.answer_dict[ans] += 1

    def decrement_answer(ans): 
        self.answer_dict[ans] -= 1