
COMMANDS = {}


def register(name, callback):
    global COMMANDS
    COMMANDS[name] = callback


def run_command(name="help", *params):
    global COMMANDS
    callback = COMMANDS.get(name, *params)
    if callback:
        callback()
    else:
        COMMANDS["help"]()
