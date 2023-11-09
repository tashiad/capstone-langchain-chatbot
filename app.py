from flask import Flask, render_template
from flask import request, jsonify, abort

from langchain.llms import Cohere

app = Flask(__name__)

def answer_from_knowledgebase(message):
    # TODO: Write your code here
    return ""

def search_knowledgebase(message):
    # TODO: Write your code here
    sources = ""
    return sources

def answer_as_chatbot(message):
    # TODO: Write your code here
    return ""

@app.route('/kbanswer', methods=['POST'])
def kbanswer():
    # TODO: Write your code here
    
    # call answer_from_knowledebase(message)
        
    # Return the response as JSON
    return 

@app.route('/search', methods=['POST'])
def search():    
    # Search the knowledgebase and generate a response
    # (call search_knowledgebase())
    
    # Return the response as JSON
    return

@app.route('/answer', methods=['POST'])
def answer():
    message = request.json['message']
    
    # Generate a response
    response_message = answer_as_chatbot(message)
    
    # Return the response as JSON
    return jsonify({'message': response_message}), 200

@app.route("/")
def index():
    return render_template("index.html", title="")

if __name__ == "__main__":
    app.run()