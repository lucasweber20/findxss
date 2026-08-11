from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse, unquote


class Parser:
    def __init__(self, url):
        self.url = url

    def parser_params(self, payload):
        keyword = payload
        parsed_url = urlparse(self.url)
        if parsed_url.query:
            params = parse_qsl(parsed_url.query)
            fuzzed_params = [(k, keyword) for k, _ in params]
            fuzzed_query = urlencode(fuzzed_params)
            fuzzed_url = unquote(urlunparse([parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, fuzzed_query, parsed_url.fragment]))

            return fuzzed_url