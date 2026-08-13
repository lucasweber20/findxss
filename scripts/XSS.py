from bs4 import BeautifulSoup


class XSS:
    def __init__(self):
        pass

    def check_chars(self, body, url):
        tag_context = []
        attr_context = []
        chars = [">", "<", '"', "'"]
        for line in body.split("\n"):
            soup = BeautifulSoup(line, 'html.parser')
            for t in soup.findAll():

                # Check payload between tags contexts
                if "findxss" in str(t.string): 
                    for char in chars:
                        if char in t.string:
                            print(f"Char reflected: {char}")
                            if ">" in t.string and "<" in t.string:
                                tag_context.append(url)

                # Check payload into the attributes
                for attr in t.attrs:
                    if "findxss" in t[attr]:
                        for char in chars:
                            if char in t[attr]:
                                print(f"Char reflected: {char}")
                                if '"' in t[attr] and "'" in t[attr]:
                                    attr_context.append(url)
