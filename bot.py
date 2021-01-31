from discord.ext import commands
from dotenv import load_dotenv
import yfinance as yf
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

#uses external libraries to fetch stock price.
def stock_quote(ticker):

    stock = ticker
    tendie = yf.Ticker(stock)
    quote = tendie.history(period='5d')

    return quote

bot.run(DISCORD_TOKEN)