import numpy as np
from app.suggestion import Suggestion

# flask imports
from flask import Flask, render_template, request

# chatterbot imports
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from emotion_detection import Emotion


#  initialization of emotion_detection
emotion = Emotion()

emotion.load_model()


#  initialization of chatterbot
chatbot = ChatBot("Chatbot")

# trainer = ChatterBotCorpusTrainer(chatbot)
#
# trainer.train(
#     "chatterbot.corpus.english"
# )

inputArray = []

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')

    # find the emotion
    currentEmotion = emotion.prediction(userText)

    print(currentEmotion)  # TODO: DEBUG

    inputArray.append(currentEmotion)

    # emotion capture of 3 last inputs
    if len(inputArray) == 3:
        unique, counts = np.unique(inputArray, return_counts=True)

        # create a dict with the emotions and their occurrences
        emotion_dict = dict(zip(unique, counts))
        print(emotion_dict)  # TODO: DEBUG

        # get the dominant emotion
        dominantEmotion = max(emotion_dict, key=emotion_dict.get)
        print(f"dominant emotion: {dominantEmotion}")  # TODO: DEBUG

        # find and suggest music based on the dominant emotion TODO: na antistoixisw kapoia emotions sto idio (p.x. sadness,fear)
        suggest = Suggestion()

        result = suggest.search(dominantEmotion)

        reply = f"looks like your emotion is {dominantEmotion}.<br>I can suggest you this song:<br>{result}"

        inputArray.clear()

        return reply


    return str(chatbot.get_response(userText))


if __name__ == '__main__':
    app.run()
