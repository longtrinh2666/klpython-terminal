import os
import importlib.util
import zipfile
import sys
import zipfile
import tarfile
import platform
import code
import subprocess
import datetime
import socket
import atexit
import shlex
import builtins
import hashlib
import json
import re
from typing import Optional
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
    from argon2 import PasswordHasher
    import curses
    import psutil
    import speedtest
    import requests
    system = platform.system()
    if system in ("Darwin", "Linux"):
        import curses
        import readline 
    elif system in ("Windows"):
        try:
            import curses
        except ImportError:
            import windows_curses as curses
        import pyreadline3
except ModuleNotFoundError:
    print("your system doesn't has some python Module to run , do you want install?")
    while True:
        install = input("(y/n):")
        if install.lower() == "y":
            try:
                system = platform.system()
                subprocess.run([sys.executable, "-m", "pip", "install", "argon2-cffi"], check=True)
                subprocess.run([sys.executable, "-m", "pip", "install", "pycryptodome"], check=True)
                subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
                subprocess.run([sys.executable, "-m", "pip", "install", "speedtest-cli"], check=True)
                subprocess.run([sys.executable, "-m", "pip", "install", "psutil"], check=True)
                if system in ("Darwin", "Linux"):
                    subprocess.run([sys.executable, "-m", "pip", "install", "curses"], check=True)
                    subprocess.run([sys.executable, "-m", "pip", "install", "readline"], check=True)
                    import readline
                    import psutil
                    import requests
                    import speedtest
                    import curses
                    from Crypto.Cipher import AES
                    from Crypto.Util.Padding import unpad
                    from argon2 import PasswordHasher
                    break
                elif system in ("Windows"):
                    subprocess.run([sys.executable, "-m", "pip", "install", "windows-curses"], check=True)
                    subprocess.run([sys.executable, "-m", "pip", "install", "pyreadline3"], check=True)
                    import pyreadline3
                    import psutil
                    import requests
                    import speedtest
                    from Crypto.Cipher import AES
                    from Crypto.Util.Padding import unpad
                    from argon2 import PasswordHasher
                    try:
                        import curses
                        break
                    except ImportError:
                        import windows_curses as curses
                        break
            except Exception as e:
                print("Error:", e)
                #print("does pip installed on your python? if error not installed choose y")
                #while True:
                    #install_pip_question = input("(y/n):")
                    #if install_pip_question.lower() == "y":
                        #try:
                            #subprocess.run([sys.executable, "get-pip.py"], check=True)
                        #except Exception as e:
                            #print("Error installing pip:", e)
                    #if install_pip_question.lower() == "n":
                        #run = False
                        #break
                    #else:
                        #print("error, only use y/n")

                run = False
                break
        if install.lower() == "n":
            run = False
            break
        else:
            print("error, only use y/n")
    
import time
import shutil
try:
    import readline   # Linux/macOS
except ImportError:
    import pyreadline3 as readline  # Windows

# chọn file history
if platform.system() == "Windows":
    histfile = os.path.join(os.environ.get("TEMP", os.getcwd()), "myshell_history.txt")
else:
    histfile = os.path.join("/tmp", "myshell_history.txt")

# nạp lại history nếu có
try:
    readline.read_history_file(histfile)
except FileNotFoundError:
    pass

# khi thoát thì ghi lại history
atexit.register(readline.write_history_file, histfile)
run = True
ROOT_DIR = os.getcwd()
username = os.environ.get('USERNAME') or os.environ.get('USER')
ENV = {
    "ver": "1.3.0",
    "ROOT_DIR": ROOT_DIR,
    "current_dir": ROOT_DIR,
    "username": username
}
os.chdir(ROOT_DIR + "/root")

# ==============================================================================
# KLPYTHON TERMINAL - MULTI-MIRROR JSON & PACK LOADER (FULL CODE WITH ver)
# ==============================================================================

import os
import sys
import json
import hashlib
import importlib.util
import platform
import requests
import builtins
from typing import Optional

# ---------------- Config / Globals ----------------
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

BIN_DIR = os.path.join(ROOT_DIR, "bin")
MIRROR_LIST_PATH = os.path.join(ROOT_DIR, "mirror", "mirror.txt")
TRUST_STORE_PATH = os.path.join(ROOT_DIR, "trusted.json")

commands = {}

BLACKLIST_MODULES = {
    "os", "sys", "subprocess", "socket",
    "shutil", "ctypes", "cffi", "pickle",
    "importlib", "multiprocessing", "threading",
    "requests", "urllib"
}

