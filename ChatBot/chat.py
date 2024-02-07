from flask import Flask, render_template, request, jsonify
import google.generativeai as palm

palm_api_key = 'AIzaSyBcVBDZtyGiD_zGo6dk06I7LBeqRvyMIoI'
palm.configure(api_key=palm_api_key)

# Set up your Flask app
app = Flask(__name__)

# Route for the main page
@app.route("/")
def index():
    return render_template('chat.html')

# Route for handling chat requests
@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    
    # Get the chat response from Google Palm API
    google_palm_response = get_google_palm_response(msg)

    return jsonify({"response": google_palm_response})

# Function to get chat response from Google Palm API
def get_google_palm_response(text):
    # Make a call to the Google Palm API using the provided library
    # Replace 'your_google_palm_api_key' with your actual API key
    google_palm_api = palm(api_key='AIzaSyBcVBDZtyGiD_zGo6dk06I7LBeqRvyMIoI')
    response = google_palm_api.get_response(text)

    return response

# Run the Flask app
if __name__ == '__main__':
    app.run()
