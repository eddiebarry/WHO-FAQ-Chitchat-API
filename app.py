from datetime import datetime
import json
from os import chdir, getcwd
from os.path import join as os_join
from subprocess import call as subprocess_call
from threading import Thread

import fasttext, faiss
import flask
from flask import request, jsonify
# from flask_caching import Cache
import numpy as np

from preprocessing import preprocess


MODEL_WEIGHTS_DIR = os_join(
    getcwd(),
    "model_weights"
)
MODEL_WEIGHTS_PATH = os_join(
    MODEL_WEIGHTS_DIR,
    "cc.en.300.bin"
)


# chitchat_index = faiss.read_index("./production_data/chitchat_emoji_faq.bin")
chitchat_index = faiss.read_index("./production_data/chitchat_faq.bin")

# f = open("./production_data/id_emoji_chitchat_answer.json",) 
f = open("./production_data/id_chitchat_answer.json",)
id_chitchat_answer = json.load(f)
f.close()

# f = open("./production_data/id_emoji_chitchat_question.json",) 
f = open("./production_data/id_chitchat_question.json",)
id_chitchat_question = json.load(f)
f.close()

# SETUP
app = flask.Flask(__name__)
# Only chithcat index
app.config['chitchat_index']=chitchat_index
app.config['id_chitchat_answer']=id_chitchat_answer
app.config['id_chitchat_question']=id_chitchat_question

# Combined index
# app.config['chitchat_index']=index


@app.route('/download-weights', methods=['GET'])
def download_model_weights():
    """
    Download the embedding model weights and load it into a configuration
    variable so that it i sloaded only once during the application lifetime.
    """
    # downloading the model weights:
    current_path = getcwd()
    chdir(MODEL_WEIGHTS_DIR)
    fasttext.util.download_model('en', if_exists='ignore')
    chdir(current_path)

    # loading the model only once, as a "global" variable for the application:
    app.config['model'] = fasttext.load_model(MODEL_WEIGHTS_PATH)

    return 200, "Model weights successfuly downloaded."


@app.route('/prepare-knowledge-base', methods=['GET'])
def prepare_knowledge_base():
    """
    Process and index the knowledge base, generating the files used by the
    application to serve chit-chat retrieval requests at runtime.
    """
    subprocess_call("demo.py", shell=True)

    return 200, "Knowledge base successfully processed and indexed."


@app.route('/get-chitchat', methods=['GET'])
def get_chitchat():
    request_json = json.loads(request.data, strict=False)
    if 'query' not in request_json.keys():
        return jsonify({"message":"request does not contain query"})

    request_json['query'] = preprocess(request_json['query'])

    vec =  np.expand_dims(np.float32(
            app.config['model'].get_sentence_vector(
                request_json['query']
            )
        ),axis=0)
    
    D,I = app.config['chitchat_index'].search(vec,1)
    response = {
        "chitchat_question" : app.config['id_chitchat_question'][str(I[0][0])],
        "chitchat_answer" : app.config['id_chitchat_answer'][str(I[0][0])],
        "confidence" : float(D[0][0]),
    }
    # ID which maps to chitchat question
    # ID which maps to chitchat answer
    # original_stdout = sys.stdout 
    # with open('./log.txt', 'a') as f:
    #     sys.stdout = f # Change the standard output to the file we created.
    #     print(" - ", "time : ", datetime.now().strftime("%H:%M:%S"),)
    #     print(" - ", response)
    #     sys.stdout = original_stdout
    print(" - ", "time : ", datetime.now().strftime("%H:%M:%S"),)
    print(" - ", response)

    return jsonify(response)

@app.route('/')
def hello_world():
    return 'Hello, World! The service is up for serving qna to the bot :-)'