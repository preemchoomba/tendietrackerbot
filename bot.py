import os

import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(verbose=True)
DISCORD_TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('TendieTracker online!')

@bot.command()
async def stock(ctx, ticker):
    await ctx.send(stock_quote(ticker))

#scrapes CNN market stock pricing
def stock_quote(ticker):
    
    url = "https://money.cnn.com/quote/quote.html?symb=" + ticker
    
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')

    price = soup.find_all('span')[2].get_text()

    return price 

def crypto_quote(query):
    try:
        store = query.split(':')

        coin = store[0]

        currency = store[1]

        url = 'https://query1.finance.yahoo.com/v7/finance/quote?&symbols=' \
            + coin \
            + '-' \
            + currency

        page = requests.get(url)

        soup = BeautifulSoup(page.text, 'html.parser')

        coin_json = json.loads(soup.text)

        price = coin_json['quoteResponse']['result'][0]['regularMarketPrice']
        if price == None:
            return "No pricing information for that pair."

        return price
    except IndexError:
        print("Coin or currency pair price information doesn't exist. Use <cointicker>:<currency> ex. BTC:USD")
    except KeyError:
        print("Coin or currency pair price information doesn't exist. Use <cointicker>:<currency> ex. BTC:USD")
    except Exception as e:
        print(repr(e))

bot.run(DISCORD_TOKEN)
