from flask import Flask, render_template, request, jsonify

# Replace 'GooglePalmAPI' with the actual Python client library for the API
from google.generativeai import GooglePalmAPI

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    return get_chat_response(input)

def get_chat_response(text):
    # Let's chat for 5 lines
    for step in range(5):
        new_user_input_ids = tokenizer.encode(str(text) + tokenizer.eos_token, return_tensors='pt')
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

        # Replace 'GooglePalmAPI' with the actual Python client library for the API
        google_palm_api = GooglePalmAPI(api_key='AIzaSyBcVBDZtyGiD_zGo6dk06I7LBeqRvyMIoI')
        google_palm_response = google_palm_api.get_response(text)

        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    return jsonify({"response": response, "google_palm_response": google_palm_response})

if __name__ == '__main__':
    app.run()
