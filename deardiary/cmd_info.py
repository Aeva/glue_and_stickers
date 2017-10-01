
import assets
from cmd_common import register


@register
def info():
    """
    Prints info about the current Glue and Stickers context.
    """

    msg = "Project root: {}\n".format(assets.find_project_root())
    
    print(assets.find_project_root())
    
    current = assets.working_page()
    assorted = assets.all_pages()
    latest = assets.latest_page(assorted)
