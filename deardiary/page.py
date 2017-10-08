
import os
import sys
import json
from datetime import datetime
from core import find_project_root

import jinja2


class PowerLoader(jinja2.BaseLoader):
    def __init__(self, page):
        self.page = page

    def get_source(self, environment, template):
        path = self.page.find(template)
        if not (path or os.path.exists(path)):
            raise jinja2.TemplateNotFound(template)
        mtime = os.path.getmtime(path)
        with open(path, "r") as f:
            source = f.read()
        return source, path, lambda: mtime == os.path.getmtime(path)


PAGE_CACHE = {}


class Page:
    """
    Provides access to page data.
    """
    TIMESTAMP_FORMAT = "%Y:%m:%d:%H:%M"

    def __init__(self, page_root, quiet=False):
        global PAGE_CACHE
        page_root = os.path.abspath(page_root)
        assert(os.path.exists(page_root))
        assert(PAGE_CACHE.get(page_root) is None)
        PAGE_CACHE[page_root] = self

        if os.path.isfile(page_root):
            page_root = os.path.split(page_root)[0]
        self.page_root = page_root
        self.page_path = os.path.join(page_root, "page.html")
        self.meta_path = os.path.join(page_root, "meta.json")
        self.__page_data = None
        self.meta_data = None
        self.render_path = os.path.join(page_root, "index.html")

        self.jinja_env = jinja2.Environment(
            loader = PowerLoader(self),
            autoescape=jinja2.select_autoescape(['html', 'xml']))
        
        try:
            with open(self.page_path, "r") as page_file:
                # Just verify that we can open the file for now.
                self.__page_data = True
            with open(self.meta_path, "r") as meta_file:
                self.meta_data = json.load(meta_file)
        except:
            if not quiet:
                error = " --- Cannot open page:\n - {}\n - \n{}\n"
                print(error.format(self.page_root, sys.exc_info()))

    def __repr__(self):
        if self.is_valid:
            if self.is_published:
                return "<Page: {}>".format(self.slug)
            else:
                return "<Page WIP: {}>".format(self.slug)
        else:
            return "<Invalid Page>"
        
    @property
    def page_data(self):
        # Lazy load the page data.
        if self.__page_data:
            with open(self.page_path, "r") as page_file:
                return page_file.read()
        else:
            return None

    @property
    def is_valid(self):
        return self.page_data is not None and self.meta_data is not None

    @property
    def is_published(self):
        # A page is considered to be published if it is valid, and has
        # a fixed date stamp in its metadata.
        return self.is_valid and self.meta_data.get("date")        

    @property
    def datetime(self):
        if self.is_published:
            return datetime.strptime(
                self.meta_data.get("date"), self.TIMESTAMP_FORMAT)
        else:
            # Use the current time for unpublished or invalid pages.
            return datetime.now()

    @property
    def date_stamp(self):
        return self.datetime.strftime(self.TIMESTAMP_FORMAT)

    @property
    def date_locale(self):
        return self.datetime.strftime("%c")

    @property
    def slug(self):
        return os.path.split(self.page_root)[1]

    @property
    def path(self):
        return os.path.relpath(self.page_root, find_project_root())

    @property
    def tags(self):
        if self.is_valid:
            return self.meta_data.get("tags") or tuple()
        else:
            return tuple()

    @property
    def extends(self):
        if self.is_valid:
            return self.meta_data.get("extends") or tuple()
        else:
            return tuple()

    @property
    def context(self):
        return {
            "published" : self.datetime,
            "slug" : self.slug,
            "tags" : self.tags,
        }

    def find(self, asset):
        def find_in_path(asset, search_path):
            for dir_path, dir_names, file_names in os.walk(search_path):
                for file_name in file_names:
                    if file_name == asset:
                        return os.path.join(dir_path, file_name)
        found = find_in_path(asset, self.page_root)
        if found:
            return found
        else:
            project_root = find_project_root()
            for extend in self.extends:
                path = os.path.join(extend, project_root)
                page = access_page(path, True)
                if page.is_valid:
                    return page.find(asset)
                else:
                    found = find_in_path(asset, path)
                    if found:
                        return found

    def render(self, global_context):
        template = self.jinja_env.get_template("page.html")
        return template.render(**global_context, **self.context)
        

def access_page(page_path, quiet=False):
    page = PAGE_CACHE.get(page_path)
    if not page:
        page = Page(page_path, quiet)
        PAGE_CACHE[page_path] = page
    return page