VALID_HASHES_BIN = {}
AVAILABLE_PACKS = {}       # {pack_name: download_raw_url}
MIRROR_PACK_GROUPS = {}    # {mirror_name: [list of pack names]}

OFFICIAL_MIRROR_URL = "https://raw.githubusercontent.com/longtrinh2666/klpython-terminal/refs/heads/mirror/mirror.json"

ver = f"{ENV['ver']}"

def get_normalized_sha256(file_path: str) -> str:
    """
    Chuẩn hóa nội dung file (loại bỏ khác biệt CRLF/LF và khoảng trắng thừa) 
    trước khi tính SHA-256 để chống lệch mã băm giữa Windows và GitHub.
    """
    try:
        with open(file_path, "rb") as f:
            raw_bytes = f.read()
        content = raw_bytes.decode("utf-8", errors="ignore")
    except Exception:
        content = ""

    content = content.replace("\r\n", "\n")
    content = content.strip()
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


# ---------------- Multi-Mirror & Pack Loader Logic ----------------
def load_mirrors():
    """Đọc mirror.txt, tải mirror.json, phân giải qua biến ver để lấy danh sách pack tương ứng"""
    global VALID_HASHES_BIN, AVAILABLE_PACKS, MIRROR_PACK_GROUPS
    VALID_HASHES_BIN = {}
    AVAILABLE_PACKS = {}       
    MIRROR_PACK_GROUPS = {}    

    mirrors_txt_urls = []

    if os.path.exists(MIRROR_LIST_PATH):
        try:
            with open(MIRROR_LIST_PATH, "r", encoding="utf-8") as f:
                mirrors_txt_urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        except Exception as e:
            print("⚠️ Không thể đọc mirror.txt:", e)

    if not mirrors_txt_urls:
        mirrors_txt_urls = [OFFICIAL_MIRROR_URL]
        os.makedirs(os.path.dirname(MIRROR_LIST_PATH), exist_ok=True)
        with open(MIRROR_LIST_PATH, "w", encoding="utf-8") as f:
            f.write(OFFICIAL_MIRROR_URL + "\n")

    for m_json_url in mirrors_txt_urls:
        try:
            fetch_url = m_json_url
            if "github.com" in fetch_url and "/blob/" in fetch_url:
                fetch_url = fetch_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

            resp = requests.get(fetch_url, timeout=6)
            resp.raise_for_status()
            mirror_data = json.loads(resp.text)

            mirror_name = mirror_data.get("name", "Unknown Mirror")
            bin_json_url = mirror_data.get("bin")
            pack_url_base = mirror_data.get("pack-url")
            kernel_mapping = mirror_data.get("kernel", {})

            print(f"🌐 Đang kết nối Mirror: [{mirror_name}]")

            pack_list = []
            target_version_url = kernel_mapping.get(ver)
            
            if target_version_url:
                try:
                    if "github.com" in target_version_url and "/blob/" in target_version_url:
                        target_version_url = target_version_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

                    ver_resp = requests.get(target_version_url, timeout=6)
                    ver_resp.raise_for_status()
                    ver_data = json.loads(ver_resp.text)
                    
                    pack_list = ver_data.get("pack", [])
                    print(f"   ✅ Đã tải danh sách gói cho Kernel v{ver}")
                except Exception as e:
                    print(f"   ⚠️ Không thể tải file cấu hình phiên bản kernel {ver}: {e}")
            else:
                print(f"   ⚠️ Mirror không hỗ trợ phiên bản kernel hiện tại: {ver}")

            MIRROR_PACK_GROUPS[mirror_name] = pack_list

            if not pack_url_base:
                pack_url_base = fetch_url.rsplit("/", 1)[0] + "/bin/"

            if not pack_url_base.endswith("/"):
                pack_url_base += "/"

            for pack_item in pack_list:
                fname = pack_item if pack_item.endswith(".py") else pack_item + ".py"
                download_url = pack_url_base + fname
                
                if fname not in AVAILABLE_PACKS:
                    AVAILABLE_PACKS[fname] = download_url

            if bin_json_url:
                try:
                    fetch_bin_url = bin_json_url
                    if "github.com" in fetch_bin_url and "/blob/" in fetch_bin_url:
                        fetch_bin_url = fetch_bin_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

                    bin_resp = requests.get(fetch_bin_url, timeout=6)
                    bin_resp.raise_for_status()
                    bin_data = json.loads(bin_resp.text)

                    for author, files in bin_data.items():
                        if not isinstance(files, dict):
                            continue
                        if author not in VALID_HASHES_BIN:
                            VALID_HASHES_BIN[author] = {}
                        for fname, sha256_hash in files.items():
                            if fname in VALID_HASHES_BIN[author]:
                                continue
                            VALID_HASHES_BIN[author][fname] = sha256_hash

                    print(f"   ✅ Nạp thành công mã băm từ mirror: {mirror_name}")
                except Exception as e:
                    print(f"   ⚠️ Không thể tải bin.json của mirror {mirror_name}: {e}")

        except Exception as e:
            print(f"⚠️ Không thể kết nối tới mirror URL {m_json_url}: {e}")

    if not VALID_HASHES_BIN:
        print("⚠️ Không có mã băm nào được nạp từ các mirror!")


