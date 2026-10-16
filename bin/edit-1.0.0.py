author = "longtrinh2666"
import os

def register(commands, name="edit"):
    def edit_command(args):
        if not args:
            print("Usage: edit <filename>")
            return
        filename = args[0]
        edit_file(filename)

    commands["edit"] = edit_command


def edit_file(filename):
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
        else:
            lines = []

        cursor = 0
        while True:
            print("\n--- File content ---")
            for i, line in enumerate(lines):
                marker = "->" if i == cursor else "  "
                print(f"{marker} {i+1}: {line.rstrip()}")

            cmd = input("(edit mode) >>> ").strip()

            if cmd == ":up":
                cursor = max(0, cursor-1)
            elif cmd == ":down":
                cursor = min(len(lines)-1, cursor+1)
            elif cmd.startswith(":edit"):
                parts = cmd.split()
                if len(parts) == 2 and parts[1].isdigit():
                    n = int(parts[1]) - 1
                    if 0 <= n < len(lines):
                        new_text = input(f"New content for line {n+1}: ")
                        lines[n] = new_text + "\n"
                    else:
                        print("E: Invalid line number")
                else:
                    print("Usage: :edit <line_number>")
            elif cmd == ":add":
                new_text = input("New line: ")
                lines.append(new_text + "\n")
            elif cmd == ":save":
                with open(filename, "w", encoding="utf-8") as f:
                    f.writelines(lines)
                print("File saved ✅")
            elif cmd == ":exit":
                print("Exit edit mode ❌")
                break
            else:
                print("Commands: :up, :down, :edit <n>, :add, :save, :exit")
    except Exception as e:
        print("E: Error editing file:", e)
