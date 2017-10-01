
COMMANDS = {}


def register(callback):
    global COMMANDS
    COMMANDS[callback.__name__] = callback
    return callback


def run_command(name="help", *params):
    global COMMANDS
    callback = COMMANDS.get(name, *params)
    if callback:
        callback()
    else:
        COMMANDS["help"]()
