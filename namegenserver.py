import traceback
import random
import socketserver
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os

if os.getenv('NAMEGEN_PORT', '8080').isdigit():
    PORT = int(os.getenv('NAMEGEN_PORT', '8080'))
else:
    PORT = 8080

class NameServer(BaseHTTPRequestHandler):
    first_names = [
        "Rasmus",
        "Sebastian",
        "Andreas",
        "Jonas"]

    last_names = [
        "Lorenzen",
        "Hajslund",
        "Specht",
        "Therkildsen"]

    def do_GET(self):
        try:
            url = urlparse(self.path)
            query = parse_qs(url.query)
            path = url.path

            if path == '/name':
                count = 1
                if query:
                    if query.get('count'):
                        if query.get('count')[0].isdigit():
                            count = int(query.get('count')[0])

                response_obj = []
                for x in range(0, count):
                    first_name = NameServer.first_names[random.randint(0, len(NameServer.first_names) - 1)]
                    last_name = NameServer.last_names[random.randint(0, len(NameServer.last_names) - 1)]
                    name_obj = {'name': first_name + " " + last_name}
                    response_obj.append(name_obj)
                self.send_response(200)
            else:
                response_obj = {'error': "The path " + path + " is not valid. please try /name"};
                self.send_response(404)
        except BaseException as be:
            response_obj = {'error': "Exception message: " + str(be)}
            print(traceback.format_exc())
            self.send_response(500)

        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(response_obj), 'utf-8'))

with socketserver.TCPServer(("", PORT), NameServer) as httpd:
    print("[INFO] Serving at port", PORT)
    httpd.serve_forever()
