import numpy as np
from app.suggestion import Suggestion
from emotion_detection import Emotion
from Blenderbot import BlenderBot
# flask imports
from flask import Flask, render_template, request


#  initialization of variables
emotion = Emotion()

emotion.load_model()

suggest = Suggestion()

bot = BlenderBot()

inputArray = []

past_user_inputs = []

bot_response = []

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')
    past_bot_text = request.args.get('botMsg')
    past_user_text = request.args.get('userMsg')

    # if past_user_text is None:
    #     past_user_text = ' '

    # find the emotion
    current_emotion = emotion.prediction(user_text)

    print(f"{user_text} : {current_emotion}")  # TODO: DEBUG

    inputArray.append(current_emotion)

    # initiate the variable which suggest a song
    reply = None
    # emotion capture of 5 last inputs
    if len(inputArray) == 3:
        unique, counts = np.unique(inputArray, return_counts=True)

        # create a dict with the emotions and their occurrences
        emotion_dict = dict(zip(unique, counts))
        print(emotion_dict)  # TODO: DEBUG

        # get the dominant emotion
        dominant_emotion = max(emotion_dict, key=emotion_dict.get)
        print(f"dominant emotion: {dominant_emotion}")  # TODO: DEBUG

        # find and suggest music based on the dominant emotion
        result = suggest.search(dominant_emotion)

        reply = f"looks like your emotion is {dominant_emotion}.<br>I can suggest you this song:<br>{result}"

        inputArray.clear()


    # save past user input and bot response
    global past_user_inputs
    global bot_response

    if past_user_text is not None:
        past_user_inputs.append(past_user_text)
        bot_response.append(past_bot_text)


    paylaod = bot.get_payolaod(past_user_inputs, bot_response, user_text)

    # sent the query
    query = bot.query(paylaod)

    print(query)  # TODO: DEBUG

    if reply is None:
        return query['generated_text']
    else:
        return f"{query['generated_text']}<br><br>{reply}"


if __name__ == '__main__':
    app.run()
