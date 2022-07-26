import discord
import json

async def lchannel(message):
    role = discord.utils.find(lambda r: r.name == 'mol', message.guild.roles)
    if role not in message.author.roles:
        return await message.reply('invalid perms')
    with open('commands/message_data.json', 'r+') as f:
        data = json.load(f)
        data['leaderboard_channel_id'] = message.channel.id
        f.seek(0)        
        json.dump(data, f, indent=4)
        f.truncate() 
   