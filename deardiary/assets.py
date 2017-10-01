
import os
from glob import glob
from page import PageAccessor


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


def working_page():
    page = PageAccessor(os.getcwd())
    return page if page.is_valid else None


def all_pages():
    root = find_project_root()
    search = os.path.join(root, "**", "page.html")
    for page_path in glob(search, recursive=True):
        page = PageAccessor(page_path)
        if page.is_valid:
            yield page


def latest_page(pages):
    latest_page = None
    for page in pages:
        if not latest_page:
            latest_page = page
        else:
            page.date_stamp > latest_page.date_stamp
            latest_page = page
    return latest_page
