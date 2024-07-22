from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')

    if question:
        response = handle_question(question)
        return jsonify({'response': response})
    return jsonify