
COMMANDS = {}
HELP_TEXT = {}


def register(name, help_text):
    def decorator(callback):
        global COMMANDS
        global HELP_TEXT
        COMMANDS[name] = callback
        HELP_TEXT[name] = help_text
    return decorator


def run_command(name="help", *params):
    global COMMANDS
    callback = COMMANDS.get(name, *params)
    if callback:
        callback()
    else:
        COMMANDS["help"]()
