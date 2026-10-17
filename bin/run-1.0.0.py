author = "longtrinh2666"
import os, sys, subprocess, platform

def register(commands, ENV, name="run"):
    def run_command(args):
        if not args:
            print("Usage: run <filename>")
            return
        filename = args[0]
        run_file(filename, commands, ENV)

    commands["run"] = run_command
    commands["bash"] = run_command
    commands["./"] = run_command


def run_file(filename, commands, ENV):
    ext = os.path.splitext(filename)[1].lower()
    try:
        if ext == ".py":
            subprocess.run([sys.executable, filename])
        elif ext in (".exe", ".com") and platform.system() == "Windows":
            subprocess.run([filename])
        elif ext == ".bat" and platform.system() == "Windows":
            subprocess.run([filename], shell=True)
        elif ext == ".sh":
            if platform.system() == "Linux":
                subprocess.run(["bash", filename])
            else:
                print("Unsupported OS for .sh")
        elif ext == ".kl":
            if not os.path.exists(filename):
                print("File not found:", filename)
                return
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Hàm thực thi danh sách dòng lệnh bên trong một khối (block)
            # Trả về tín hiệu điều khiển: "break", "continue", hoặc None
            def execute_block(block_lines):
                i_b = 0
                while i_b < len(block_lines):
                    line = block_lines[i_b].rstrip()
                    if not line or line.startswith("#"):
                        i_b += 1
                        continue

                    # Bắt từ khóa break / continue trong block
                    if line == "break":
                        return "break"
                    if line == "continue":
                        return "continue"

                    # Hỗ trợ cấu trúc if lồng nhau trong block nếu cần
                    if line.startswith("if "):
                        cond = line[3:].split(":", 1)[0].strip()
                        sub_block = []
                        i_b += 1
                        while i_b < len(block_lines) and block_lines[i_b].startswith("    "):
                            sub_block.append(block_lines[i_b].lstrip())
                            i_b += 1
                        
                        # Gom các nhánh elif/else tiếp theo nếu có
                        elif_branches = []
                        else_block = None
                        while i_b < len(block_lines):
                            next_l = block_lines[i_b].strip()
                            if next_l.startswith("elif "):
                                e_cond = next_l[5:].split(":", 1)[0].strip()
                                e_sub = []
                                i_b += 1
                                while i_b < len(block_lines) and block_lines[i_b].startswith("    "):
                                    e_sub.append(block_lines[i_b].lstrip())
                                    i_b += 1
                                elif_branches.append((e_cond, e_sub))
                            elif next_l == "else:":
                                else_sub = []
                                i_b += 1
                                while i_b < len(block_lines) and block_lines[i_b].startswith("    "):
                                    else_sub.append(block_lines[i_b].lstrip())
                                    i_b += 1
                                else_block = else_sub
                            else:
                                break

                        res = commands["if"]([cond], sub_block, elif_branches, else_block, ENV)
                        if res in ("break", "continue"):
                            return res
                        continue

                    # Gán biến trong block
                    if "=" in line and not line.startswith("export"):
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip()
                        ENV[key] = value
                        os.environ[key] = value
                        i_b += 1
                        continue

                    # Lệnh thường
                    parts = line.split()
                    cmd, args_sub = parts[0], parts[1:]
                    if cmd in commands:
                        # Đặc biệt nếu lệnh là hàm trả về trạng thái (như while/if)
                        if cmd in ("if", "while"):
                            # Xử lý riêng hoặc gọi qua command tương ứng
                            pass
                        commands[cmd](args_sub)
                    else:
                        print(f"E: Unknown command '{cmd}' in script")
                    i_b += 1
                return None

            i = 0
            while i < len(lines):
                line = lines[i].rstrip()
                if not line or line.startswith("#"):
                    i += 1
                    continue

                # 1. Phát hiện khối lệnh if ... :
                if line.startswith("if "):
                    cond = line[3:].split(":", 1)[0].strip()
                    block = []
                    i += 1
                    while i < len(lines) and lines[i].startswith("    "):
                        block.append(lines[i].lstrip())
                        i += 1

                    # Quét các nhánh elif / else ngay bên dưới nếu có
                    elif_branches = []
                    else_block = None
                    while i < len(lines):
                        next_line = lines[i].strip()
                        if next_line.startswith("elif "):
                            e_cond = next_line[5:].split(":", 1)[0].strip()
                            e_sub = []
                            i += 1
                            while i < len(lines) and lines[i].startswith("    "):
                                e_sub.append(lines[i].lstrip())
                                i += 1
                            elif_branches.append((e_cond, e_sub))
                        elif next_line == "else:":
                            else_sub = []
                            i += 1
                            while i < len(lines) and lines[i].startswith("    "):
                                else_sub.append(lines[i].lstrip())
                                i += 1
                            else_block = else_sub
                        else:
                            break

                    commands["if"]([cond], block, elif_branches, else_block, ENV)
                    continue

                # 2. Phát hiện khối lệnh while ..aauthor = "longtrinh2666"
