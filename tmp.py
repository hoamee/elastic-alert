import json

js = json.load(open('tmp.json', 'r'))
print(js['fields']['message'][0])