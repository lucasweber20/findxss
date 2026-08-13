import yaml
from bs4 import BeautifulSoup


class XSS:
    def __init__(self):
        pass

    def check_chars(self, body, url):
        html_context = []
        js_context = []
        attr_context = []
        counter = 0
        chars = [">", "<", '"', "'"]
        for line in body.split("\n"):
            soup = BeautifulSoup(line, 'html.parser')
            for t in soup.findAll():

                # Check payload between tags contexts
                if "findxss" in str(t.string): 
                    for char in chars:
                        if char in t.string:
                            print(f"Char reflected: {char}")
                            counter += 1
                            if counter == 4:
                                if "script" in t.name:
                                    js_context.append(url)
                                else:
                                    html_context.append(url)

                # Check payload into the attributes
                for attr in t.attrs:
                    if "findxss" in t[attr]:
                        for char in chars:
                            if char in t[attr]:
                                print(f"Char reflected: {char}")
                                if '"' in t[attr] and "'" in t[attr]:
                                    attr_context.append(url)
                                    
        return html_context, js_context, attr_context

    def generate_payloads(self, url):
        with open("./db/payloads.yml", "r") as f:
            payloads = yaml.safe_load(f)
            
        if url[0]: # HTML context
            html_context = payloads["payloads"][0]["html_context"]
        elif url[1]: # JS context
            js_context = payloads["payloads"][1]["js_context"]
            print(js_context)
        elif url[2]: # Attribute context
            attr_context = payloads["payloads"][2]["attr_context"]


