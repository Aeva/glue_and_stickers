
from os import path


def find_project_root(search=""):
    """
    This function attempts to find the base directory for the current
    Glue and Stickers project.
    """

    check = path.join(search, ".glue_and_stickers")
    if (path.isfile(check)):
        return path.abspath(path.split(check)[0])
    
    else:
        next = path.abspath(path.join(search, ".."))
        if next == search:
            raise Exception("Cannot find project root.")
        else:
            find_project_root(next)