# ---------------- Verification & Security Helpers ----------------
def verify_bin_file(file_path: str, author: str) -> bool:
    fname = os.path.basename(file_path)
    file_hash = get_normalized_sha256(file_path)
    expected_hash = VALID_HASHES_BIN.get(author, {}).get(fname)

    if file_hash != expected_hash:
        print(f"[ SECURITY WARNING ] Sai lệch mã băm cho file '{fname}'!")
        print(f"  Tính toán: {file_hash}")
        print(f"  Trên mirror: {expected_hash}")
        return False

    return True


def extract_bin_author(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith("author") or stripped.startswith("cfs_author"):
                    parts = stripped.split("=")
                    if len(parts) > 1:
                        return parts[1].strip().strip('"').strip("'")
    except Exception:
        pass
    return "unknown"


# ---------------- Sandbox Environment ----------------
def safe_import(name, *args, **kwargs):
    if name in BLACKLIST_MODULES:
        raise ImportError(f"Import of '{name}' is blocked in sandbox")
    return builtins.__import__(name, *args, **kwargs)


# ---------------- Main Bin Loader ----------------
def load_bin_commands():
    print("=== Secure/Sandbox Multi-Mirror Bin Loader ===")
    os.makedirs(BIN_DIR, exist_ok=True)
    load_mirrors()

    loaded = 0
    for fname in os.listdir(BIN_DIR):
        if not fname.endswith(".py"):
            continue
        
        file_path = os.path.join(BIN_DIR, fname)
        module_name = os.path.splitext(fname)[0]

        author = extract_bin_author(file_path)

        is_trusted = False
        if VALID_HASHES_BIN:
            if verify_bin_file(file_path, author):
                is_trusted = True
            else:
                print(f"[ SECURITY NOTICE ] File '{fname}' không khớp mã băm mirror. Chuyển sang chế độ Sandbox an toàn!")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code_text = f.read()

            if is_trusted:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    if hasattr(module, "register"):
                        try:
                            module.register(commands, ENV)
                        except TypeError:
                            module.register(commands)
                            
                        print(f"[ OK ] Nạp thành công (Toàn quyền): {fname} (Tác giả: {author})")
                        loaded += 1
            else:
                safe_env = {
                    "__builtins__": {
                        "print": print, "len": len, "range": range, "str": str,
                        "int": int, "float": float, "dict": dict, "list": list,
                        "__import__": safe_import,
                    },
                    "ENV": ENV
                }
                exec(compile(code_text, file_path, "exec"), safe_env)
                if "register" in safe_env:
                    try:
                        safe_env["register"](commands, ENV)
                    except TypeError:
                        safe_env["register"](commands)

                    print(f"[ OK ] Nạp thành công (Sandbox an toàn): {fname}")
                    loaded += 1

        except Exception as e:
            print(f"[ ERROR ] Lỗi khi nạp {fname}: {e}")

    print(f"Đã nạp thành công {loaded} lệnh từ bin ✅")
    print("==========================================")


def reload_bin():
    global commands
    commands.clear()
    load_bin_commands()
    print("Bin reloaded ✅")
#________________________________________________________________________

print(r"""
 _________________________________________________________________________ 
|________________________________Welcome__________________________________|
|                       Welcome klpython terminal                         |
|                     ┌──────────────────────────┐                        |
|                     │      __                  │                        |
|                     │     |  \                 │                        |
|                     │      \$$\                │                        |
|                     │       \$$\               │                        |
|                     │        >$$\              │                        |
|                     │       /  $$              │                        |
|                     │      /  $$               │                        |
|                     │     |  $$     _________  │                        |
|                     │      \$$     |         \ │                        |
|                     │              \$$$$$$$$$$ │                        |
|                     └──────────────────────────┘                        |
|          create at 8/1/2026 Shell by longtrinh2666 on github.           |
|_________________________________________________________________________|
""")
load_bin_commands()
print("=== Hardware Info ===")
print("System:", platform.system())
print("Node Name:", platform.node())
print("Release:", platform.release())
print("Version:", platform.version())
print("Machine:", platform.machine())
print("Processor:", platform.processor())
print("CPU cores:", psutil.cpu_count(logical=True))
print("Memory:", round(psutil.virtual_memory().total / (1024**3), 2), "GB")
print("=====================")
while run:
    key = "PWD"
    value = os.getcwd()
    os.environ[key] = value
    PWD = os.environ.get("PWD")
    try:
        user_input = input(f"{username}@{platform.node()}:{PWD}$ ").strip()
    except (EOFError, KeyboardInterrupt):
        break
    if not user_input:
        continue

    try:
        parts = shlex.split(user_input)   # dùng shlex thay vì split()
    except ValueError as e:
        print("E: Invalid syntax:", e)
        continue

    cmd = parts[0].lower()
    args = parts[1:]

    if cmd in commands:
        commands[cmd](args)
    elif cmd.startswith("#"):
        pass
    elif cmd == "bin":
            # bin reload
            if len(args) >= 1 and args[0] == "reload":
                print("🔄 Đang làm mới lại danh sách gói lệnh và nạp lại mô-đun...")
                reload_bin()

            # bin info <command.py>
            elif len(args) >= 2 and args[0] == "info":
                target_file = args[1]
                if not target_file.endswith(".py"):
                    target_file += ".py"
                    
                base_dir = os.path.dirname(os.path.abspath(__file__))
                target_path = os.path.join(base_dir, "bin", target_file)
                
                if not os.path.exists(target_path):
                    print(f"❌ Không tìm thấy gói lệnh '{target_file}' trong thư mục cục bộ.")
                else:
                    try:
                        with open(target_path, "r", encoding="utf-8") as f:
                            text = f.read()
                        
                        author = extract_bin_author(target_path)
                        desc_m = re.search(r'^\s*(?:description|plugin_description)\s*=\s*["\'](.*?)["\']\s*$', text, re.MULTILINE)
                        ver_m = re.search(r'^\s*(?:version|plugin_version)\s*=\s*["\'](.*?)["\']\s*$', text, re.MULTILINE)
                        
                        file_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
                        expected_hash = VALID_HASHES_BIN.get(author, {}).get(target_file)
                        
                        if expected_hash:
                            status = "✅ Hợp lệ (Khớp mã băm SHA-256 chính hãng)" if file_hash == expected_hash else "⚠️ Cảnh báo: Lệch mã băm (Chạy ở chế độ Sandbox)"
                        else:
                            status = "⚠️ Chưa đăng ký trên mirror (Chạy ở chế độ Sandbox)"

                        print(f"\n📦 Gói lệnh: {target_file}")
                        print(f"  👤 Tác giả    : {author}")
                        print(f"  📝 Mô tả      : {desc_m.group(1) if desc_m else 'Không có mô tả'}")
                        print(f"  🏷 Phiên bản  : {ver_m.group(1) if ver_m else 'không có thông tin'}")
                        print(f"  🔒 Trạng thái : {status}")
                        print(f"  🔑 SHA-256    : {file_hash}\n")
                    except Exception as e:
                        print("E: Không thể đọc siêu dữ liệu (metadata) của gói:", e)

            # bin update / refresh (Tải lại metadata từ mirror)
            elif len(args) >= 1 and args[0] in ("update", "refresh"):
                print("🔄 Đang kết nối tới kho lưu trữ Mirror để cập nhật danh sách gói...")
                try:
                    load_mirrors()
                    print("✅ Đã cập nhật kho lưu trữ thành công!")
                except Exception as e:
                    print(f"❌ Không thể cập nhật từ mirror: {e}")

            # bin list
            elif len(args) >= 1 and args[0] in ("list", "search"):
                print("\n=============================================================")
                print(" 📦 DANH SÁCH KHO LƯU TRỮ GÓI LỆNH (KLPython Repositories)")
                print("=============================================================")
                
                installed_files = set(f for f in os.listdir(BIN_DIR) if f.endswith(".py")) if os.path.exists(BIN_DIR) else set()
                all_available = sorted(list(AVAILABLE_PACKS.keys()))
                
                if not all_available:
                    print("⚠️ Chưa có gói nào được đồng bộ từ mirror. Hãy thử gõ 'bin update'.")
                else:
                    for pkg in all_available:
                        is_installed = pkg in installed_files
                        status_str = " [✔ Đã cài đặt]" if is_installed else " [☁ Có sẵn]"
                        print(f"  • {pkg:<20} {status_str}")
                print("=============================================================\n")

            # bin install <pkg> 
            elif len(args) >= 2 and args[0] in ("install", "add"):
                target_pkg = args[1]
                if not target_pkg.endswith(".py"):
                    target_pkg += ".py"

                if target_pkg not in AVAILABLE_PACKS:
                    print(f"❌ [ LỖI ] Gói lệnh '{target_pkg}' không tồn tại trong kho lưu trữ của Mirror!")
                    print("💡 Gõ lệnh 'bin list' để xem danh sách các gói hợp lệ.")
                else:
                    target_path = os.path.join(BIN_DIR, target_pkg)
                    is_update = os.path.exists(target_path)
                    
                    action_name = "Cập nhật" if is_update else "Cài đặt"
                    download_url = AVAILABLE_PACKS[target_pkg]
                    
                    print(f"📥 Đang {action_name.toLowerCase() if 'toLowerCase' in '' else 'tải xuống'} gói '{target_pkg}' từ mirror...")
                    try:
                        resp = requests.get(download_url, timeout=10)
                        resp.raise_for_status()
                        
                        with open(target_path, "wb") as f:
                            f.write(resp.content)
                            
                        print(f"✅ Đã {action_name} thành công gói '{target_pkg}'!")
                        print("🔄 Đang tự động nạp lại hệ thống (reload)...")
                        reload_bin()
                    except Exception as e:
                        print(f"❌ Không thể tải xuống gói lệnh: {e}")

            # bin uninstall / remove <pkg> (Giống pkg remove / apt-get remove)
            elif len(args) >= 2 and args[0] in ("uninstall", "remove", "del"):
                target_pkg = args[1]
                if not target_pkg.endswith(".py") and os.path.exists(os.path.join(BIN_DIR, f"{target_pkg}.py")):
                    target_pkg = f"{target_pkg}.py"
                elif not target_pkg.endswith(".py"):
                    target_pkg += ".py"

                target_path = os.path.join(BIN_DIR, target_pkg)
                if not os.path.exists(target_path):
                    print(f"❌ Gói lệnh '{target_pkg}' chưa được cài đặt trong hệ thống.")
                else:
                    try:
                        os.remove(target_path)
                        print(f"🗑 Đã gỡ bỏ thành công gói lệnh: {target_pkg}")
                        print("🔄 Đang làm mới lại hệ thống...")
                        reload_bin()
                    except Exception as e:
                        print(f"❌ Không thể gỡ bỏ file: {e}")

            # bin installed (Liệt kê các gói đang có trong máy cục bộ)
            elif len(args) >= 1 and args[0] in ("installed", "listbin"):
                print("\n=============================================================")
                print(" 💻 CÁC GÓI LỆNH ĐÃ CÀI ĐẶT CỤC BỘ (Local Packages)")
                print("=============================================================")
                if not os.path.exists(BIN_DIR):
                    print("⚠️ Thư mục bin/ chưa được khởi tạo.")
                else:
                    installed_files = [f for f in os.listdir(BIN_DIR) if f.endswith(".py")]
                    if not installed_files:
                        print("⚠️ Chưa có gói lệnh nào được cài đặt.")
                    else:
                        for f in sorted(installed_files):
                            print(f"  ✔ {f}")
                print("=============================================================\n")
                
            else:
                print("""
    ============================================================
     📦 KLPython Package Manager
    ============================================================
     Hướng dẫn sử dụng lệnh quản lý gói (bin):
       - bin list / search    : Hiển thị tất cả các gói từ mirror (đã cài & chưa cài).
       - bin installed        : Liệt kê các gói đang có trong máy cục bộ.
       - bin install <gói>    : Cài đặt hoặc cập nhật gói lệnh từ kho mirror.
       - bin uninstall <gói>  : Gỡ bỏ một gói lệnh khỏi hệ thống.
       - bin update           : Đồng bộ hóa lại danh sách gói từ máy chủ mirror.
       - bin info <gói>       : Xem thông tin chi tiết, tác giả, trạng thái bảo mật.
       - bin reload           : Tải lại toàn bộ các mô-đun lệnh trong thư mục bin/.
    ============================================================
    """)
            
    else:
        print(f"E:'{cmd}' is not recognized as an internal , program or executor file.")      

