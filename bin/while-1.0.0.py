author = "longtrinh2666"
version = "1.0.0"
import shlex

def register(commands, ENV):
    def eval_condition(cond_raw, env):
        cond_str = cond_raw.strip()
        
        # 🟢 Hỗ trợ các từ khóa vòng lặp vô tận
        if cond_str.lower() in ("true", "1", "yes", "on"): 
            return True
        if cond_str.lower() in ("false", "0", "no", "off"): 
            return False

        # Thay thế biến từ môi trường ENV nếu có
        for k, v in env.items():
            cond_str = cond_str.replace(f"${k}", str(v))

        # Đánh giá các toán tử so sánh
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
        max_loops = 10000  # Giới hạn an toàn chống treo vòng lặp
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
                    break # Thoát vòng lặp hiện tại, chuyển sang chu kỳ kế tiếp

                # Sử dụng shlex.split để xử lý an toàn các tham số có khoảng trắng (như read -p)
                parts = shlex.split(line)
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