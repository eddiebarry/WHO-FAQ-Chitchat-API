#TODO : FIX imports to follow pep8 sorted order
import sys, os, json, pdb, random, copy, hashlib, re, sys
from datetime import datetime
# from flask_caching import Cache
from collections import defaultdict 
from threading import Thread

import fasttext, faiss
import flask
from flask import request, jsonify
import numpy as np

ft = fasttext.load_model('./cc.en.300.bin')
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
app.config['model']=ft
# Only chithcat index
app.config['chitchat_index']=chitchat_index
app.config['id_chitchat_answer']=id_chitchat_answer
app.config['id_chitchat_question']=id_chitchat_question

# Combined index
# app.config['chitchat_index']=index


@app.route('/get-chitchat', methods=['GET'])
def get_chitchat():
    request_json = json.loads(request.data, strict=False)
    if 'query' not in request_json.keys():
        return jsonify({"message":"request does not contain query"})
    else:
        request_json['query'] = re.sub('[^A-Za-z0-9\s]+', '', request_json['query'])

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