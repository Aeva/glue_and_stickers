
import sys
import os.path
import datetime
import weakref
import json


class PageData:
    """
    Page internals.  Not intended to be used directly.
    """
    def __init__(self, page_root):
        self.page_root = page_root
        self.page_path = os.path.join(page_root, "page.html")
        self.meta_path = os.path.join(page_root, "meta.json")
        self.__page_data = None
        self.meta_data = None
        self.load()

    def load(self):
        try:
            with open(self.page_path, "r") as page_file:
                # Just verify that we can open the file for now.
                self.__page_data = True
            with open(self.meta_path, "r") as meta_file:
                self.meta_data = json.load(meta_file)
        except:
            error = " --- Cannot open page:\n - {}\n - \n{}\n"
            print(error.format(self.page_root, sys.exc_info()))

    @property
    def page_data(self):
        # Lazy load the page data.
        if self.__page_data:
            with open(self.page_path, "r") as page_file:
                return page_file.read()
        else:
            return None


class PageAccessor:
    """
    Provides access to page data.
    """
    TIMESTAMP_FORMAT = "%Y:%m:%d:%H:%M"
    PAGE_CACHE = {}

    def __get_or_create(self, page_root):
        if not self.PAGE_CACHE.get(page_root):
            self.PAGE_CACHE[page_root] = PageData(page_root)
        return weakref.ref(self.PAGE_CACHE.get(page_root))

    def __init__(self, page_path):
        assert(os.path.exists(page_path))
        if os.path.isfile(page_path):
            page_path = os.path.split(page_path)[0]
        self.__inner = self.__get_or_create(page_path)

    def __eq__(self, other):
        self.__inner() == other.__inner()

    def __repr__(self):
        if self.is_valid:
            if self.is_published:
                return "<Page: {}>".format(self.slug)
            else:
                return "<Page WIP: {}>".format(self.slug)
        else:
            return "<Invalid Page>"

    @property
    def page_root(self):
        wrapped = self.__inner()
        return wrapped.page_root if wrapped else None

    @property
    def page_data(self):
        wrapped = self.__inner()
        return wrapped.page_data if wrapped else None

    @property 
    def meta_data(self):
        wrapped = self.__inner()
        return wrapped.meta_data if wrapped else None

    @property
    def is_valid(self):
        return self.page_data is not None and self.meta_data is not None

    @property
    def is_published(self):
        # A page is considered to be published if it is valid, and has
        # a fixed date stamp in its metadata.
        return self.is_valid and self.meta_data.get("date")

    @property
    def date_stamp(self):
        if self.is_published:
            return datetime.datetime.strptime(
                self.meta_data.get("date"), self.TIMESTAMP_FORMAT)
        else:
            # Use the current time for unpublished or invalid pages.
            return datetime.now()

    @property
    def slug(self):
        return os.path.split(self.page_root)[1]

    @property
    def tags(self):
        if is_valid():
            return self.meta_data.get("tags") or tuple()
        else:
            return tuple()

    @property
    def extends(self):
        if is_valid():
            return self.meta_data.get("extends") or tuple()
        else:
            return tuple()
