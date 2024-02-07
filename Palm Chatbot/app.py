from flask import Flask, render_template, request
import google.generativeai as palm

#API key
palm_api_key = 'AIzaSyBcVBDZtyGiD_zGo6dk06I7LBeqRvyMIoI'

#PaLM API to use the API key
palm.configure(api_key=palm_api_key)

#Flask App
app = Flask(__name__)

#home page route
@app.route("/")
def home():
    return render_template("chatbot.html")

#chatbot route
@app.route("/chatbot", methods=["POST"])
def chatbot():
  #message input from the user
  user_input = request.form["message"]

  models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
  model = models[0].name

  #PaLM API to generate a response
  prompt = f"User: {user_input}\nPaLM Bot: "

  # Generate the response
  response = palm.generate_text(
    model=model,
    prompt=prompt,
    stop_sequences=None,
    temperature=0,
    max_output_tokens=100
  )

  #bot's response
  bot_response = response.result

  # Add the user input and bot response to the chat history
  chat_history = []
  chat_history.append(f"User: {user_input}\nPaLM Bot: {bot_response}")

  # Render the Chatbot template with the response text
  return render_template(
    "chatbot.html",
    user_input=user_input,
    bot_response=bot_response,
    chat_history=chat_history,
  )

if __name__ == "__main__":
  app.run(debug=True)
