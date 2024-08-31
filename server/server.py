from agents import Drone, Guard, SimulationModel
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import threading
import time 

SimulationModel = None


class Server(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write(json.dumps({"message": "Hello, World!"}).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        self._set_response()
        self.wfile.write(json.dumps({"message": "POST received"}).encode("utf-8"))
        self.handle_request(post_data)


def run(server_class=HTTPServer, handler_class=Server, port=8585):
    logging.basicConfig(level=logging.INFO)
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    logging.info(f"Starting httpd on port {port}")
    httpd.serve_forever()


# Parse client data

# Ontology

if __name__ == "__main__":
    p = threading.Thread(target=run, args=tuple(), daemon=True)
    p.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Server stopped.")

