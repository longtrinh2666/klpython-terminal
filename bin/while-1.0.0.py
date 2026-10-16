author = "longtrinh2666"

def register(commands, ENV):
    def while_cmd(args, block=None):
        if not args or not block:
            print("Usage: while <condition> (Used in .kl scripts)")
            return

        cond_raw = " ".join(args).strip()

        def eval_cond():
            cond_str = cond_raw
            for k, v in ENV.items():
                cond_str = cond_str.replace(f"${k}", str(v))

            for op in ["==", "!=", ">=", "<=", ">", "<"]:
                if op in cond_str:
                    parts = cond_str.split(op, 1)
                    left = parts[0].strip().strip('"').strip("'")
                    right = parts[1].strip().strip('"').strip("'")

                    if op == "==": return left == right
                    if op == "!=": return left != right
                    if op == ">": return float(left) > float(right) if left.replace('.','',1).isdigit() and right.replace('.','',1).isdigit() else left > right
                    if op == "<": return float(left) < float(right) if left.replace('.','',1).isdigit() and right.replace('.','',1).isdigit() else left < right
            return False

        # Thực thi vòng lặp lặp lại khối lệnh block
        max_loops = 1000  # Tránh lặp vô tận gây treo terminal
        count = 0
        while eval_cond() and count < max_loops:
            for line in block:
                line = line.rstrip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                sub_cmd, sub_args = parts[0], parts[1:]
                if sub_cmd in commands:
                    commands[sub_cmd](sub_args)
            count += 1

    commands["while"] = while_cmd