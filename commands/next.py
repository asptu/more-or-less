
import discord
import json
from concatenate import create
from datetime import datetime
import time


async def game_next(message):
    role = discord.utils.find(lambda r: r.name == 'mol', message.guild.roles)
    if role not in message.author.roles:
        return await message.reply('invalid perms')

    with open('commands/message_data.json', 'r+') as f:
            data = json.load(f)

    await message.delete()
    channel = await message.guild.fetch_channel(data['channel_id'])
    sent_message = await channel.fetch_message(data['message_id'])
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
    with open('commands/message_data.json', 'r+') as f:
        data = json.load(f)

    lchannel = await message.guild.fetch_channel(data['leaderboard_channel_id'])
    updated_message = await lchannel.fetch_message(data['leaderboard_message_id'])

    with open('leaderboard.json', 'r') as f:
        data = json.load(f)

    top_users = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}

    names = ''
    for postion, user in enumerate(top_users):
        names += f'{postion+1} - <@!{user}> with {top_users[user]}\n'

    embed = discord.Embed(title="Leaderboard", color=0x3B88C3)
    embed.add_field(name="Names", value=names, inline=False)
    await updated_message.edit(embed=embed) 