from flask import Flask, render_template, request, jsonify
from langchain.llms import Cohere
from langchain import PromptTemplate, LLMChain
import os
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.embeddings import CohereEmbeddings
from langchain.vectorstores import Chroma

load_dotenv()

app = Flask(__name__)

def answer_as_chatbot(message):
    template = """Question: {question}
Answer as if you are an expert Python developer"""
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm = Cohere(cohere_api_key=os.environ["COHERE_API_KEY"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    return llm_chain.run(message)

def load_db():
    try:
        embeddings = CohereEmbeddings(cohere_api_key=os.environ["COHERE_API_KEY"])
        vectordb = Chroma(persist_directory='db', embedding_function=embeddings)
        docs = vectordb.get()
        if len(docs['documents']) == 0:
            print("⚠️ Warning: No documents found in the database.")
        qa = RetrievalQA.from_chain_type(
            llm=Cohere(cohere_api_key=os.environ["COHERE_API_KEY"]),
            chain_type="refine",
            retriever=vectordb.as_retriever(),
            return_source_documents=True
        )
        return qa
    except Exception as e:
        print("❌ Failed to load knowledge base:", e)
        return None

qa = load_db()

@app.route('/')
def index():
    return render_template('index.html', title='')

@app.route('/answer', methods=['POST'])
def answer():
    message = request.json.get('message', '')
    response_message = answer_as_chatbot(message)
    return jsonify({'message': response_message}), 200

@app.route('/kbanswer', methods=['POST'])
def answer_from_knowledgebase():
    if not qa:
        print("❌ Knowledge base not loaded.")
        return jsonify({'error': 'Knowledge base is not loaded'}), 500
    try:
        message = request.json.get('message', '')
        res = qa({"query": message})
        return jsonify({'message': res['result']}), 200
    except Exception as e:
        print("❌ Error handling knowledge base query:", e)
        return jsonify({'error': 'Something went wrong with the knowledgebase query.'}), 500

@app.route('/search', methods=['POST'])
def search_knowledgebase():
    if not qa:
        return jsonify({'error': 'Knowledge base is not loaded'}), 500
    try:
        message = request.json.get('message', '')
        res = qa({"query": message})
        
        # Format source documents nicely
        sources = ""
        for count, source in enumerate(res['source_documents'], 1):
            sources += f"Source {count}:\n{source.page_content}\n\n"
        
        return jsonify({
            'message': res['result'],
            'sources': sources.strip()
        }), 200
    except Exception as e:
        print("Error in /search:", e)
        return jsonify({'error': 'Something went wrong with the search query.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
