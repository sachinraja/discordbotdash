import discord
from discord.ext import commands
import discordbotdash.dash as dbd

# load from env
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.environ["TOKEN"]

bot = commands.AutoShardedBot("b!")

@bot.command()
async def hi(ctx):
    """Says hi"""
    await ctx.send("Hi!")

@bot.command()
async def bye(ctx):
    """Says bye"""
    await ctx.send("Bye!")

@bot.command()
async def morning(ctx):
    """Says morning"""
    await ctx.send("Good morning!")

@bot.command()
async def afternoon(ctx):
    """Says afternoon"""
    await ctx.send("Good afternoon!")

@bot.command()
async def evening(ctx):
    """Says evening"""
    await ctx.send("Good evening!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} | {bot.user.id}")
    dbd.openDash(bot)

bot.run(TOKEN)