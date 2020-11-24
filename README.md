# discordbotdash
A discord.py package for testing Discord bots in your browser and viewing statistics. You can turn commands on and off, see the code for them, and view your shards with their respective latencies. This is still in development and more features will come.

## Screenshots
### Cogs
<img src="../assets/assets/cogs.png" width="300" height="200">

### Commands
<img src="../assets/assets/commands.png" width="300" height="200">

### Shards
<img src="../assets/assets/shards.png" width="300" height="200">

### Console
<img src="../assets/assets/console.png" width="300" height="200">

## Installation
  * PyPi
    1. Run `pip install discordbotdash` for the latest version.

## Usage - Example
Once you have installed it, you can easily open up a dashboard in your browser:
```py
import discord
from discord.ext import commands
import discordbotdash.dash as dbd

bot = commands.AutoShardedBot("!")

@bot.event
async def on_ready():
    dbd.openDash(bot)

bot.run("token")
```
Ensure that you are opening the dashboard before you are running the bot with `bot.run`. Your dashboard will be open on `127.0.0.1:5000` once you have run `openDash`.

## Contributing
  * Pull Requests for new features are always welcome.
  * If you have a suggestion or a bug to report, open an issue.