import os, sys, subprocess, platform

def register(commands, ENV, name="run"):
    def run_command(args):
        if not args:
            print("Usage: run <filename>")
            return
        filename = args[0]
        run_file(filename, commands, ENV)

    commands["run"] = run_command
    commands["bash"] = run_command
    commands["./"] = run_command


def detect_file_type_by_shebang(filename):
    """
    Đọc từ dòng 1 đến dòng 5 của file để tìm shebang (#!),
    giúp nhận diện loại file mà không cần quan tâm đến phần đuôi mở rộng.
    """
    try:
        with open(filename, "r", encoding="utf-8", errors="ignore") as f:
            for _ in range(5):
                line = f.readline()
                if not line:
                    break
                stripped = line.strip()
                if stripped.startswith("#!"):
                    shebang = stripped[2:].strip().lower()
                    
                    # Kiểm tra các dạng bash / sh
                    if "bash" in shebang or shebang == "/bin/sh" or shebang == "sh":
                        return "shell"
                    
                    # Kiểm tra shebang riêng cho KLPython script (.kl)
                    if "bin/run" in shebang or shebang.endswith("/run"):
                        return "klscript"
                    
                    # Các loại khác có thể mở rộng sau (ví dụ python)
                    if "python" in shebang:
                        return "python"
    except Exception:
        pass
    return None

