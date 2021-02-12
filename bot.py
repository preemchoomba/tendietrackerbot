import json
import os

import discord
import requests
from bs4 import BeautifulSoup
from discord import message
from discord.ext import commands
from discord.guild import Guild
from dotenv import load_dotenv

# use environment file for token key
load_dotenv(verbose=True)
DISCORD_TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("TendierTracker online")
    
@bot.command()
async def stock(ctx, ticker):
    id = ctx.guild.id
    name = ctx.guild.name
    print("stock:" + ticker + ":" + name + ":" + str(id))
    await ctx.channel.send(stock_quote(ticker))

@bot.command()
async def crypto(ctx, pair):
    id = ctx.guild.id
    name = ctx.guild.name
    print("crypto:" + pair + ":" + name + ":" + str(id))
    await ctx.channel.send(crypto_quote(pair))


# scrapes CNN market stock pricing
def stock_quote(ticker):
    
    source = "https://money.cnn.com/quote/quote.html?symb="

    url = source + ticker
    
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')

    price = soup.find_all('span')[2].get_text()

    return price 

def crypto_quote(query):
    try:
        # split query coin:currency pair into variables for URL
        store = query.split(':')

        coin = store[0]

        currency = store[1]

        # use formatted command for URL query.
        url = 'https://query1.finance.yahoo.com/v7/finance/quote?&symbols=' \
            + coin \
            + '-' \
            + currency

        # get request for url above through requests library.
        page = requests.get(url)

        # create the soup from the get request above.
        soup = BeautifulSoup(page.text, 'html.parser')

        # load JSON API response for scraping.
        coin_json = json.loads(soup.text)

        # pulling text out of json for crypto regular price
        price = coin_json['quoteResponse']['result'][0]['regularMarketPrice']
        if price == None:
            return "No pricing information for that pair."

        return price

    # catch errors related to API calls failing.
    except IndexError:
        print("Coin or currency pair price information doesn't exist. Use <cointicker>:<currency> ex. BTC:USD")

    except KeyError:
        print("Coin or currency pair price information doesn't exist. Use <cointicker>:<currency> ex. BTC:USD")

    except Exception as e:
        print(repr(e))

bot.run(DISCORD_TOKEN)
