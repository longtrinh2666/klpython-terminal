author = "longtrinh2666"

def register(commands, ENV):
    def eval_condition(cond_raw, env):
        cond_str = cond_raw.strip()
        
        if cond_str.lower() in ("true", "1", "yes"): return True
        if cond_str.lower() in ("false", "0", "no"): return False

        for k, v in env.items():
            cond_str = cond_str.replace(f"${k}", str(v))

        for op in ["==", "!=", ">=", "<=", ">", "<"]:
            if op in cond_str:
                parts = cond_str.split(op, 1)
                left = parts[0].strip().strip('"').strip("'")
                right = parts[1].strip().strip('"').strip("'")

                is_num = left.replace('.', '', 1).isdigit() and right.replace('.', '', 1).isdigit()
                if op == "==": return left == right
                elif op == "!=": return left != right
                elif op == ">": return (float(left) > float(right)) if is_num else (left > right)
                elif op == "<": return (float(left) < float(right)) if is_num else (left < right)
                elif op == ">=": return (float(left) >= float(right)) if is_num else (left >= right)
                elif op == "<=": return (float(left) <= float(right)) if is_num else (left <= right)
        return False

    def while_cmd(args, block=None, custom_env=None, block_executor=None):
        env_to_use = custom_env if custom_env is not None else ENV
        if not args or not block:
            print("Usage: while <condition> (Used in .kl scripts)")
            return

        cond_raw = " ".join(args).strip()
        max_loops = 10000  # Chống treo vòng lặp vô tận
        count = 0

        while eval_condition(cond_raw, env_to_use) and count < max_loops:
            should_break = False
            for line in block:
                line = line.rstrip()
                if not line or line.startswith("#"):
                    continue
                
                if line == "break":
                    should_break = True
                    break
                if line == "continue":
                    break # Bỏ qua phần còn lại của vòng lặp hiện tại, quay lại kiểm tra điều kiện

                parts = line.split()
                if parts:
                    sub_cmd, sub_args = parts[0], parts[1:]
                    if sub_cmd in commands:
                        commands[sub_cmd](sub_args)
                    else:
                        print(f"E: Unknown command '{sub_cmd}' in while-block")

            if should_break:
                break
            count += 1

    commands["while"] = while_cmd