def run_file(filename, commands, ENV):
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    ext = os.path.splitext(filename)[1].lower()
    
    # 1. Quét shebang ở đầu file (1-5 dòng đầu) để nhận diện file không cần đuôi
    shebang_type = detect_file_type_by_shebang(filename)

    try:
        # Nếu shebang chỉ định rõ là kịch bản KLPython (#! /bin/run)
        if shebang_type == "klscript" or ext == ".kl":
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # (Giữ nguyên toàn bộ logic phân tích khối block, if, while, break, continue như bản trước)
            def execute_block(block_lines):
                i_b = 0
                while i_b < len(block_lines):
                    line = block_lines[i_b].rstrip()
                    if not line or line.startswith("#"):
                        i_b += 1
                        continue
                    if line == "break": return "break"
                    if line == "continue": return "continue"

                    if line.startswith("if "):
                        cond = line[3:].split(":", 1)[0].strip()
                        sub_block = []
                        i_b += 1
                        while i_b < len(block_lines) and block_lines[i_b].startswith("    "):
                            sub_block.append(block_lines[i_b].lstrip())
                            i_b += 1
                        
                        elif_branches = []
                        else_block = None
                        while i_b < len(block_lines):
                            next_l = block_lines[i_b].strip()
                            if next_l.startswith("elif "):
                                e_cond = next_l[5:].split(":", 1)[0].strip()
                                e_sub = []
                                i_b += 1
                                while i_b < len(block_lines) and block_lines[i_b].startswith("    "):
                                    e_sub.append(block_lines[i_b].lstrip())
                                    i_b += 1
                                elif_branches.append((e_cond, e_sub))
                            elif next_l == "else:":
                                else_sub = []
                                i_b += 1
                                while i_b < len(block_lines) and block_lines[i_b].startswith("    "):
                                    else_sub.append(block_lines[i_b].lstrip())
                                    i_b += 1
                                else_block = else_sub
                            else:
                                break

                        res = commands["if"]([cond], sub_block, elif_branches, else_block, ENV)
                        if res in ("break", "continue"): return res
                        continue

                    if "=" in line and not line.startswith("export"):
                        key, value = line.split("=", 1)
                        ENV[key.strip()] = value.strip()
                        os.environ[key.strip()] = value.strip()
                        i_b += 1
                        continue

                    parts = line.split()
                    cmd, args_sub = parts[0], parts[1:]
                    if cmd in commands:
                        commands[cmd](args_sub)
                    else:
                        print(f"E: Unknown command '{cmd}' in script")
                    i_b += 1
                return None

            i = 0
            while i < len(lines):
                line = lines[i].rstrip()
                if not line or line.startswith("#"):
                    i += 1
                    continue

                if line.startswith("if "):
                    cond = line[3:].split(":", 1)[0].strip()
                    block = []
                    i += 1
                    while i < len(lines) and lines[i].startswith("    "):
                        block.append(lines[i].lstrip())
                        i += 1

                    elif_branches = []
                    else_block = None
                    while i < len(lines):
                        next_line = lines[i].strip()
                        if next_line.startswith("elif "):
                            e_cond = next_line[5:].split(":", 1)[0].strip()
                            e_sub = []
                            i += 1
                            while i < len(lines) and lines[i].startswith("    "):
                                e_sub.append(lines[i].lstrip())
                                i += 1
                            elif_branches.append((e_cond, e_sub))
                        elif next_line == "else:":
                            else_sub = []
                            i += 1
                            while i < len(lines) and lines[i].startswith("    "):
                                else_sub.append(lines[i].lstrip())
                                i += 1
                            else_block = else_sub
                        else:
                            break

                    commands["if"]([cond], block, elif_branches, else_block, ENV)
                    continue

                if line.startswith("while "):
                    cond = line[6:].split(":", 1)[0].strip()
                    block = []
                    i += 1
                    while i < len(lines) and lines[i].startswith("    "):
                        block.append(lines[i].lstrip())
                        i += 1

                    commands["while"]([cond], block, ENV, execute_block)
                    continue

                if "=" in line and not line.startswith("export"):
                    key, value = line.split("=", 1)
                    ENV[key.strip()] = value.strip()
                    os.environ[key.strip()] = value.strip()
                    i + 1
                    continue

                parts = line.split()
                cmd, args = parts[0], parts[1:]
                if cmd in commands:
                    commands[cmd](args)
                else:
                    print(f"E: Unknown command '{cmd}' in script")
                i += 1

        # 2. Xử lý file Shell script qua shebang hoặc đuôi .sh
        elif shebang_type == "shell" or ext == ".sh":
            if platform.system() == "Linux":
                subprocess.run(["bash", filename])
            else:
                print("Unsupported OS for shell scripts")

        # 3. Xử lý file Python qua shebang hoặc đuôi .py
        elif shebang_type == "python" or ext == ".py":
            subprocess.run([sys.executable, filename])

        # 4. Các định dạng theo đuôi thông thường khác
        elif ext in (".exe", ".com") and platform.system() == "Windows":
            subprocess.run([filename])
        elif ext == ".bat" and platform.system() == "Windows":
            subprocess.run([filename], shell=True)
        else:
            print(f"E: Unsupported or unrecognized file type for '{filename}'")

    except Exception as e:
        print("E: Error running file:", e). :
                if line.startswith("while "):
                    cond = line[6:].split(":", 1)[0].strip()
                    block = []
                    i += 1
                    while i < len(lines) and lines[i].startswith("    "):
                        block.append(lines[i].lstrip())
                        i += 1

                    commands["while"]([cond], block, ENV, execute_block)
                    continue

                # Gán biến cấp ngoài
                if "=" in line and not line.startswith("export"):
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    ENV[key] = value
                    os.environ[key] = value
                    i += 1
                    continue

                # Lệnh thông thường
                parts = line.split()
                cmd, args = parts[0], parts[1:]
                if cmd in commands:
                    commands[cmd](args)
                else:
                    print(f"E: Unknown command '{cmd}' in script")
                i += 1
        else:
            print(f"E: Unsupported file type '{ext}'")
    except Exception as e:
        print("E: Error running file:", e)