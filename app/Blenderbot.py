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
