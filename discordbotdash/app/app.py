from flask import Flask, request, url_for, redirect, render_template
import threading
import inspect

# disable POST and GET messages
import logging
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

# add timestamp to console messages
import datetime

app = Flask(__name__)
bot = None
command_prefix = None

disabled_cogs = {}
disabled_commands = []

# console-related variables
console_help_text = \
"help - Display list of commands (this message).\n\
cls - Clear console text.\n\
eval [expression] - Run eval() on expression and display output.\n"

# begin with list of commands
console_text = ""

def console_log(message):
    global console_text
    # format timestamp add add to each console message
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # add timestamp at beginning and line break at end
    console_text += f"[{timestamp}] {message}\n"

def startApp(init_bot):
    
    global bot
    global command_prefix
    
    bot = init_bot

    # save initial copies to easily modify bot lists
    command_prefix = bot.command_prefix

    # if command_prefix is function
    if inspect.isfunction(bot.command_prefix):
        command_prefix = f"<Function> {bot.command_prefix.__name__}"

    # add help to console at start
    console_log(console_help_text)

    # start on separate thread so it does not block bot
    threading.Thread(target=app.run).start()

@app.route("/")
def render_static():
    return redirect(url_for("commands"))

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
                console_log(f"Disabled cog {cog_name}")
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
                
                # search for cog and add if ticked on
                # add cog back and remove from disabled
                bot.add_cog(disabled_cogs[cog]) 
                del disabled_cogs[cog]
                console_log(f"Enabled cog {cog}")
                print(f"Enabled cog {cog}")

        # clear form
        return redirect(url_for("cogs"))
    
    return render_template("cogs.html", bot=bot, command_prefix=command_prefix, getfile=inspect.getfile, enabled_cogs=bot.cogs.items(), disabled_cogs=disabled_cogs.items())

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
                    console_log(f"Disabled command {cmd.name}")
                    print(f"Disabled command {cmd.name}")
            
            # enable command
            for cmd in checkbox_cmds:
                # search for command and add if ticked on
                for disabled_cmd in disabled_commands:
                    if cmd == disabled_cmd.name:
                        # add command back and remove from disabled
                        bot.add_command(disabled_cmd)
                        disabled_commands.remove(disabled_cmd)
                        console_log(f"Enabled command {cmd}")
                        print(f"Enabled command {cmd}")
        
        
        return redirect(url_for("commands"))
    
    return render_template("commands.html", getsource=inspect.getsource, bot=bot, command_prefix=command_prefix, enabled_commands=bot.commands, disabled_commands=disabled_commands)

@app.route("/shards", methods=["GET", "POST"])
def shards():
    if request.method == "POST":
        return redirect(url_for("shards"))
    
    # get bot latencies if it is sharded, else get the bot's only latency
    latencies = None
    if hasattr(bot, "latencies"):
        latencies = bot.latencies
    else:
        latencies = [(0, bot.latency)]
    
    return render_template("shards.html", bot=bot, command_prefix=command_prefix, latencies=latencies)

@app.route("/console", methods=["GET", "POST"])
def console():
    if request.method == "POST":
        if request.form["formName"] == "execute":
            # get text from input box and log it to the console
            text = request.form["txtExecute"].strip()
            text_list = text.split()
            command = text_list[0]
            
            # get arguments if possible
            if len(text_list) > 1:
                arguments = text_list[1:]
            
            if command == "help":
                console_log(console_help_text)

            # clear console of text
            elif command == "cls":
                global console_text
                console_text = ""
            
            elif command == "eval":
                # +1 to not include space after command
                rest_of_text = text[len(command)+1:]

                try:
                    output = eval(rest_of_text)
                except Exception as e:
                    output = e
                
                console_log(f"Evaluated {rest_of_text}: {output}")
            
            else:
                console_log(f"{command} is not a command.")
        
        return redirect(url_for("console"))
    
    return render_template("console.html", bot=bot, command_prefix=command_prefix, console_text=console_text)