import json

async def extrapoints(message):

    sliced = message.content[13:]
    print(int(sliced))
    with open('./data/scores.json', 'r+') as f:
        data = json.load(f)
        data['extra_points'] = int(sliced) 
        f.seek(0)        
        json.dump(data, f, indent=4)
        f.truncate() 
        await message.reply(f'Extrapoints have been set to {sliced}') 