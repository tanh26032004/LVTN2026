# Cloudinary Client - Upload, Delete, List images
import streamlit as st
import cloudinary
import cloudinary.uploader
import cloudinary.api

def _init_cloudinary():
    """Khởi tạo Cloudinary từ st.secrets."""
    if "cloudinary" not in st.secrets:
        raise ValueError("Thiếu cấu hình [cloudinary] trong secrets.toml")
    
    cfg = st.secrets["cloudinary"]
    cloudinary.config(
        cloud_name=cfg["cloud_name"],
        api_key=cfg["api_key"],
        api_secret=cfg["api_secret"],
        secure=True
    )

def upload_image(file_data, filename):
    """
    Upload ảnh lên Cloudinary.
    Args:
        file_data: File-like object (từ st.file_uploader).
        filename: Tên file (dùng làm public_id, không có đuôi).
    Returns:
        dict: {"url": ..., "public_id": ...} hoặc None nếu lỗi.
    """
    _init_cloudinary()
    # Bỏ đuôi file để làm public_id
    public_id = filename.rsplit(".", 1)[0] if "." in filename else filename
    folder = "lvtn2026"
    
    try:
        result = cloudinary.uploader.upload(
            file_data,
            public_id=public_id,
            folder=folder,
            overwrite=True,
            resource_type="image"
        )
        return {
            "url": result.get("secure_url"),
            "public_id": result.get("public_id")
        }
    except Exception as e:
        print(f"Cloudinary upload error: {e}")
        return None

def delete_image(public_id):
    """
    Xóa ảnh khỏi Cloudinary.
    Args:
        public_id: ID của ảnh trên Cloudinary (ví dụ: "lvtn2026/mbti_intj").
    Returns:
        bool: True nếu xóa thành công.
    """
    _init_cloudinary()
    try:
        result = cloudinary.uploader.destroy(public_id, resource_type="image")
        return result.get("result") == "ok"
    except Exception as e:
        print(f"Cloudinary delete error: {e}")
        return False

def list_images():
    """
    Lấy danh sách tất cả ảnh đã upload trong folder lvtn2026.
    Returns:
        list[dict]: Mỗi phần tử gồm {"filename": ..., "url": ..., "public_id": ...}
    """
    _init_cloudinary()
    try:
        # Thử lấy danh sách tài nguyên
        result = cloudinary.api.resources(
            type="upload",
            prefix="lvtn2026/",
            max_results=500,
            resource_type="image"
        )
        
        images = []
        for r in result.get("resources", []):
            pid = r.get("public_id", "")
            # Lấy tên file từ public_id (bỏ prefix "lvtn2026/")
            fname = pid.replace("lvtn2026/", "") if pid.startswith("lvtn2026/") else pid
            images.append({
                "filename": fname,
                "url": r.get("secure_url"),
                "public_id": pid,
                "format": r.get("format", "png"),
                "size": r.get("bytes", 0),
            })
        return images
    except Exception as e:
        # Nếu lỗi 500 từ Cloudinary, log ra console và trả về list rỗng để app không chết
        print(f"Cloudinary list error: {e}")
        # Bạn có thể thử reload lại trang nếu gặp lỗi này
        return []
