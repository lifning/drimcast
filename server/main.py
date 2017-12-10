import http.server
import subprocess
import re

URL_REGEX = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'


class DrimcastRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length).decode('utf-8')
        urls = re.findall(URL_REGEX, data)
        if urls:
            self.send_response(200)
        else:
            self.send_response(400)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        for url in urls:
            subprocess.check_call(
                ['livestreamer', url, 'best', '-p', 'mplayer -fs'],
                stdout=self.wfile)


def main():
    addr = ('', 8000)
    httpd = http.server.HTTPServer(addr, DrimcastRequestHandler)
    try:
        httpd.serve_forever()
    finally:
        httpd.server_close()

main()
