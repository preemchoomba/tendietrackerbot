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
    stock = ticker
    tendie = yf.Ticker(stock)
    
    await ctx.send(tendie.history(period='5d'))

bot.run(DISCORD_TOKEN)