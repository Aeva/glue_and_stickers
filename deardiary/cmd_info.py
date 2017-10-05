
import os
import assets
from cmd_common import register


def print_index(pages, verbose=False):
    for page in pages:
        marker = "-"
        if (verbose and page.extends) or page.is_published or page.tags:
            marker = "+"

        print("\n {} {}".format(marker, page.path))
        if page.is_published:
            print("   - {}".format(page.date_locale))
        elif verbose:
            print("   - UNPUBLISHED")
            
        if page.tags:
            print("   - tags: {}".format(", ".join(page.tags)))
            
        if verbose and page.extends:
            print("   + search paths:")
            for extend in page.extends:
                print("     - {}".format(extend))
    print()


@register
def info():
    """
    Prints info about the current Glue and Stickers context.
    """

    root = assets.find_project_root()
    print("Project root:\n\n   {}\n\n".format(root))
    
    current = assets.working_page()
    if current:
        print("Current Page:")
        print_index([current], True)

        # TODO : this is temporary debug code, and should be removed
        # once we have a command for rendering templates
        print("----------------------")
        print(current.render())

    else:
        published = assets.published_pages()
        if published:
            print("Published Pages:")
            print_index(published)

        unpublished = assets.secret_pages()
        if unpublished:
            if published:
                print()
            print("Unpublished Pages:")
            print_index(unpublished)

