
import inspect
from cmd_common import register
from cmd_common import COMMANDS


# @register("help", None)
# def help():
#     print(\
# """Glue and Stickers commands:

# $ deardiary init site_name
# Creates a new Glue and Stickers project in the current directory.

# $ deardiary refresh
# Regenerates static serve files.

# $ deardiary info
# Prints info about the current Glue and Stickers context.

# $ deardiary serve [port]
# Serves the site locally for preview.
# """)


@register
def help():
    commands = [i for i in COMMANDS.keys()]
    commands.sort()
    messages = []
    pattern = "$ deardiary {} {}\n{}"
    for command in commands:
        function = COMMANDS.get(command)

        if not function.__doc__:
            continue
        lines = function.__doc__.split("\n")
        reflow = [line for line in map(str.strip, lines) if line]
        help_text = "\n".join(reflow)

        arguments = " ".join(inspect.getargspec(function)[0])
        message = pattern.format(command, arguments, help_text)
        messages.append(message)

    print("\n\n".join(messages) + "\n")
