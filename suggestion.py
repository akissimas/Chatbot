import pandas as pd
import random


class Suggestion:
    def __init__(self):
        dataset = pd.read_csv("./datasets/suggestions.csv")

        self.dataset_dict = dict(zip(dataset["Text"], dataset["Emotion"]))


    def search(self, value):
        result = [k for k, v in self.dataset_dict.items() if v == value]
        return random.choice(result)


if __name__ == '__main__':
    sug = Suggestion()

    result = sug.search("sadness")

    print(result)





