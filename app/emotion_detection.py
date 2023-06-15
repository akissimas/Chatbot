import numpy as np
import ktrain
from app.suggestion import Suggestion


class Emotion:
    def __init__(self):
        self.predictor = None

    def load_model(self):
        # Load predictor
        self.predictor = ktrain.load_predictor('../saved_model_v4')

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
        if len(inputArray) == 1:
            unique, counts = np.unique(inputArray, return_counts=True)

            # create a dict with the emotions and their occurrences
            emotion_dict = dict(zip(unique, counts))
            print(emotion_dict)

            # get the dominant emotion
            dominantEmotion = max(emotion_dict, key=emotion_dict.get)
            print(f"dominant emotion: {dominantEmotion}")

            # find and suggest music based on the dominant emotion
            suggest = Suggestion()

            result = suggest.search(dominantEmotion)

            print(f"looks like your emotion is: {dominantEmotion}\nI can suggest you this song: {result}")


            inputArray.clear()

        if query in 'q':
            break



    # Make A Prediction
    # sample = "It is so annoying when she starts typing on her computer in the middle of the night!", \
    #          "dude, that is my favorite sandwich place ever. ummm did you take PICTURES?", \
    #          "Chillin with the roomies. Can't wait for the zombie CLWN CR. Its gonna be 6-8 weeks", \
    #          "I'm having a problem with my photo here in twitter amf!!!...can't see my face!"

    # print(f"check accuracy: {emotion.check_accuracy()}\n")

    # print(f"prediction: {emotion.pipe_lr.predict(emotion.x_test.real)}\n")
    # print(f"prediction: {emotion.pipe_lr.predict(sample)}")

