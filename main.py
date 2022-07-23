import time
import discord
import os
import json
from concatenate import create
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guild_reactions = True
intents.reactions = True

client = discord.Client(intents=intents)

message_id = []
channel_id = []
leaderboard_id = []
leaderboard_channel = []

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$leaderboard'):
        with open('leaderboard.json', 'r') as f:
            data = json.load(f)

        top_users = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}

        names = ''
        for postion, user in enumerate(top_users):
            names += f'{postion+1} - <@!{user}> with {top_users[user]}\n'

        embed = discord.Embed(title="Leaderboard")
        embed.add_field(name="Names", value=names, inline=False)
        leaderboard = await message.channel.send(embed=embed)    
  
    if message.content.startswith('$start'):

        reaction_1 = '⬆️'
        reaction_2 = '⬇️'

        print('creating...')
        create()
        print('done')
        with open('./scores.json') as fp:
            scores = json.load(fp)
            higher = scores['higher'] 
            lower = scores['lower']    

        dt = datetime.now()
        timestamp = int( dt.timestamp() )
        print( timestamp )
        time_left = timestamp + 7

        embed = discord.Embed(title="React with :arrow_up: or :arrow_down:!", description=f"You have <t:{time_left}:R>", color=0x00ff00) #creates embed
        file = discord.File("out.png", filename="out.png")
        embed.set_image(url="attachment://out.png")
        sent_message = await message.channel.send(file=file, embed=embed)

        message_id.clear()
        message_id.append(sent_message.id)

        channel_id.clear()
        channel_id.append(sent_message.channel.id)
           
        # sent_message = await message.channel.send(file=discord.File('out.png'))
        await sent_message.add_reaction(reaction_1) 
        await sent_message.add_reaction(reaction_2) 

        time.sleep(5)
        embed = discord.Embed(title="React with :arrow_up: or :arrow_down:!", description=f"Time's up!", color=0x00ff00) #creates embed
        file = discord.File("done.png", filename="done.png")
        embed.set_image(url="attachment://done.png")
        await sent_message.edit(file=file, embed=embed)


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

                                filename = './leaderboard.json'
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

                                dictObj.update({str(user.id): dictObj[str(user.id)] + higher,})

                                with open(filename, 'w') as json_file:
                                    json.dump(dictObj, json_file, 
                                                        indent=4,  
                                                        separators=(',',': '))
                            
                        elif reaction.emoji == reaction_2:
                            if f'{user}: {reaction_1}' not in ones:
                                twos.add(f'{user}: {reaction.emoji}')
                                #print(f'added {user} to twos')
                                #print(user.name)
                               
                                filename = './leaderboard.json'
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

                                dictObj.update({str(user.id): dictObj[str(user.id)] + lower,})

                                with open(filename, 'w') as json_file:
                                    json.dump(dictObj, json_file, 
                                                        indent=4,  
                                                        separators=(',',': '))

        leaderboard_channel = await client.fetch_channel(1000226480401416254)

        with open('leaderboard.json', 'r') as f:
            data = json.load(f)

        top_users = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}

        names = ''
        for postion, user in enumerate(top_users):
            names += f'{postion+1} - <@!{user}> with {top_users[user]}\n'

        embed = discord.Embed(title="Leaderboard")
        embed.add_field(name="Names", value=names, inline=False)
        leaderboard = await leaderboard_channel.send(embed=embed)
        leaderboard_id.clear()
        leaderboard_id.append(leaderboard.id)     
                                
    if message.content.startswith('$next'):

        print(message_id[0])

        channel = await client.fetch_channel(channel_id[0])
        sent_message = await channel.fetch_message(message_id[0])
        await sent_message.clear_reactions()

        reaction_1 = '⬆️'
        reaction_2 = '⬇️'  

        print('creating...')
        create()
        print('done')
        with open('./scores.json') as fp:
            scores = json.load(fp)
            higher = scores['higher'] 
            lower = scores['lower']  

        dt = datetime.now()
        timestamp = int( dt.timestamp() )
        print( timestamp )
        time_left = timestamp + 7   

        embed = discord.Embed(title="React with :arrow_up: or :arrow_down:!", description=f"You have <t:{time_left}:R>", color=0x00ff00) #creates embed
        file = discord.File("out.png", filename="out.png")
        embed.set_image(url="attachment://out.png")
        await sent_message.edit(file=file, embed=embed)   

        await sent_message.add_reaction(reaction_1) 
        await sent_message.add_reaction(reaction_2)   

        time.sleep(5)
        embed = discord.Embed(title="React with :arrow_up: or :arrow_down:!", description=f"Time's up!", color=0x00ff00) #creates embed
        file = discord.File("done.png", filename="done.png")
        embed.set_image(url="attachment://done.png")
        await sent_message.edit(file=file, embed=embed)


        await message.channel.send('times up!')
        updated_message = await channel.fetch_message(sent_message.id)
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

                                filename = './leaderboard.json'
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

                                dictObj.update({str(user.id): dictObj[str(user.id)] + higher,})

                                with open(filename, 'w') as json_file:
                                    json.dump(dictObj, json_file, 
                                                        indent=4,  
                                                        separators=(',',': '))
                            
                        elif reaction.emoji == reaction_2:
                            if f'{user}: {reaction_1}' not in ones:
                                twos.add(f'{user}: {reaction.emoji}')
                                #print(f'added {user} to twos')
                                #print(user.name)
                               
                                filename = './leaderboard.json'
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

                                dictObj.update({str(user.id): dictObj[str(user.id)] + lower,})

                                with open(filename, 'w') as json_file:
                                    json.dump(dictObj, json_file, 
                                                        indent=4,  
                                                        separators=(',',': '))
                                                        
        leaderboard_channel = await client.fetch_channel(1000226480401416254)
        updated_message = await leaderboard_channel.fetch_message(leaderboard_id[0])

        with open('leaderboard.json', 'r') as f:
            data = json.load(f)

        top_users = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}

        names = ''
        for postion, user in enumerate(top_users):
            names += f'{postion+1} - <@!{user}> with {top_users[user]}\n'

        embed = discord.Embed(title="Leaderboard")
        embed.add_field(name="Names", value=names, inline=False)
        await updated_message.edit(embed=embed) 
                
           

client.run(os.getenv('TOKEN'))