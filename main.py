from http import client
import time
import discord
import os

# Import Commands
from commands.leaderboard import show_leaderboard
from commands.start import game_start
from commands.next import game_next
from commands.leaderboard_channel import lchannel
from commands.extrapoints import extrapoints
from commands.scraping import scraping


from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guild_reactions = True
intents.reactions = True

client = discord.Bot(intents=intents)



@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


# Prefix commands

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$leaderboard'):
        print(message)
        print('displaying leaderboard...')
        await show_leaderboard(message)
    
    if message.content.startswith('$start'):
        print('starting...')
        await game_start(message)
                                
    if message.content.startswith('$next'):
        print('going next...')
        await next(message)

    if message.content.startswith('$lchannel'):
        print('setting leaderboard channel...')
        await lchannel(message)
        l_message = await message.channel.send(f'Set leaderboard channel to {message.channel.name}')  
        time.sleep(2)
        await l_message.delete()
        await message.delete()
            
    if message.content.startswith('$extrapoints'):
        print('creating extra points...')
        await extrapoints(message)

    if message.content.startswith('$scrape'):
        print('scraping data...')
        await scraping(message)


# Slash Commands

@client.slash_command(guild_ids=[740886739538673664], description="Displays the leaderboard.")
async def leaderboard(message):
    print(message)
    await show_leaderboard(message)
    await message.respond('Displaying leaderboard:')

@client.slash_command(guild_ids=[740886739538673664], description="Starts the game.")
async def start(message):
    await message.respond('Starting game...', ephemeral=True)
    await game_start(message) 

@client.slash_command(guild_ids=[740886739538673664], description="Starts another roud.")
async def next(message):
    await game_next(message)

@client.slash_command(guild_ids=[740886739538673664], description="Defines the leaderboard channel.")
async def set_channel(message):
    await lchannel(message)
    await message.respond(f'Set leaderboard channel to {message.channel.name}', ephemeral=True)    


client.run(os.getenv('TOKEN'))