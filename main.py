from multiprocessing.connection import wait
import time
import discord
import os
import json
from concatenate import create
from scrape import update
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

        embed = discord.Embed(title="Leaderboard", color=0x3B88C3)
        embed.add_field(name="Names", value=names, inline=False)
        leaderboard = await message.channel.send(embed=embed)    
  
    if message.content.startswith('$start'):

        role = discord.utils.find(lambda r: r.name == 'mol', message.guild.roles)
        if role not in message.author.roles:
            return await message.reply('invalid perms')

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
        timestamp = int(dt.timestamp())
        time_left = timestamp + 9

        embed = discord.Embed(title="React with :arrow_up: or :arrow_down:!", description=f"Finished <t:{time_left}:R>!", color=0x3B88C3) #creates embed
        file = discord.File("out.png", filename="out.png")
        embed.set_image(url="attachment://out.png")
        sent_message = await message.channel.send(file=file, embed=embed)

        message_id.clear()
        message_id.append(sent_message.id)

        channel_id.clear()
        channel_id.append(sent_message.channel.id)
           
        await sent_message.add_reaction(reaction_1) 
        await sent_message.add_reaction(reaction_2)

        time.sleep(5)
        embed = discord.Embed(title="React with :arrow_up: or :arrow_down:!", description=f"Time's up!", color=0x3B88C3) #creates embed
        file = discord.File("done.png", filename="done.png")
        embed.set_image(url="attachment://done.png")
        await sent_message.edit(file=file, embed=embed)


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


        lchannel = await client.fetch_channel(leaderboard_channel[0])

        with open('leaderboard.json', 'r') as f:
            data = json.load(f)

        top_users = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}

        names = ''
        for postion, user in enumerate(top_users):
            names += f'{postion+1} - <@!{user}> with {top_users[user]}\n'

        embed = discord.Embed(title="Leaderboard", color=0x3B88C3)
        embed.add_field(name="Names", value=names, inline=False)
        leaderboard = await lchannel.send(embed=embed)
        leaderboard_id.clear()
        leaderboard_id.append(leaderboard.id)     
                                
    if message.content.startswith('$next'):
        role = discord.utils.find(lambda r: r.name == 'mol', message.guild.roles)
        if role not in message.author.roles:
            return await message.reply('invalid perms')

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
        time_left = timestamp + 9   

        embed = discord.Embed(title="React with :arrow_up: or :arrow_down:!", description=f"Finished <t:{time_left}:R>!", color=0x3B88C3) #creates embed
        file = discord.File("out.png", filename="out.png")
        embed.set_image(url="attachment://out.png")
        await sent_message.edit(file=file, embed=embed)   

        await sent_message.add_reaction(reaction_1) 
        await sent_message.add_reaction(reaction_2)   

        time.sleep(5)
        embed = discord.Embed(title="React with :arrow_up: or :arrow_down:!", description=f"Time's up!", color=0x3B88C3) #creates embed
        file = discord.File("done.png", filename="done.png")
        embed.set_image(url="attachment://done.png")
        await sent_message.edit(file=file, embed=embed)

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
                                                        
        lchannel = await client.fetch_channel(leaderboard_channel[0])
        updated_message = await lchannel.fetch_message(leaderboard_id[0])

        with open('leaderboard.json', 'r') as f:
            data = json.load(f)

        top_users = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}

        names = ''
        for postion, user in enumerate(top_users):
            names += f'{postion+1} - <@!{user}> with {top_users[user]}\n'

        embed = discord.Embed(title="Leaderboard", color=0x3B88C3)
        embed.add_field(name="Names", value=names, inline=False)
        await updated_message.edit(embed=embed) 

    if message.content.startswith('$lchannel'):
        role = discord.utils.find(lambda r: r.name == 'mol', message.guild.roles)
        if role not in message.author.roles:
            return await message.reply('invalid perms')
        leaderboard_channel.clear()
        leaderboard_channel.append(message.channel.id)
        l_message = await message.channel.send(f'Set leaderboard channel to {message.channel.name}')  
        time.sleep(2)
        await l_message.delete()
        await message.delete()
        

    if message.content.startswith('$extrapoints'):
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

    if message.content.startswith('$update'):
        role = discord.utils.find(lambda r: r.name == 'mol', message.guild.roles)
        if role not in message.author.roles:
            return await message.reply('invalid perms')
        sliced = message.content[8:]
        update(sliced)

        await message.reply(f'updated {sliced}')



client.run(os.getenv('TOKEN'))