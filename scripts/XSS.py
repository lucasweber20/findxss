from bs4 import BeautifulSoup


class XSS:
    def __init__(self):
        pass

    def check_chars(self, body):
        chars = [">", "<", '"', "'"]
        for line in body.split("\n"):
            soup = BeautifulSoup(line)
            for tag in soup.find_all():
                for attr in tag.attrs:
                    for char in chars:
                        if char in tag[attr]:
                            print(f"Char reflected: \033[92m{char}\033[00m")
                    