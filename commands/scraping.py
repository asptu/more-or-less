from commands.scrape import scrape

async def scraping(message):

    sliced = message.content[8:]
    scrape(sliced)

    await message.reply(f'scraped **{sliced}**')