from flask import Flask, request
import google.generativeai as genai
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os

load_dotenv() 
# Init the Flask App
app = Flask(__name__)

# Initialize the Gemini API key
# export GEMINI_API_KEY=YOUR API KEY
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define a function to generate answers using Gemini
def generate_answer(question):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(question)

    if response and hasattr(response, "text"):
        return response.text.strip()
    return "Sorry, I couldn't generate an answer."

# Define a route to handle incoming requests
@app.route('/chatgemini', methods=['POST'])
def chatgemini():
    incoming_que = request.values.get('Body', '').lower()
    print("Question: ", incoming_que)

    # Generate the answer using Gemini
    answer = generate_answer(incoming_que)
    print("BOT Answer: ", answer)

    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    msg.body(answer)

    return str(bot_resp)

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
