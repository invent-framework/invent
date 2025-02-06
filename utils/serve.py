#!/usr/bin/env python
"""
Ensures the local Python server has responses with the expected HTTP headers
to create a proper security context in which web workers can function with
SharedArrayBuffer objects.

For more details, see:

https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer#security_requirements
"""
import multiprocessing
import subprocess
import argparse
import time
from http import server
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHTTPRequestHandler(server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin:", "*")
        self.send_header("Cache-Control", "no-cache, must-revalidate")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "credentialless")
        server.SimpleHTTPRequestHandler.end_headers(self)


class ServerSubProcess(multiprocessing.Process):
    """
    A subprocess used to run the HTTP server.

    Will be terminated and restarted when a change has been detected in the
    source code.
    """

    def __init__(self, port):
        super().__init__()
        self.port = port

    def run(self):
        server.test(
            HandlerClass=MyHTTPRequestHandler, bind="localhost", port=self.port
        )


class SourceChangeHander(FileSystemEventHandler):
    """
    A file system event handler that restarts the HTTP server when a change
    has been detected in the source code.
    """

    def __init__(self, port):
        """
        Take the port number as an argument, and start the server subprocess.
        """
        self.port = port
        self.start_server()

    def on_modified(self, event):
        self.restart_server()

    def on_created(self, event):
        self.restart_server()

    def restart_server(self):
        """
        Stop the server subprocess, `make package`, and restart the server
        subprocess.
        """
        print("♻️  Restarting server...")
        self.stop_server()
        subprocess.run(["make", "package"])
        self.start_server()

    def start_server(self):
        """
        Start the server subprocess.
        """
        self.server_process = ServerSubProcess(self.port)
        self.server_process.start()

    def stop_server(self):
        """
        Stop the server subprocess.
        """
        self.server_process.terminate()
        self.server_process.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int, default=8000, nargs="?")
    args = parser.parse_args()
    event_handler = SourceChangeHander(args.port)
    invent_observer = Observer()
    test_observer = Observer()
    for path in [
        "src/invent",
        "src/toga/core/src/toga",
        "src/toga/travertino/src/travertino",
        "src/toga_invent",
    ]:
        invent_observer.schedule(event_handler, path, recursive=True)
    test_observer.schedule(event_handler, "tests", recursive=True)
    invent_observer.start()
    test_observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        event_handler.stop_server()
        invent_observer.stop()
        test_observer.stop()
    invent_observer.join()
    test_observer.join()
