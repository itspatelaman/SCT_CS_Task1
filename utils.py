def save_to_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)


def load_from_file(filename):
    with open(filename, 'r') as f:
        return f.read()
