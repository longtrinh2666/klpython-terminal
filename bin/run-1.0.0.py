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

            i = 0
            while i < len(lines):
                line = lines[i].rstrip()
                if not line or line.startswith("#"):
                    i += 1
                    continue

                # detect if block
                if line.startswith("if "):
                    cond = line[3:].split(":", 1)[0].strip()
                    block = []
                    i += 1
                    while i < len(lines) and lines[i].startswith("    "):
                        block.append(lines[i].lstrip())
                        i += 1
                    commands["if"]([cond], block)
                    continue

                # detect while block
                if line.startswith("while "):
                    cond = line[6:].split(":", 1)[0].strip()
                    block = []
                    i += 1
                    while i < len(lines) and lines[i].startswith("    "):
                        block.append(lines[i].lstrip())
                        i += 1
                    commands["while"]([cond], block)
                    continue

                # gán biến: chỉ khi dòng KHÔNG bắt đầu bằng if/while
                if "=" in line and not line.startswith("export"):
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    ENV[key] = value
                    os.environ[key] = value
                    print(f"Exported {key}={value}")
                    i += 1
                    continue

                # lệnh thường
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
