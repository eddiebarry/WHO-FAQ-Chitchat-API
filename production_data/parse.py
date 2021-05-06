import os, pdb
import json 
  

labeled_data = {

}

for x in os.listdir("./vla_data_no_variations"):
    if x.endswith(".json"):
        # Opening JSON file 
        f = open("./vla_data_no_variations/"+x,) 

        data = json.load(f) 

        statement = data['question']

        labeled_data[statement]=0
        f.close()
# pdb.set_trace()

f = open("./qna.json",) 
data = json.load(f)
f.close()
# pdb.set_trace()
for x in data['qnas']:
    # pdb.set_trace()
    statements = x["data"]["questions"]["en"]
    for statement in statements:
        labeled_data[statement]=1

json_file_name = "labelled_data.json"
print("writing", json_file_name)
with open(json_file_name , 'w') as json_file:
    json.dump(labeled_data, json_file,\
        indent = 4, sort_keys=True)


f = open("./qna.json",) 
data = json.load(f)
f.close()
# pdb.set_trace()
for x in data['qnas']:
    # pdb.set_trace()
    statements = x["data"]["questions"]["en"]
    for statement in statements:
        labeled_data[statement]=x["data"]["answers"]["en"][0]

json_file_name = "chitchat_answers.json"
print("writing", json_file_name)
with open(json_file_name , 'w') as json_file:
    json.dump(labeled_data, json_file,\
        indent = 4, sort_keys=True)