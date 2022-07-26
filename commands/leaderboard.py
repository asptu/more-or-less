import json
import discord

async def show_leaderboard(message):  
    with open('leaderboard.json', 'r') as f:
        data = json.load(f)

    top_users = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}

    names = ''
    for postion, user in enumerate(top_users):
        names += f'{postion+1} - <@!{user}> with {top_users[user]}\n'

    embed = discord.Embed(title="Leaderboard", color=0x3B88C3)
    embed.add_field(name="Names", value=names, inline=False)
    await message.channel.send(embed=embed)   
