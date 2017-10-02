
import os
from glob import glob
import assets
from cmd_common import register


@register
def find(asset):
    """
    Find a named asset.  When called from a page's directory, this
    will list the best match in the page's search tree.  When called
    elsewhere, this command just lists all occurances of the named
    asset in the project.
    """

    def munge(path):
        return os.path.relpath(os.path.abspath(path), root)

    root = assets.find_project_root()
    page = assets.working_page()
    
    if page:
        found = page.find(asset)
        if found:
            print(munge(found))

    else:
        found = map(
            munge, glob(os.path.join(root, "**", asset), recursive=True))

        if found:
            for path in sorted(found):
                print(path)
