import numpy as np
import ktrain
from app.suggestion import Suggestion


class Emotion:
    def __init__(self):
        self.predictor = None

    def load_model(self):
        # Load predictor
        self.predictor = ktrain.load_predictor('../text classification/saved_model')

    def prediction(self, text):
        return self.predictor.predict(text)


if __name__ == '__main__':
    emotion = Emotion()

    emotion.load_model()

    inputArray = []

    while True:
        query = input("> ")

        currentEmotion = emotion.prediction(query)

        inputArray.append(currentEmotion)

        # emotion capture of 3 last inputs
        if len(inputArray) == 3:
            unique, counts = np.unique(inputArray, return_counts=True)

            # create a dict with the emotions and their occurrences
            emotion_dict = dict(zip(unique, counts))
            print(emotion_dict)

            # get the dominant emotion
            dominantEmotion = max(emotion_dict, key=emotion_dict.get)
            print(f"dominant emotion: {dominantEmotion}")

            # find and suggest music based on the dominant emotion TODO: na antistoixisw kapoia emotions sto idio (p.x. sadness,fear)
            suggest = Suggestion()

            result = suggest.search(dominantEmotion)

            print(f"looks like your emotion is: {dominantEmotion}\nI can suggest you this song: {result}")


            inputArray.clear()

        if query in 'q':
            break



    # Make A Prediction
    # sample = "I have to look at life in her perspective, and it would break anyone’s heart.", \
    #          "We stayed in a tiny mountain village called Droushia, and these people brought hospitality to incredible new heights.", \
    #          "But the rest of it came across as a furious, drunken rant.", \
    #          "Which, to be honest, was making Brad slightly nervous."

    # print(f"check accuracy: {emotion.check_accuracy()}\n")

    # print(f"prediction: {emotion.pipe_lr.predict(emotion.x_test.real)}\n")
    # print(f"prediction: {emotion.pipe_lr.predict(sample)}")

