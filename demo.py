#!/usr/bin/env python
# coding: utf-8

# In[1]:


import fasttext


# In[2]:


# import io

# def load_vectors(fname):
#     fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
#     n, d = map(int, fin.readline().split())
#     data = {}
#     for line in fin:
#         tokens = line.rstrip().split(' ')
#         data[tokens[0]] = map(float, tokens[1:])
#     return data


# In[3]:


# # vec = load_vectors("/Users/edgarmonis/Desktop/code/WHO/chitchat-fasttext/crawl-300d-2M.vec")
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context


# In[4]:


# import fasttext.util
# fasttext.util.download_model('en', if_exists='ignore')


# In[5]:


ft = fasttext.load_model('cc.en.300.bin')


# In[6]:


ft.get_sentence_vector("My name is jeff")[:10]


# In[7]:


import json 

# f = open("/Users/edgarmonis/Desktop/code/WHO/chitchat-fasttext/data/labelled_data.json",) 
f = open("/WHO-FAQ-Chitchat-API/production_data/labelled_data.json",)
data = json.load(f)


# In[8]:


vec_labels = {}
for x in data.keys():
    vec_labels[x] = (x,ft.get_sentence_vector(x))


# In[23]:


import numpy as np

a = np.empty([0,300])

for x in vec_labels.keys():
    vec = vec_labels[x][1]
    a = np.concatenate((a,np.expand_dims(vec,axis=0)),axis=0)


# In[37]:


test = a[:10]
test = np.float32(test)
test_id = np.arange(test.shape[0])

print(test.shape)
test_id

test.dtype


# In[47]:


# # vec_labels[x]
# import faiss

# index1 = faiss.IndexIDMap2(faiss.IndexFlatL2(300))

# index1.add_with_ids(test,test_id)                  # add vectors to the index

# vec_labels[x]
import faiss

index = faiss.IndexIDMap2(faiss.IndexFlatL2(300))

index.add_with_ids(np.float32(a),np.arange(a.shape[0]))                  # add vectors to the index


# In[48]:


# test[:1].shape
D, I = index.search(test[:1], 4)
print(D)
print(I)


# In[52]:


# faiss.write_index(index, "./chitchat_faq.bin")
faiss.write_index(index, "/WHO-FAQ-Chitchat-API/chitchat_faq.bin")


# In[54]:


# index2 = faiss.read_index("./chitchat_faq.bin")
index2 = faiss.read_index("/WHO-FAQ-Chitchat-API/chitchat_faq.bin")
D, I = index2.search(test[:1], 4)

print(D)
print(I)


# In[12]:


from numpy import dot
from numpy.linalg import norm

def cosine_sim(a,b):
    return dot(a, b)/(norm(a)*norm(b))


# In[32]:



top_5 = []

for x in vec_labels.keys():
    if data[x] == 0:
        dist_ = []
        for y in vec_labels.keys():
            dist = cosine_sim(vec_labels[x][1],vec_labels[y][1])
            dist_.append((dist,y))

        dist_ = sorted(dist_, reverse=True)
        top_5.append((x,dist_[:100]))


# In[55]:


# top_5[1]


# In[56]:


# top_5_[1]
import fasttext
ft = fasttext.load_model('cc.en.300.bin')


# In[81]:


# f = open("/Users/edgarmonis/Desktop/code/WHO/chitchat-fasttext/data/chitchat_answers.json",) 
f = open("/WHO-FAQ-Chitchat-API/production_data/chitchat_answers.json",)
chitchat_data = json.load(f)
f.close()

id_chitchat_answer = {}
id_chitchat_question = {}
id_chitchat_vector = {}


chitchat_vecs = np.empty([0,300])
chitchat_ids = np.empty([0])

chitchat_id = 0
for x in data.keys():
    if data[x]==1:
        id_chitchat_answer[chitchat_id] = chitchat_data[x]
        id_chitchat_question[chitchat_id] = x
        id_chitchat_vector[chitchat_id] = np.float32(ft.get_sentence_vector(x))

        chitchat_vecs = np.concatenate(
            (chitchat_vecs,np.expand_dims(id_chitchat_vector[chitchat_id], axis=0))
        )
        chitchat_ids = np.concatenate(
            (chitchat_ids, np.array([chitchat_id],dtype=np.int))
        )
        chitchat_id += 1


# In[82]:


# json_file_name = "id_chitchat_answer.json"
json_file_name = "/WHO-FAQ-Chitchat-API/production_data/id_chitchat_answer.json"
print("writing", json_file_name)
with open(json_file_name , 'w') as json_file:
    json.dump(id_chitchat_answer, json_file,        indent = 4, sort_keys=True)

# json_file_name = "id_chitchat_question.json"
json_file_name = "/WHO-FAQ-Chitchat-API/production_data/id_chitchat_question.json"
print("writing", json_file_name)
with open(json_file_name , 'w') as json_file:
    json.dump(id_chitchat_question, json_file,        indent = 4, sort_keys=True)

chitchat_vecs = np.float32(chitchat_vecs)
chitchat_ids = chitchat_ids.astype(int)


# In[100]:


import faiss

index = faiss.IndexIDMap2(faiss.IndexFlatL2(300))

index.add_with_ids(chitchat_vecs,chitchat_ids)


# In[104]:


# faiss.write_index(index, "./chitchat.bin")
faiss.write_index(index, "/WHO-FAQ-Chitchat-API/production_data/chitchat.bin")


# In[116]:


vec = np.expand_dims(np.float32(
            ft.get_sentence_vector(
                "I am happy"
            )
        ),axis=0)
D,I = index.search(vec,10)


# In[131]:


# id_chitchat_answer[I[0][3]]


# In[ ]:




