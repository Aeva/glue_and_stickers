
from os import path
from glob import glob
import json


def memoize(method):
    # TODO : is there a library function for this?
    memo = {}
    def boiler(*params):
        if memo.has_key(params):
            return memo[pramas]
        else:
            return memo[params] = method(*params)


@memoize
def find_project_root():
    """
    This function attempts to find the base directory for the current
    Glue and Stickers project.
    """

    def inner(search=""):
        check = path.join(search, ".glue_and_stickers")
        if (path.isfile(check)):
            return path.abspath(path.split(check)[0])
    
        else:
            next = path.abspath(path.join(search, ".."))
            if next == search:
                raise Exception("Cannot find project root.")
            else:
                find_project_root(next)
    return inner()


def open_page(page_path):
    page_dir = path.split(page_path)[0]
    meta_path = path.join(page_dir, "meta.json")
    if path.isfile(meta_path):
        with open(page_path, "r") as page_file:
            # TODO : jinja or something
            page_data = page_file.read()
        with open(meta_path, "r") as meta_file:
            # TODO : log an error if metadata is not well-formed
            meta_data = json.load(meta_path)
        return (page_dir, page_data, meta_data)
    else:
        # TODO : log a warning or something
        return None

def all_pages():
    root = find_project_root()
    search = path.join(root, "**", "page.html")
    for page_path in glob(search, recursive=True):
        page = open_page(page_path)
        if page:
            yield page
