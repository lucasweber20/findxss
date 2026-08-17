import argparse
import concurrent.futures
from scripts.URL import URL
from scripts.Parser import Parser
from scripts.Requests import Requests
from scripts.XSS import XSS


parser = argparse.ArgumentParser()

args = parser.add_argument("-u", "--url", help='Specify url, example: -u https://example.com/?param=value', nargs="+", type=str)
args = parser.add_argument("-l", "--list", help="Specify file with urls, example: -l urls.txt", type=str)
args = parser.add_argument("-t", "--thread", help="Specify threads number, example: -t 2", default=1, type=int)
args = parser.add_argument("-o", "--output", help="Specify output file, example: -o outputs.txt", type=str)

args = parser.parse_args()

def main():
    # Arguments flags
    url = args.url
    file = args.list
    thread = args.thread
    output = args.output

    payload = """FxSsfindxss><"'FxSs"""

    urls = URL()

    # Remove duplicates
    if file:
        url = urls.remove_duplicates(file)

    # Parser
    parsed_urls = []
    for parser_url in url:
        parser = Parser(parser_url)
        parsed_urls_params = parser.parser_params(payload)
        if parsed_urls_params and parsed_urls_params not in parsed_urls:
            parsed_urls.append(parsed_urls_params)

    # Requests
    req = Requests()
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
        futures = [executor.submit(req.requests, url) for url in parsed_urls]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                url = result[0]
                body = result[1]

                # Check if payload reflected
                if "findxss" in body:
                    print(f"Reflected: \033[92m{url}\033[00m")

                    # Check characters if reflected
                    print("===== \033[92mCharacter reflecteds\033[00m =====")
                    xss = XSS()
                    check_chars = xss.check_chars(body, url)
                    
                    if check_chars:
                        print("===== \033[92mPayloads\033[00m =====")
                        xss.generate_payloads(check_chars)
                        if output:
                            write_file = open(output, "a").write(f"{url}\n")

if __name__ == "__main__":
    main()