import time
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Cấu hình
FILE_TO_WATCH = "data.json"
GIT_PATH = r"C:\Program Files\Git\cmd\git.exe"

class DeployHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_run = 0
        
    def on_modified(self, event):
        if event.src_path.endswith(FILE_TO_WATCH):
            # Tránh chạy trùng lặp quá nhanh (debounce)
            current_time = time.time()
            if current_time - self.last_run < 5:
                return
            
            self.last_run = current_time
            print(f"\n[!] Phát hiện thay đổi trong {FILE_TO_WATCH}")
            self.deploy()

    def deploy(self):
        print("[...] Đang tự động deploy lên GitHub...")
        try:
            # Commit and Push
            subprocess.run([GIT_PATH, "add", "data.json"], check=True)
            subprocess.run([GIT_PATH, "commit", "-m", "Auto-update card info"], check=True)
            result = subprocess.run([GIT_PATH, "push", "origin", "main"], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("[OK] Đã cập nhật thành công lên GitHub Pages!")
            else:
                print(f"[!] Lỗi khi push: {result.stderr}")
        except Exception as e:
            print(f"[!] Lỗi: {e}")

if __name__ == "__main__":
    # Cài đặt thư viện cần thiết nếu chưa có
    try:
        import watchdog
    except ImportError:
        print("[INFO] Đang cài đặt thư viện hỗ trợ (watchdog)...")
        subprocess.run(["pip", "install", "watchdog"], check=True)
        import watchdog

    print("============================================")
    print("      Pro ID - Bộ Tự Động Hóa Đã Sẵn Sàng")
    print("============================================")
    print(f"[*] Đang theo dõi file: {os.path.abspath(FILE_TO_WATCH)}")
    print("[*] Khi bạn sửa thông tin trong manager.html, tôi sẽ tự cập nhật GitHub.")
    print("[*] Nhấn Ctrl+C để dừng.")
    print("--------------------------------------------")

    event_handler = DeployHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
