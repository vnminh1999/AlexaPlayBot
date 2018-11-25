from botconfig import bot_token
import urllib.request
from bs4 import BeautifulSoup
import discord
import asyncio

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    msg_tokens = message.content.split(' ')
    if message.content.startswith('alexa help'):
        msg = "Alexa guide:\n"
        msg = msg + "`alexa play <song title>` - plays the song specified\n"
        msg = msg + "`alexa help` to display this\n"

        await client.send_message(message.channel, msg)

    elif message.content.startswith('alexa play'):
        if(len(msg_tokens) > 2):
            quote_page = 'https://www.youtube.com/results?search_query='
            for str in msg_tokens[2:]:
                quote_page = quote_page + str + "+"

            quote_page = quote_page[:-1]

            page = urllib.request.urlopen(quote_page)
            soup = BeautifulSoup(page, 'html.parser')
            yt_links = soup.find_all("a", class_ = "yt-uix-tile-link")

            yt_href = yt_links[0].get("href")
            yt_title = yt_links[0].get("title")
            msg = "Now Playing: " + yt_title + "\n"
            if(yt_href.find("googleads") == -1):
                msg = msg + "https://www.youtube.com" + yt_href + "\n"
            else:
                msg = msg + yt_href + "\n"
        else:
            msg = "Alexa needs a song title\n"

        await client.send_message(message.channel, msg)

client.run(bot_token)
