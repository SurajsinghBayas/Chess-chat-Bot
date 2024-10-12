import json
import random
import spacy
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


 
nlp = spacy.load("en_core_web_sm")


with open("main.json", "r") as json_file:
    data = json.load(json_file)


intents = data["intents"]


patterns = []
labels = []
for intent in intents:
    intent_tag = intent["tag"]
    for pattern in intent["patterns"]:
        patterns.append(pattern.lower())
        labels.append(intent_tag)

@app.route('/')  
def index():
    return render_template('index.html')  

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['user_message'].lower()

    best_match_response = "I'm sorry, I don't understand."
    best_match_score = 0

   
    user_doc = nlp(user_input)

    
    for intent in intents:
        intent_tag = intent["tag"]
        for pattern in intent["patterns"]:
            pattern_doc = nlp(pattern.lower())
            score = user_doc.similarity(pattern_doc)  

            
            if score > best_match_score:
                best_match_score = score
                best_match_response = random.choice(intent["responses"])

    return jsonify({'bot_response': best_match_response})

if __name__ == '__main__':
    app.run(debug=True)