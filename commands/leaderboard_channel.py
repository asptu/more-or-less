import json

async def lchannel(message):

    with open('commands/message_data.json', 'r+') as f:
        data = json.load(f)
        data['leaderboard_channel_id'] = message.channel.id
        f.seek(0)        
        json.dump(data, f, indent=4)
        f.truncate() 
   