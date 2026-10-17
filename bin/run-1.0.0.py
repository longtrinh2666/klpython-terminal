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


def detect_file_type_by_shebang(filename):
    try:
        with open(filename, "r", encoding="utf-8", errors="ignore") as f:
            for _ in range(5):
                line = f.readline()
                if not line:
                    break
                stripped = line.strip()
                if stripped.startswith("#!"):
                    shebang = stripped[2:].strip().lower()
                    if "bash" in shebang or shebang == "/bin/sh" or shebang == "sh":
                        return "shell"
                    if "bin/run" in shebang or shebang.endswith("/run"):
                        return "klscript"
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
    shebang_type = detect_file_type_by_shebang(filename)

    try:
        if shebang_type == "klscript" or ext == ".kl":
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()

            def execute_block(block_lines):
                i_b = 0
                while i_b < len(block_lines):
                    line = block_lines[i_b].rstrip()
                    stripped_line = line.strip()
                    
                    # Bỏ qua dòng trống hoặc chú thích
                    if not stripped_line or stripped_line.startswith("#"):
                        i_b += 1
                        continue

                    # 🛡️ CHẶN CÁC TỪ KHÓA CẤU TRÚC KHÔNG ĐƯỢC COI LÀ LỆNH THƯỜNG
                    if stripped_line in ("break", "continue") or stripped_line.startswith("elif ") or stripped_line.startswith("else"):
                        i_b += 1
                        continue

                    if stripped_line == "break": 
                        return "break"
                    if stripped_line == "continue": 
                        return "continue"

                    # Xử lý khối if lồng nhau trong block
                    if stripped_line.startswith("if "):
                        cond = stripped_line[3:].split(":", 1)[0].strip()
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
                        if res in ("break", "continue"): 
                            return res
                        continue

                    # Xử lý gán biến trong block
                    if "=" in stripped_line and not stripped_line.startswith("export"):
                        key, value = stripped_line.split("=", 1)
                        ENV[key.strip()] = value.strip()
                        os.environ[key.strip()] = value.strip()
                        i_b += 1
                        continue

                    # Thực thi lệnh thông thường
                    parts = stripped_line.split()
                    if parts:
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
                stripped_line = line.strip()
                
                if not stripped_line or stripped_line.startswith("#"):
                    i += 1
                    continue

                # 1. Phát hiện khối lệnh if
                if stripped_line.startswith("if "):
                    cond = stripped_line[3:].split(":", 1)[0].strip()
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

                # 2. Phát hiện khối lệnh while
                if stripped_line.startswith("while "):
                    cond = stripped_line[6:].split(":", 1)[0].strip()
                    block = []
                    i += 1
                    while i < len(lines) and lines[i].startswith("    "):
                        block.append(lines[i].lstrip())
                        i += 1

                    commands["while"]([cond], block, ENV, execute_block)
                    continue

                # Gán biến cấp ngoài
                if "=" in stripped_line and not stripped_line.startswith("export"):
                    key, value = stripped_line.split("=", 1)
                    ENV[key.strip()] = value.strip()
                    os.environ[key.strip()] = value.strip()
                    i += 1
                    continue

                # Lệnh thông thường ở cấp ngoài
                parts = stripped_line.split()
                if parts:
                    cmd, args = parts[0], parts[1:]
                    if cmd in commands:
                        commands[cmd](args)
                    else:
                        print(f"E: Unknown command '{cmd}' in script")
                i += 1

        elif shebang_type == "shell" or ext == ".sh":
            if platform.system() == "Linux":
                subprocess.run(["bash", filename])
            else:
                print("Unsupported OS for shell scripts")

        elif shebang_type == "python" or ext == ".py":
            subprocess.run([sys.executable, filename])

        elif ext in (".exe", ".com") and platform.system() == "Windows":
            subprocess.run([filename])
        elif ext == ".bat" and platform.system() == "Windows":
            subprocess.run([filename], shell=True)
        else:
            print(f"E: Unsupported or unrecognized file type for '{filename}'")

    except Exception as e:
        print("E: Error running file:", e)