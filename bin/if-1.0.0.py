author = "longtrinh2666"
import os

def register(commands, ENV):
    def if_cmd(args, block=None):
        if not args:
            print("Usage: if <condition> [then <command>]")
            return

        # 1. Lấy điều kiện băm từ args
        cond_str = " ".join(args).replace("then", "").strip()

        # Thay thế biến $VAR từ ENV nếu có
        for k, v in ENV.items():
            cond_str = cond_str.replace(f"${k}", str(v))

        # Đánh giá điều kiện đơn giản (==, !=, >, <)
        condition_met = False
        for op in ["==", "!=", ">=", "<=", ">", "<"]:
            if op in cond_str:
                parts = cond_str.split(op, 1)
                left = parts[0].strip().strip('"').strip("'")
                right = parts[1].strip().strip('"').strip("'")

                if op == "==": condition_met = (left == right)
                elif op == "!=": condition_met = (left != right)
                elif op == ">": condition_met = (float(left) > float(right) if left.replace('.','',1).isdigit() and right.replace('.','',1).isdigit() else left > right)
                elif op == "<": condition_met = (float(left) < float(right) if left.replace('.','',1).isdigit() and right.replace('.','',1).isdigit() else left < right)
                break

        if condition_met:
            # Nếu truyền vào một khối block từ file script (.kl)
            if block:
                for line in block:
                    line = line.rstrip()
                    if not line or line.startswith("#"):
                        continue
                    parts = line.split()
                    sub_cmd, sub_args = parts[0], parts[1:]
                    if sub_cmd in commands:
                        commands[sub_cmd](sub_args)
                    else:
                        print(f"E: Unknown command '{sub_cmd}' in if-block")
            else:
                # Nếu gọi inline từ terminal: if $A == 1 then echo Yes
                if "then" in args:
                    then_idx = args.index("then")
                    sub_parts = args[then_idx + 1:]
                    if sub_parts and sub_parts[0] in commands:
                        commands[sub_parts[0]](sub_parts[1:])

    commands["if"] = if_cmd