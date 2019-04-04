import sys, os

# __debug__ is always true when building w/ cx_freeze, no known solution
DEBUG = __debug__ and not hasattr(sys, 'frozen')

def die(message=None):
    if message:
        print(message)

    sys.exit(0)

def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.join(
            os.path.dirname(__file__), ".."
        )
        

    return os.path.join(datadir, filename)

