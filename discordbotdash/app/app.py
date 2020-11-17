from flask import Flask, request, url_for, redirect, render_template
import threading
import inspect

app = Flask(__name__)
bot = None
all_commands = None
disabled_commands = []
command_prefix = None

def startApp(init_bot):
    global bot
    global all_commands
    global command_prefix

    bot = init_bot
    # save initial copy to easily modify bot commands list
    all_commands = bot.commands.copy()
    
    command_prefix = bot.command_prefix

    # if command_prefix is function
    if inspect.isfunction(bot.command_prefix):
        command_prefix = f"<Function> {bot.command_prefix.__name__}"

    # start on separate thread so it does not block bot
    threading.Thread(target=app.run).start()

@app.route("/")
def render_static():
    return redirect("/commands")

@app.route("/commands", methods=["GET", "POST"])
def commands():
    if request.method == "POST":
        # commands form
        if request.form["formName"] == "commands":
            
            cmds = [item[0] for item in request.form.items()]

            # disable command
            for cmd in bot.commands:
                if cmd.name not in cmds:
                    print(f"Disabled {cmd.name}")
                    # remove command and add to disabled
                    bot.remove_command(cmd.name)
                    disabled_commands.append(cmd)
            
            # enable command
            for cmd in cmds:
                if cmd in [disabled_cmd.name for disabled_cmd in disabled_commands]:
                    # search for command and add if ticked on
                    for command in all_commands:
                        if command.name == cmd:
                            print(f"Enabled {cmd}")
                            # add command back and remove from disabled
                            bot.add_command(command)
                            disabled_commands.remove(command)
        
        # clear form
        return redirect(url_for("commands"))
    
    return render_template("commands.html", getsource=inspect.getsource, bot=bot, command_prefix=command_prefix, enabled_commands=bot.commands, disabled_commands=disabled_commands)

@app.route("/shards", methods=["GET", "POST"])
def shards():
    if request.method == "POST":
        # clear form
        return redirect(url_for("shards"))
    
    return render_template("shards.html", bot=bot, command_prefix=command_prefix)
