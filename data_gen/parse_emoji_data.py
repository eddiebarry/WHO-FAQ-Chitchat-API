import json, pdb, re
import pandas as pd

xl = pd.read_csv("./emoji_chitchat.csv")

f = open("./emoji_qna_combined.json",) 
labelled_data = json.load(f)
f.close()

cleaned_data = {}
for query in labelled_data:
    qry = re.sub('[^A-Za-z0-9\s]+', '', query)
    cleaned_data[qry] = query

for row_num, row in xl.iterrows():
    if row_num <= 1:
        continue
    # print(row['Unnamed: 0'])
    # print(row['Unnamed: 2'])

    for query in row['Unnamed: 0'].split('/'):
        query = query.strip()
        query = re.sub('[^A-Za-z0-9\s]+', '', query)

        if not query in  cleaned_data.keys():
            labelled_data[query] = row['Unnamed: 2']
            print(query, "added")
        else:
            original_query = cleaned_data[query]
            old_response = labelled_data[original_query]

            labelled_data[original_query] = row['Unnamed: 2']
            for key in labelled_data.keys():
                if labelled_data[key] == old_response:
                    labelled_data[key] = row['Unnamed: 2']

json_file_name = "emoji_data_qna.json"
with open(json_file_name , 'w') as json_file:
    json.dump(labelled_data, json_file,\
    indent = 4, sort_keys=True)
