import json
import random


class QuestionManager:

    def __init__(self, filename="questions.json"):
        with open(filename, "r") as file:
            self.questions = json.load(file)

    def get_questions(self, subject):
        return self.questions.get(subject, [])

    def get_random_question(self, subject):

        if subject in self.questions:
            return random.choice(self.questions[subject])
        else:
            return "No Questions Found!"