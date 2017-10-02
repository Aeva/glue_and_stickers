
import os
from glob import glob
from core import find_project_root
from page import access_page


def working_page():
    if glob("page.html"):
        page = access_page(os.getcwd())
        return page
    else:
        return None


def assorted_pages():
    root = find_project_root()
    search = os.path.join(root, "**", "page.html")
    for page_path in glob(search, recursive=True):
        page = access_page(page_path)
        if page.is_valid:
            yield page


def query_pages(matcher, sort_key=None, page_set=None):
    if page_set:
        return sorted(
            [page for page in page_set if matcher(page)],
            key=sort_key)
    else:
        return sorted(
            [page for page in assorted_pages() if matcher(page)],
            key=sort_key)


def valid_pages(page_set=None):
    return query_pages(
        lambda p: p.is_valid, lambda p: p.datetime, page_set)


def invalid_pages(page_set=None):
    return query_pages(
        lambda p: not p.is_valid, lambda p: p.datetime, page_set)


def published_pages(page_set=None):
    return query_pages(
        lambda p: p.is_published, lambda p: p.datetime, page_set)


def secret_pages(page_set=None):
    return query_pages(
        lambda p: not p.is_published, lambda p: p.datetime, page_set)
