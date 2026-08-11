

class URL:
    def __init__(self):
        pass

    def remove_duplicates(self, file):
        with open(file, 'r') as f:
            file_read = f.read().splitlines()
        result = list(dict.fromkeys(file_read))
        return result