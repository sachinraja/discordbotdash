from flask import Flask, request, url_for, redirect, render_template
import threading
import inspect

# disable POST and GET messages
import logging
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

app = Flask(__name__)
bot = None
command_prefix = None

disabled_cogs = {}
disabled_commands = []

def startApp(init_bot):
    
    global bot
    global command_prefix
    
    bot = init_bot

    # save initial copies to easily modify bot lists
    command_prefix = bot.command_prefix

    # if command_prefix is function
    if inspect.isfunction(bot.command_prefix):
        command_prefix = f"<Function> {bot.command_prefix.__name__}"

    # start on separate thread so it does not block bot
    threading.Thread(target=app.run).start()

@app.route("/")
def render_static():
    return redirect("/commands")

@app.route("/cogs", methods=["GET", "POST"])
def cogs():
    if request.method == "POST":
        checkbox_cogs = [item[0] for item in request.form.items()]

        # disable cog
        # copy to prevent size from changing during iteration
        for cog_name, cog in bot.cogs.copy().items():
            if cog_name not in checkbox_cogs:
                # add cog's commands to disabled commands
                for command in cog.__cog_commands__:
                    if command not in disabled_commands:
                        disabled_commands.append(command)
                
                # remove cog and add to disabled
                disabled_cogs[cog_name] = cog
                bot.remove_cog(cog_name)
                print(f"Disabled cog {cog_name}")
        
        # enable cog
        for cog in checkbox_cogs:
            if cog in disabled_cogs.keys():
                # remove commands from disabled_commands
                for cmd in disabled_cogs[cog].__cog_commands__:
                    if cmd in disabled_commands:
                        disabled_commands.remove(cmd)
                    
                    # remove command if it already exists before the cog is added
                    if cmd.name in [command.name for command in bot.commands]:
                        bot.remove_command(cmd.name)
                
                # search for extension and add if ticked on
                # add extension back and remove from disabled
                bot.add_cog(disabled_cogs[cog]) 
                del disabled_cogs[cog]
                print(f"Enabled cog {cog}")

        return redirect(url_for("cogs"))
    
    return render_template("cogs.html", bot=bot, command_prefix=command_prefix, enabled_cogs=bot.cogs.items(), disabled_cogs=disabled_cogs.items())

@app.route("/commands", methods=["GET", "POST"])
def commands():
    if request.method == "POST":
        # commands form
        if request.form["formName"] == "commands":
            
            checkbox_cmds = [item[0] for item in request.form.items()]

            # disable command
            for cmd in bot.commands:
                if cmd.name not in checkbox_cmds:
                    # remove command and add to disabled
                    bot.remove_command(cmd.name)
                    disabled_commands.append(cmd)
                    print(f"Disabled command {cmd.name}")
            
            # enable command
            for cmd in checkbox_cmds:
                # search for command and add if ticked on
                for disabled_cmd in disabled_commands:
                    if cmd == disabled_cmd.name:
                        # add command back and remove from disabled
                        bot.add_command(disabled_cmd)
                        disabled_commands.remove(disabled_cmd)
                        print(f"Enabled command {cmd}")
        
        # clear form
        return redirect(url_for("commands"))
    
    return render_template("commands.html", getsource=inspect.getsource, bot=bot, command_prefix=command_prefix, enabled_commands=bot.commands, disabled_commands=disabled_commands)

@app.route("/shards", methods=["GET", "POST"])
def shards():
    if request.method == "POST":
        return redirect(url_for("shards"))
    
    return render_template("shards.html", bot=bot, command_prefix=command_prefix)
