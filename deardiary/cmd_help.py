from cmd_common import register


def usage_message():
    print(\
"""Glue and Stickers commands:

$ deardiary init site_name
Creates a new Glue and Stickers project in the current directory.

$ deardiary refresh
Regenerates static serve files.

$ deardiary info
Prints info about the current Glue and Stickers context.

$ deardiary serve [port]
Serves the site locally for preview.
""")

register("help", usage_message)
