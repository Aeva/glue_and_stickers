
import assets
from cmd_common import register


@register
def info():
    """
    Prints info about the current Glue and Stickers context.
    """           
    print(assets.find_project_root())
