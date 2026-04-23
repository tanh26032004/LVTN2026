import os
import tomllib
import cloudinary
import cloudinary.uploader
import cloudinary.api

# 1. Load configuration from secrets.toml
SECRETS_PATH = '.streamlit/secrets.toml'
if not os.path.exists(SECRETS_PATH):
    print("Error: .streamlit/secrets.toml not found")
    exit(1)

with open(SECRETS_PATH, 'rb') as f:
    secrets = tomllib.load(f)

cfg = secrets.get('cloudinary')
if not cfg:
    print("Error: [cloudinary] section not found in secrets.toml")
    exit(1)

cloudinary.config(
    cloud_name=cfg['cloud_name'],
    api_key=cfg['api_key'],
    api_secret=cfg['api_secret'],
    secure=True
)

# 2. Path to local images
IMG_DIR = 'assets/images'
if not os.path.exists(IMG_DIR):
    print(f"Error: Directory {IMG_DIR} not found")
    exit(1)

# 3. List and upload images
images = [f for f in os.listdir(IMG_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
print(f"Found {len(images)} images in {IMG_DIR}. Starting upload...")

folder = "lvtn2026"
success_count = 0

for img_name in images:
    img_path = os.path.join(IMG_DIR, img_name)
    public_id = img_name.rsplit(".", 1)[0]
    
    print(f"Uploading {img_name}...", end=" ", flush=True)
    try:
        result = cloudinary.uploader.upload(
            img_path,
            public_id=public_id,
            folder=folder,
            overwrite=True,
            resource_type="image"
        )
        print(f"DONE. URL: {result.get('secure_url')}")
        success_count += 1
    except Exception as e:
        print(f"FAILED: {e}")

print(f"\n--- SYNC COMPLETE ---")
print(f"Successfully uploaded: {success_count}/{len(images)}")
