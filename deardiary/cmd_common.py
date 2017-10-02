
COMMANDS = {}


def register(callback):
    global COMMANDS
    COMMANDS[callback.__name__] = callback
    return callback


def run_command(name="help", *params):
    global COMMANDS
    callback = COMMANDS.get(name)
    if callback:
        callback(*params)
    else:
        COMMANDS["help"]()
