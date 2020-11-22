from discord.ext import commands

class Two(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="twofoo")
    async def foo(self, ctx):
        await ctx.send("two-foo")
    
    @commands.command(name="twobar")
    async def bar(self, ctx):
        await ctx.send("two-bar")

def setup(bot):
    bot.add_cog(Two(bot))
