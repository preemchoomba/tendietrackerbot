from discord.ext import commands
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import os

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

def crypto_quote(coin):



    return price

bot.run(DISCORD_TOKEN)