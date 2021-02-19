import requests
import json

base_url="http://0.0.0.0:5001/get-chitchat"
# base_url="http://18.203.115.216:5007/api/v1/reranking"

qry = 'i am sad'

params = {
    "query": qry,
}

r = requests.get(base_url, json=json.dumps(params))
response  = r.json()
import pdb; pdb.set_trace()