from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json

class SimpleHandler(BaseHTTPRequestHandler):
    def do_PUT(self):
        print("요청 path:", self.path)
        print("headers:", self.headers)
        # 현대 로보틱스 http_cli는 /setting 으로만 옴
        if self.path.rstrip("/") == "/setting":
            length = int(self.headers.get("Content-Length", 0))
            print("============================")
            print("Content-Length", length)
            body = self.rfile.read(length)
            data = json.loads(body)
            #json형태로 수신
            max_torque = data["max_torque"]
            print("받은 max_torque:", max_torque)
            #print("body repr", repr(body))
            print("============================")
            print("raw body bytes:", body)
            print("raw body decoded:", body.decode("utf-8"))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

        else:
            self.send_response(404)
            self.end_headers()

    # 로그 정리용 (선택)
    def log_message(self, format, *args):
        return     
        
    def do_GET(self):        
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("HTTP 서버 정상 동작 중".encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        print("받은 데이터:", body)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8765), SimpleHandler)
    print("HTTP 서버 시작 (port 8765)")
    server.serve_forever()