
import sys
import glob
import os.path
from cmd_common import run_command


def load_plugins():
    module_path = os.path.split(__file__)[0]
    for path in glob.glob(os.path.join(module_path, "cmd*.py")):
        plugin = os.path.split(path)[1][:-3]
        __import__(plugin)


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        print("Glue and Stickers requires Python 3")
        exit(1)
    
    load_plugins()
    run_command(*sys.argv[1:])
