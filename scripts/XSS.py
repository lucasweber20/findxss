import yaml
import re
from bs4 import BeautifulSoup
from scripts.Parser import Parser


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
                            print(f"Char reflected: \033[92m{char}\033[00m")
                            counter += 1
                            if counter == 4:
                                if "script" in t.name:
                                    js_context.append(url)
                                else:
                                    html_context.append(url)

                # Check payload into the attributes
                for attr in t.attrs:
                    if "findxss" in t[attr]:
                        match = re.search(r"FxSs.+FxSs", str(t))
                        match_payload = match.group()
                        for char in chars:
                            if char in match_payload:
                                print(f"Char reflected: \033[92m{char}\033[00m")
                                if '"' in match_payload and "'" in match_payload:
                                    attr_context.append(url)
                                    
        return html_context, js_context, attr_context

    def generate_payloads(self, url):
        with open("./db/payloads.yml", "r") as f:
            payloads = yaml.safe_load(f)
            
        if url[0]: # HTML context
            for u in url[0]:
                parser = Parser(u)
                html_context = payloads["payloads"][0]["html_context"]
                for html_payload in html_context:
                    print(parser.parser_params(html_payload))
        elif url[1]: # JS context
            for u in url[1]:
                parser = Parser(u)
                js_context = payloads["payloads"][1]["js_context"]
                for js_payload in js_context:
                    print(parser.parser_params(js_payload))
        elif url[2]: # Attribute context
            for u in url[2]:
                parser = Parser(u)
                attr_context = payloads["payloads"][2]["attr_context"]
                for attr_payload in attr_context:
                    print(parser.parser_params(attr_payload))
        print("\n")

# https://revistapag.agricultura.rs.gov.br/ojs/index.php/revistapag/login?source=findxss