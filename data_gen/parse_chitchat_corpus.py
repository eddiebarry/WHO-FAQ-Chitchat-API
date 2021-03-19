import os, hashlib, pdb, json, re

# Using readlines() 

def parse_chitchat_file(
  path='/Users/edgarmonis/Desktop/code/WHO/chitchat-fasttext/data_gen/Chitchat - English Friendly EDIT.txt'):
  file1 = open(path, 'r') 
  # Lines = file1.readlines() 
    

  # Strips the newline character 
  # for line in Lines: 
  line = "lol"
  while line[:3] != '# ?':
      line = file1.readline().strip()

  data = {}
  while line is not None:
      if line[:3] == '# ?':
          # start
          question_list = [line.replace("# ? ","")]
          line = file1.readline().strip()

      while line[:2] == '- ':
          question_list.append(line.replace('- ',''))
          line = file1.readline().strip()

      if line[:2]=='**':
          line = file1.readline().strip()
          while line[:3] != '```':
              line = file1.readline().strip()
          line = file1.readline().strip()
          answer_list = [line]
          line = file1.readline().strip()
          line = file1.readline().strip()
      
      exit_=False
      while line[:3] != '# ?':
          line = file1.readline().strip()
          if not line:
              exit_ = True
              break
      
      answer = answer_list[0].strip('\\').strip()
      # question = re.sub('[^A-Za-z0-9\s]+', '', question)
      for question in question_list:
        data[question.strip('\\').strip()] = answer
      
      if exit_:
          return data

data_friendly = parse_chitchat_file(path="/Users/edgarmonis/Desktop/code/WHO/chitchat-fasttext/data_gen/Chitchat - English Friendly EDIT.txt")
data_professional = parse_chitchat_file(path="/Users/edgarmonis/Desktop/code/WHO/chitchat-fasttext/data_gen/Chitchat - English_Professional EDIT.txt")

data_friendly.update(data_professional)

json_file_name = "emoji_qna_combined.json"
with open(json_file_name , 'w') as json_file:
    json.dump(data_friendly, json_file,\
    indent = 4, sort_keys=True)

# pdb.set_trace()