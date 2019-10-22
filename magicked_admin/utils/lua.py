from utils import find_data_file


def load_script(filename):
    filepath = find_data_file(filename)
    with open(filepath, 'r') as file:
        script = file.read()
    return script
