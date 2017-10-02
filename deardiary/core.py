
import os


def find_project_root():
    """
    This function attempts to find the base directory for the current
    Glue and Stickers project.
    """

    def inner(search=""):
        check = os.path.join(search, ".glue_and_stickers")
        if (os.path.isfile(check)):
            return os.path.abspath(os.path.split(check)[0])
    
        else:
            next = os.path.abspath(os.path.join(search, ".."))
            if next == search:
                print("Cannot find project root.  Are you in the right directory?")
                exit(1)
            else:
                return inner(next)

    return inner()
