import http.server
import socketserver
import json
import webbrowser
import os
import subprocess
import base64
from datetime import datetime

PORT = 8080
GIT_PATH = r"C:\Program Files\Git\cmd\git.exe"

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            # Xử lý ảnh đại diện nếu có dạng base64
            if 'avatar_base64' in data and data['avatar_base64']:
                try:
                    format, imgstr = data['avatar_base64'].split(';base64,')
                    ext = format.split('/')[-1]
                    filename = f"avatar_user.{ext}"
                    with open(filename, "wb") as fh:
                        fh.write(base64.b64decode(imgstr))
                    data['profile']['avatar'] = filename
                    del data['avatar_base64'] # Xóa dữ liệu rác trước khi lưu JSON
                except Exception as e:
                    print(f"Lỗi lưu ảnh: {e}")

            # 1. Lưu vào data.json
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            # 2. Tự động Push lên GitHub
            print(f"\n[!] Đang tự động cập nhật lên GitHub...")
            try:
                subprocess.run([GIT_PATH, "add", "."], check=True) # Add tất cả (bao gồm ảnh mới)
                subprocess.run([GIT_PATH, "commit", "-m", f"Update via App - {datetime.now().strftime('%Y-%m-%d %H:%M')}"], check=True)
                subprocess.run([GIT_PATH, "push", "origin", "main"], check=True)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode())
                print("[OK] Đã cập nhật thành công!")
            except Exception as e:
                print(f"[!] Lỗi: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"[*] App đang chạy tại http://localhost:{PORT}")
    webbrowser.open(f"http://localhost:{PORT}/manager.html")
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.shutdown()
