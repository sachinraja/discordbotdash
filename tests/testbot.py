import discord
from discord.ext import commands
import discordbotdash.app.dash as dbd
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.environ["TOKEN"]
print(TOKEN)
bot = commands.AutoShardedBot("b!")

@bot.command()
async def hi(ctx):
    """Says hi"""
    await ctx.send("hi")

@bot.command()
async def bye(ctx):
    """See ya"""
    await ctx.send("bye")

@bot.command()
async def morning(ctx):
    """Says morning"""
    await ctx.send("g'day to you sir")

@bot.command()
async def afternoon(ctx):
    """Says afternoon"""
    await ctx.send("g'afternoon to you sir")

@bot.command()
async def evening(ctx):
    """Says evening"""
    await ctx.send("g'evening to you sir")

@bot.command()
async def fortnite(ctx):
    await ctx.send(f"{ctx.author}'s stats: Good!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} | {bot.user.id}")
    dbd.openDash(bot)

bot.run(TOKEN)