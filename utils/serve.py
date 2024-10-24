#!/usr/bin/env python
"""
Ensures the local Python server has responses with the expected HTTP headers
to create a proper security context in which web workers can function with
SharedArrayBuffer objects.

For more details, see:

https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer#security_requirements
"""
import argparse
from http import server


class MyHTTPRequestHandler(server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin:", "*")
        self.send_header("Cache-Control", "no-cache, must-revalidate")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "credentialless")
        server.SimpleHTTPRequestHandler.end_headers(self)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int, default=8000, nargs="?")
    args = parser.parse_args()
    server.test(
        HandlerClass=MyHTTPRequestHandler, bind="localhost", port=args.port
    )
