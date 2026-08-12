import re
from bs4 import BeautifulSoup


class XSS:
    def __init__(self):
        pass

    def check_chars(self, body):
        for line in body.split("\n"):
            soup = BeautifulSoup(line)
            for tag in soup.find_all():
                for attr in tag.attrs:
                    if ">" in tag[attr]:
                        print("Char reflected: \033[92m>\033[00m")
                    elif "<" in tag[attr]:
                        print("Char reflected: \033[92m<\033[00m")
                    elif '"' in tag[attr]:
                        print('Char reflected: \033[92m"\033[00m')
                    elif "'" in tag[attr]:
                        print("char reflected: \033[92m'\033[00m")
                    