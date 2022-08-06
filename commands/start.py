
import discord
import json
from commands.concatenate import create, create2
from datetime import datetime
import time

async def game_start(message):  

    reaction_1 = '⬆️'
    reaction_2 = '⬇️'

    print('creating...')
    im1, im2, im1_name, im2_name, im1_results, im2_results = create()
    print('done')
    with open('./data/scores.json') as fp:
        scores = json.load(fp)
        higher = scores['higher'] 
        lower = scores['lower'] 
        time_set = scores['time']


    dt = datetime.now()
    timestamp = int(dt.timestamp())
    time_left = timestamp + time_set + 4

    embed = discord.Embed(title=f"Does {im2_name} have  {reaction_1}  or  {reaction_2}  results?", description=f"Finished <t:{time_left}:R>!", color=0x3B88C3) 
    file = discord.File("export/out.png", filename="out.png")
    embed.set_image(url="attachment://out.png")
    sent_message = await message.channel.send(file=file, embed=embed)


    with open('commands/message_data.json', 'r+') as f:
            data = json.load(f)
            data['message_id'] = sent_message.id
            data['channel_id'] = sent_message.channel.id
            f.seek(0)        
            json.dump(data, f, indent=4)
            f.truncate() 
    
    await sent_message.add_reaction(reaction_1) 
    await sent_message.add_reaction(reaction_2)
    
    create2(im1, im2, im1_name, im2_name, im1_results, im2_results)

    time.sleep(time_set)
    embed = discord.Embed(title=f"Does {im2_name} have  {reaction_1}  or  {reaction_2}  results?", description=f"Time's up!", color=0x3B88C3) 
    file = discord.File("export/done.png", filename="done.png")
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


                            filename = './data/leaderboard.json'
                            dictObj = []
                            
                            with open(filename) as fp:
                                dictObj = json.load(fp)


                            if str(user.id) not in dictObj:
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

                        
                            filename = './data/leaderboard.json'
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
   
    with open('commands/message_data.json', 'r+') as f:
        data = json.load(f)
        lchannel = await message.guild.fetch_channel(data['leaderboard_channel_id'])

    with open('./data/leaderboard.json', 'r') as f:
        data = json.load(f)

    top_users = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}

    first2pairs = {k: top_users[k] for k in list(top_users)[:15]}

    names = ''
    for postion, user in enumerate(first2pairs):
        names += f'{postion+1} - <@!{user}> with {top_users[user]}\n'

    embed = discord.Embed(title="Leaderboard", color=0x3B88C3)
    embed.add_field(name="Names", value=names, inline=False)
    leaderboard = await lchannel.send(embed=embed)
    with open('commands/message_data.json', 'r+') as f:
        data = json.load(f)
        data['leaderboard_message_id'] = leaderboard.id
        f.seek(0)        
        json.dump(data, f, indent=4)
        f.truncate() 

     