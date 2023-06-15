import requests
import time


class BlenderBot:
    def __init__(self):
        self.API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
        self.headers = {"Authorization": "Bearer xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}

    # create the payload
    def get_payolaod(self, past_user_inputs, bot_response, text):
        payload = {
            "inputs": {
                "past_user_inputs": past_user_inputs,
                "generated_responses": bot_response,
                "text": text
            },
        }
        return payload


    def query(self, payload):
        response = requests.post(self.API_URL, headers=self.headers, json=payload)

        if response.status_code == 503:  # This means we need to wait for the model to load
            estimated_time = response.json()['estimated_time']
            time.sleep(estimated_time)
            print(f"Sleeping for model to load: {estimated_time}")
            response = requests.post(self.API_URL, headers=self.headers, data=payload)

        return response.json()


# bot = BlenderBot()
#
# flag = True
#
# while True:
#     message = input("MESSAGE: ")
#     if message in ["", "q", "quit"]:
#         break
#
#
#     if flag:
#         paylaod = bot.get_payolaod("Hi!", "Hi! I'm ChatBot 😄", message)  # initial message
#         flag = False
#     else:
#         paylaod = bot.get_payolaod(past_user_inputs, bot_response, message)
#
#     # sent the query
#     query = bot.query(paylaod)
#
#     # save user input and bot response
#     past_user_inputs = message
#     bot_response = query['generated_text']
#
#     # print bot response
#     print(f"🤖: {query}")
#

