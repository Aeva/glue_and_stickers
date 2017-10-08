
import os
import time
import json
from functools import reduce

import assets
from cmd_common import register


@register
def render():
    """
    Generates the static index.html files from the page.html template
    files.
    """

    start = time.monotonic()

    root = assets.find_project_root()
    manual_context_path = os.path.join(root, "globals.meta")
    manual_context = {}
    if os.path.isfile(manual_context_path):
        manual_context = json.load(manual_context_path)
    
    pages = assets.published_pages()
    tags = set()
    for page in pages:
        tags.update(page.tags)

    context = {
        "current_page" : False,
        "latest_page" : pages[-1],
        "first_page" : pages[0],
        "all_pages" : pages,
        "all_tags" : sorted(tags),
    }
    for index, page in enumerate(pages):
        is_last = page == pages[-1]
        is_first = page == pages[0]
        context["page_before"] = None if is_first else pages[index-1]
        context["page_after"] = None if is_last else pages[index+1]
        
        with open(page.render_path, "w") as out_file:
            out_file.write(page.render({**manual_context, **context}))
            
    elapsed = time.monotonic() - start
    total = len(pages)
    print("Rendered {} pages in {} seconds.".format(
        total, round(elapsed, 2)))
