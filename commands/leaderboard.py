import json
import discord

async def show_leaderboard(message):  
    with open('./data/leaderboard.json', 'r') as f:
        data = json.load(f)

        top_users = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}

        first2pairs = {k: top_users[k] for k in list(top_users)[:15]}

        names = ''
        for postion, user in enumerate(first2pairs):
            names += f'{postion+1} - <@!{user}> with {top_users[user]}\n'

        embed = discord.Embed(title="Leaderboard", color=0x3B88C3)
        embed.add_field(name="Names", value=names, inline=False)
        await message.channel.send(embed=embed)   
