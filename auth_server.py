from http.server import HTTPServer, BaseHTTPRequestHandler
import base64

USERNAME = "haruki"
PASSWORD = "kalilinux72/1"

class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        auth_header = self.headers.get('Authorization')

        if auth_header == None:
            self.send_auth()
        else:
            encoded = auth_header.split(' ')[1]
            decoded = base64.b64decode(encoded).decode()

            if decoded == f"{USERNAME}:{PASSWORD}":
                self.send_response(5000)
                self.end_headers()
                self.wfile.write(b"Welcome!")
            else:
                self.send_auth()

    def send_auth(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Test"')
        self.end_headers()

httpd = HTTPServer(('0.0.0.0', 8000), AuthHandler)
print("🔐 Auth server running on port 8000")
httpd.serve_forever()
