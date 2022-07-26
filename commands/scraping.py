import discord   
from scrape import scrape

async def scraping(message):
    role = discord.utils.find(lambda r: r.name == 'mol', message.guild.roles)
    if role not in message.author.roles:
        return await message.reply('invalid perms')
    sliced = message.content[8:]
    scrape(sliced)

    await message.reply(f'scraped **{sliced}**')