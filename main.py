# Import Commands
from commands.leaderboard import show_leaderboard
from commands.start import game_start
from commands.next import game_next
from commands.leaderboard_channel import lchannel
from commands.extrapoints import set_extrapoints
from commands.scraping import scraping

from http import client
import time
import discord
import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guild_reactions = True
intents.reactions = True

client = discord.Bot(intents=intents)
g_ids = [740886739538673664]

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for $ and slash commands!"))


# Prefix commands

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$leaderboard'):

        print('displaying leaderboard...')
        await show_leaderboard(message)
    
    if message.content.startswith('$start'):

        role = discord.utils.find(lambda r: r.name == 'mol', message.guild.roles)
        if role not in message.author.roles:
            return await message.reply('invalid perms')

        print('starting...')
        await game_start(message)
                                
    if message.content.startswith('$next'):

        role = discord.utils.find(lambda r: r.name == 'mol', message.guild.roles)
        if role not in message.author.roles:
            return await message.reply('invalid perms')

        print('going next...')
        await next(message)

    if message.content.startswith('$lchannel'):

        role = discord.utils.find(lambda r: r.name == 'mol', message.guild.roles)
        if role not in message.author.roles:
            return await message.reply('invalid perms')
        
        print('setting leaderboard channel...')
        await lchannel(message)
        l_message = await message.channel.send(f'Set leaderboard channel to {message.channel.name}')  
        time.sleep(2)
        await l_message.delete()
        await message.delete()
            
    if message.content.startswith('$extrapoints'):

        role = discord.utils.find(lambda r: r.name == 'mol', message.guild.roles)
        if role not in message.author.roles:
            return await message.reply('invalid perms')

        number = message.content[13:]

        print('creating extra points...')
        await set_extrapoints(message, number)
        await message.reply(f'Extrapoints have been set to {number}') 

    if message.content.startswith('$scrape'):

        role = discord.utils.find(lambda r: r.name == 'mol', message.guild.roles)
        if role not in message.author.roles:
            return await message.reply('invalid perms')

        string = message.content[8:]
        print('scraping data...')
        await scraping(message, string)
        await message.reply(f'scraped **{string}**')


# Slash Commands

@client.slash_command(guild_ids=[g_ids[0]], description="Displays the leaderboard.")
async def leaderboard(message):
    await message.respond('Displaying leaderboard:')
    await show_leaderboard(message)

@client.slash_command(guild_ids=[g_ids[0]], description="Starts the game.")
async def start(message):

    role = discord.utils.find(lambda r: r.name == 'mol', message.guild.roles)
    if role not in message.author.roles:
        return await message.respond('invalid perms', ephemeral=True)

    await message.respond('Starting game...', ephemeral=True)
    await game_start(message) 

@client.slash_command(guild_ids=[g_ids[0]], description="Starts another roud.")
async def next(message):

    role = discord.utils.find(lambda r: r.name == 'mol', message.guild.roles)
    if role not in message.author.roles:
        return await message.respond('invalid perms', ephemeral=True)

    await game_next(message)

@client.slash_command(guild_ids=[g_ids[0]], description="Defines the leaderboard channel.")
async def set_channel(message):

    role = discord.utils.find(lambda r: r.name == 'mol', message.guild.roles)
    if role not in message.author.roles:
        return await message.respond('invalid perms', ephemeral=True)

    await lchannel(message)
    await message.respond(f'Set leaderboard channel to {message.channel.name}', ephemeral=True)    

@client.slash_command(guild_ids=[g_ids[0]], description="Adds extrapoints")
async def extrapoints(message, number: discord.Option(int),):

    role = discord.utils.find(lambda r: r.name == 'mol', message.guild.roles)
    if role not in message.author.roles:
        return await message.respond('invalid perms', ephemeral=True)

    await set_extrapoints(message, number)
    await message.respond(f'Extrapoints have been set to {number}', ephemeral=True) 

@client.slash_command(guild_ids=[g_ids[0]], description="Adds extrapoints")
async def scrape(message, string: discord.Option(str),):

    role = discord.utils.find(lambda r: r.name == 'mol', message.guild.roles)
    if role not in message.author.roles:
        return await message.respond('invalid perms', ephemeral=True)

    await scraping(message, string)
    await message.respond(f'Scraped {string}') 



client.run(os.getenv('TOKEN'))