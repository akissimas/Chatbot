import numpy as np
from random import randint, choice
from app.suggestion import Suggestion
from emotion_detection import Emotion
from Blenderbot import BlenderBot
from re import search, split
# flask imports
from flask import Flask, render_template, request


def add_emoji_to_text(text, current_emotion):
    # create a dict of emojis based on the emotions (anger and sadness have the same emojis)
    emoji_dict = {
        "anger": ["\U0001F615", "\U0001F641"],                  # 😕, 🙁
        "sadness": ["\U0001F615", "\U0001F641"],                # 😕, 🙁
        "joy": ["\U0001F603", "\U0001F601", "\U0001F642"],      # 😃, 😁, 🙂
        "love": ["\U0001F60D", "\U0001F970"],                   # 😍, 🥰
        "surprise": ["\U0001F973"],                             # 🥳
        "fear": ["\U0001F62C"],                                 # 😬
    }

    # find the '?', '.' or '!' character in the given text
    character = search("[?|.|!]", text)

    # split the string
    output = split('[?|.|!]', text, 1)

    if character is not None:
        new_text = output[0] + f" {choice(emoji_dict[current_emotion])}{character[0]}" + ''.join(map(str, output[1:]))
    else:
        new_text = output[0] + f"{choice(emoji_dict[current_emotion])}" + ''.join(map(str, output[1:]))

    return new_text


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

    # find the emotion
    current_emotion = emotion.prediction(user_text)

    # initiate the variable which suggest a song
    reply = None

    # find and suggest music based on the emotion
    if randint(0, 1) == 1:
        result = suggest.search(current_emotion)
        reply = f"Hey! You might also be interested in listening to this song:<br>{result}"

    # save past user input and bot response
    global past_user_inputs
    global bot_response

    if past_user_text is not None:
        past_user_inputs.append(past_user_text)
        bot_response.append(past_bot_text)

    paylaod = bot.get_payolaod(past_user_inputs, bot_response, user_text)

    # sent the query
    query = bot.query(paylaod)

    # add emoji in text
    final_query = add_emoji_to_text(query['generated_text'], current_emotion)

    if reply is None:
        return final_query
    else:
        return f"{final_query}<br><br>{reply}"


if __name__ == '__main__':
    app.run()
