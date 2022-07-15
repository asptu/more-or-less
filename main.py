import time
import discord
import os
import json
from score import *  
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guild_reactions = True
intents.reactions = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$leaderboard'):
        with open('score.json', 'r') as f:
            data = json.load(f)

        top_users = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}

        names = ''
        for postion, user in enumerate(top_users):
            names += f'{postion+1} - <@!{user}> with {top_users[user]}\n'

        embed = discord.Embed(title="Leaderboard")
        embed.add_field(name="Names", value=names, inline=False)
        await message.channel.send(embed=embed)    
  
    if message.content.startswith('$start'):
        reaction_1 = '⬆️'
        reaction_2 = '⬇️'

        sent_message = await message.channel.send(file=discord.File('out.png'))
        await sent_message.add_reaction(reaction_1) 
        await sent_message.add_reaction(reaction_2) 

        time.sleep(5)

        await message.channel.send('times up!')
        updated_message = await message.channel.fetch_message(sent_message.id)
        ones = set()
        twos = set()


        for reaction in updated_message.reactions:
            async for user in reaction.users():
                    if not user.bot:

                        if reaction.emoji == reaction_1:
                            if f'{user}: {reaction_2}' not in twos:
                                ones.add(f'{user}: {reaction.emoji}')
                                #print(f'added {user} to ones')
                                #print(user.name)

                                filename = './score.json'
                                dictObj = []
                                
                                with open(filename) as fp:
                                    dictObj = json.load(fp)

                                #print(dictObj)
                                if str(user.id) not in dictObj:
                                  #  print('cannot find')
                                    with open(filename,'r+') as file:
                                            dictObj = json.load(file)
                                            dictObj[str(user.id)] = 0
                                            file.seek(0)
                                            json.dump(dictObj, file, indent = 4)

                                dictObj.update({str(user.id): dictObj[str(user.id)] + reaction1_score,})

                                with open(filename, 'w') as json_file:
                                    json.dump(dictObj, json_file, 
                                                        indent=4,  
                                                        separators=(',',': '))
                            
                        elif reaction.emoji == reaction_2:
                            if f'{user}: {reaction_1}' not in ones:
                                twos.add(f'{user}: {reaction.emoji}')
                                #print(f'added {user} to twos')
                                #print(user.name)
                               
                                filename = './score.json'
                                dictObj = []
                                
                                with open(filename) as fp:
                                    dictObj = json.load(fp)

                                #print(dictObj)
                                if str(user.id) not in dictObj:
                                   # print('cannot find')
                                    with open(filename,'r+') as file:
                                            dictObj = json.load(file)
                                            dictObj[str(user.id)] = 0
                                            file.seek(0)
                                            json.dump(dictObj, file, indent = 4)

                                dictObj.update({str(user.id): dictObj[str(user.id)] + reaction2_score,})

                                with open(filename, 'w') as json_file:
                                    json.dump(dictObj, json_file, 
                                                        indent=4,  
                                                        separators=(',',': '))
                                
                                
                            
        # print(ones)
        # print(twos)

                
           

client.run(os.getenv('TOKEN'))