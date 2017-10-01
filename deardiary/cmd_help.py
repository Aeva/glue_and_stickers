
import inspect
from cmd_common import register
from cmd_common import COMMANDS, HELP_TEXT


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


@register("help", None)
def help():
    commands = [i for i in HELP_TEXT.keys()]
    commands.sort()
    messages = []
    pattern = "$ deardiary {} {}\n{}"
    for command in commands:
        help_text = HELP_TEXT.get(command)
        if not help_text:
            continue

        function = COMMANDS.get(command)
        arguments = " ".join(inspect.getargspec(function)[0])
        message = pattern.format(command, arguments, help_text.strip())
        messages.append(message)

    print("\n\n".join(messages) + "\n")
