import os
import json
import hashlib

# ==============================================================================
# KLPYTHON TERMINAL - GENERATOR MIRROR METADATA (V3 KERNEL VERSION SUPPORT)
# ==============================================================================

# Phiên bản hiện tại của kernel hệ thống
ver = "1.3.0"

def get_normalized_sha256(file_path: str) -> str:
    """
    Chuẩn hóa nội dung file (loại bỏ khác biệt CRLF/LF và khoảng trắng thừa) 
    trước khi tính SHA-256 để khớp tuyệt đối với bộ nạp (kernel loader).
    """
    try:
        with open(file_path, "rb") as f:
            raw_bytes = f.read()
        content = raw_bytes.decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"⚠️ Không thể đọc file {file_path}: {e}")
        content = ""

    # 1. Chuẩn hóa ký tự xuống dòng Windows (\r\n) thành chuẩn chung Linux (\n)
    content = content.replace("\r\n", "\n")
    
    # 2. Xóa bỏ khoảng trắng hoặc dòng trống thừa ở đầu và cuối file
    content = content.strip()
    
    # 3. Tính mã SHA-256 trên chuỗi đã được chuẩn hóa sạch sẽ
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def generate_mirror_metadata():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bin_dir = os.path.join(base_dir, "bin")
    mirror_output_path = os.path.join(base_dir, "mirror.json")
    version_json_filename = f"{ver}.json"
    version_json_output_path = os.path.join(base_dir, version_json_filename)

    if not os.path.exists(bin_dir):
        print(f"[ ERROR ] Không tìm thấy thư mục bin: {bin_dir}")
        print(f"📁 Đang tiến hành tạo thư mục 'bin' tự động...")
        os.makedirs(bin_dir, exist_ok=True)
        print(f"👉 Hãy bỏ các file lệnh .py vào thư mục bin/ rồi chạy lại script nhé!")
        return

    print(f"=== Đang quét thư mục bin để tạo metadata chuẩn hóa cho phiên bản v{ver} ===")

    bin_files_data = {}  # {author: {filename: sha256_hash}}
    pack_list = []       # Danh sách tên file cho khóa "pack"

    for filename in os.listdir(bin_dir):
        if not filename.endswith(".py"):
            continue
        
        file_path = os.path.join(bin_dir, filename)
        pack_list.append(filename)

        # 1. Tính SHA-256 bằng hàm chuẩn hóa (Chống lệch CRLF/LF)
        file_hash = get_normalized_sha256(file_path)

        # 2. Trích xuất tên tác giả (author hoặc cfs_author)
        author = "longtrinh2666"  # Mặc định nếu không tìm thấy
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    stripped = line.strip()
                    if stripped.startswith("author") or stripped.startswith("cfs_author"):
                        parts = stripped.split("=")
                        if len(parts) > 1:
                            author = parts[1].strip().strip('"').strip("'")
                            break
        except Exception:
            pass

        # 3. Gom nhóm vào cấu trúc của bin.json
        if author not in bin_files_data:
            bin_files_data[author] = {}
        bin_files_data[author][filename] = file_hash
        print(f"  + Đã quét: {filename} (Tác giả: {author}) -> SHA256: {file_hash[:16]}...")

    # 1. Tạo file bin.json (chứa mã băm SHA-256 của các lệnh)
    bin_json_output_path = os.path.join(base_dir, "bin.json")
    with open(bin_json_output_path, "w", encoding="utf-8") as f:
        json.dump(bin_files_data, f, indent=4, ensure_ascii=False)

    # 2. Tạo file cấu hình riêng cho phiên bản (Ví dụ: 1.3.0.json chứa danh sách pack)
    version_data = {
        "ver": ver,
        "pack": sorted(pack_list)
    }
    with open(version_json_output_path, "w", encoding="utf-8") as f:
        json.dump(version_data, f, indent=4, ensure_ascii=False)

    # 3. Tạo file mirror.json tổng hợp theo cấu trúc mới có ánh xạ kernel
    mirror_data = {
        "name": "KLpython-official-mirror",
        "bin": "https://raw.githubusercontent.com/longtrinh2666/klpython-terminal/refs/heads/mirror/bin.json",
        "pack-url": "https://raw.githubusercontent.com/longtrinh2666/klpython-terminal/refs/heads/mirror/bin/",
        "kernel": {
            ver: f"https://raw.githubusercontent.com/longtrinh2666/klpython-terminal/refs/heads/mirror/mirror/{version_json_filename}"
        }
    }

    with open(mirror_output_path, "w", encoding="utf-8") as f:
        json.dump(mirror_data, f, indent=4, ensure_ascii=False)

    print(f"\n✅ Đã tạo thành công các file cấu hình tương thích hệ thống mới:")
    print(f"   - {mirror_output_path} (File mirror.json chính)")
    print(f"   - {bin_json_output_path} (File chứa mã băm bin.json)")
    print(f"   - {version_json_output_path} (File danh sách gói cho phiên bản v{ver})")
    print(f"==========================================================")

if __name__ == "__main__":
    generate_mirror_metadata()