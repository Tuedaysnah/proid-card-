import os
import json
import base64

def check_files():
    files = ["index.html", "manager.html", "card.css", "data.json", "APP_QUAN_LY.py", "deploy.bat"]
    print("--- KIỂM TRA FILE HỆ THỐNG ---")
    for f in files:
        status = "✅ OK" if os.path.exists(f) else "❌ THIẾU"
        print(f"{f:15}: {status}")

def check_data():
    print("\n--- KIỂM TRA DỮ LIỆU (data.json) ---")
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        prof = data.get('profile', {})
        print(f"Họ tên: {prof.get('firstName')} {prof.get('lastName')}")
        print(f"Chức vụ: {prof.get('jobTitle')}")
        print(f"Công ty: {prof.get('company')}")
        print(f"SĐT: {prof.get('phone')}")
        
        # Kiểm tra ảnh đại diện
        avatar = prof.get('avatar', '')
        if avatar.startswith('./') or os.path.exists(avatar):
            print(f"Ảnh đại diện: ✅ {avatar}")
        else:
            print(f"Ảnh đại diện: ⚠️ Không tìm thấy file ({avatar})")

        # Kiểm tra xử lý Base64 (Nếu còn tồn tại trong file)
        if 'avatar_base64' in data:
            print("Base64 đệm: ⚠️ Vẫn còn (Cần chạy server để xử lý)")

    except Exception as e:
        print(f"Lỗi đọc data.json: {e}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    check_files()
    check_data()
