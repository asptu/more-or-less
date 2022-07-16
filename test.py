import json
with open('./scores.json') as fp:
    scores = json.load(fp)
    higher = scores['higher']
    lower = scores['lower']

print(higher)
print(lower)  