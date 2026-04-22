import json
import os

# Đường dẫn tệp
json_path = "/Users/wocten/Documents/LVTN2026/.streamlit/lvtn2026-firebase-adminsdk-fbsvc-13fe218315.json"
secrets_path = "/Users/wocten/Documents/LVTN2026/.streamlit/secrets.toml"

def run():
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found")
        return
        
    with open(json_path, 'r') as f:
        data = json.load(f)
        
    # Lấy các giá trị hiện có trong secrets (để giữ lại admin.password_hash và firebase.api_key)
    existing_content = ""
    if os.path.exists(secrets_path):
        with open(secrets_path, 'r') as f:
            existing_content = f.read()
            
    # Tách phần admin và firebase (Web API Key)
    admin_sect = ""
    fb_sect = ""
    for line in existing_content.splitlines():
        if line.startswith("[admin]") or admin_sect:
            if line.startswith("[") and not line.startswith("[admin]"): 
                break
            admin_sect += line + "\n"
        if line.startswith("[firebase]") or fb_sect:
            if line.startswith("[") and not line.startswith("[firebase]"):
                break
            fb_sect += line + "\n"
            
    # Tạo nội dung mới
    new_content = admin_sect.strip() + "\n\n" + fb_sect.strip() + "\n\n"
    new_content += "[firebase_service_account]\n"
    for k, v in data.items():
        if k == "private_key":
            # Dùng triple quotes cho private key
            new_content += f'{k} = """{v}"""\n'
        else:
            new_content += f'{k} = "{v}"\n'
            
    with open(secrets_path, 'w') as f:
        f.write(new_content)
    print("Successfully updated secrets.toml with multiline private_key")

if __name__ == "__main__":
    run()
