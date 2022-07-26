import json
import discord

async def extrapoints(message):
    role = discord.utils.find(lambda r: r.name == 'mol', message.guild.roles)
    if role not in message.author.roles:
        return await message.reply('invalid perms')
    sliced = message.content[13:]
    print(int(sliced))
    with open('scores.json', 'r+') as f:
        data = json.load(f)
        data['extra_points'] = int(sliced) 
        f.seek(0)        
        json.dump(data, f, indent=4)
        f.truncate() 
        await message.reply(f'Extrapoints have been set to {sliced}') 