import json

async def set_time(message, number):

    with open('./data/scores.json', 'r+') as f:
        data = json.load(f)
        data['time'] = int(number) 
        f.seek(0)        
        json.dump(data, f, indent=4)
        f.truncate() 
