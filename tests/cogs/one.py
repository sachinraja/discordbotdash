from discord.ext import commands

class One(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="onefoo")
    async def foo(self, ctx):
        await ctx.send("one-foo")

def setup(bot):
    bot.add_cog(One(bot))
