class User:
    def __init__(self, answers=None, num_correct=0):
        # We have to do this to prevent a shared per-class dict
        # obj instead of the per-instance dictionary we want - ugh!
        if answers is None:
            self.answers = {}
        self.num_correct = num_correct

    def get_percent(self):
        return self.num_correct/len(self.answers)