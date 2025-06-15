from flask import Flask, render_template, request, jsonify
from langchain.llms import Cohere
from langchain import PromptTemplate, LLMChain
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)

def answer_as_chatbot(message):
    template = """Question: {question}

Answer as if you are an expert Python developer"""

    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm = Cohere(cohere_api_key=os.environ["COHERE_API_KEY"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    res = llm_chain.run(message)
    return res 

@app.route('/answer', methods=['POST'])
def answer():
    message = request.json['message']
    
    # Generate a response as an expert Python developer
    response_message = answer_as_chatbot(message)
    
    # Return the response as JSON
    return jsonify({'message': response_message}), 200

@app.route("/")
def index():
    return render_template("index.html", title="")

if __name__ == "__main__":
    app.run(debug=True)
