
import assets
from cmd_common import register


def debug_info():
    print(assets.find_project_root())


register("info", debug_info)
