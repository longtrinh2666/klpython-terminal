author = "longtrinh2666"
version = "1.0.0"
import os

def register(commands, ENV):
    def find_cmd(args):
        if not args:
            print("Usage: find <filename>")
            return

        target_name = args[0]
        curr_dir = ENV.get("current_dir", os.getcwd())
        
        found_matches = []

        # Duyệt qua các thư mục và file từ thư mục hiện tại
        for root, dirs, files in os.walk(curr_dir):
            # Tìm kiếm trong tên file và tên thư mục
            for name in files + dirs:
                if target_name in name:
                    rel_path = os.path.relpath(os.path.join(root, name), curr_dir)
                    found_matches.append(rel_path)

        if found_matches:
            print(f"Found {len(found_matches)} match(es) for '{target_name}':")
            for match in found_matches:
                print(f"  {match}")
        else:
            print(f"No results found for '{target_name}'")

    # Đăng ký lệnh 'find' vào hệ thống commands của terminal
    commands["find"] = find_cmd