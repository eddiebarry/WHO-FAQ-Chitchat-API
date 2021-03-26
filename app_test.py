import requests
import json

# base_url="http://0.0.0.0:5000/get-chitchat"

base_url="http://ec2-34-245-111-10.eu-west-1.compute.amazonaws.com:5001/get-chitchat"
# base_url="http://18.203.115.216:5007/api/v1/reranking"

qry = 'help me quit smoking'

params = {
    "query": qry,
}

r = requests.get(base_url, data=json.dumps(params))
response  = r.json()
import pdb; pdb.set_trace()