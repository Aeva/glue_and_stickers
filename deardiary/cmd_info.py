
import assets
from cmd_common import register


help_text = \
"""
Prints info about the current Glue and Stickers context.
"""            

@register("info", help_text)
def debug_info():
    print(assets.find_project_root())
