import discord
import time
import json

async def lchannel(message):
    role = discord.utils.find(lambda r: r.name == 'mol', message.guild.roles)
    if role not in message.author.roles:
        return await message.reply('invalid perms')
    with open('commands/message_data.json', 'r+') as f:
        data = json.load(f)
        data['leaderboard_message_id'] = message.channel.id
        f.seek(0)        
        json.dump(data, f, indent=4)
        f.truncate() 
    l_message = await message.channel.send(f'Set leaderboard channel to {message.channel.name}')  
    time.sleep(2)
    await l_message.delete()
    await message.delete()