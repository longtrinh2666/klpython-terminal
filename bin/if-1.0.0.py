author = "longtrinh2666"

import shlex

def register(commands, ENV):
    def eval_condition(cond_raw, env):
        cond_str = cond_raw.strip()
        
        # Hỗ trợ từ khóa cơ bản true/false
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

    def if_cmd(args, block=None, elif_branches=None, else_block=None, custom_env=None):
        env_to_use = custom_env if custom_env is not None else ENV
        if not args:
            print("Usage: if <condition>")
            return

        cond_str = " ".join(args).replace("then", "").strip()
        
        # 1. Nhánh IF chính
        if eval_condition(cond_str, env_to_use):
            if block:
                for line in block:
                    line = line.rstrip()
                    if not line or line.startswith("#"): continue
                    if line == "break": return "break"
                    if line == "continue": return "continue"
                    parts = shlex.split(line)
                    sub_cmd, sub_args = parts[0], parts[1:]
                    if sub_cmd in commands:
                        commands[sub_cmd](sub_args)
            return

        # 2. Nhánh ELIF
        if elif_branches:
            for e_cond, e_block in elif_branches:
                if eval_condition(e_cond, env_to_use):
                    if e_block:
                        for line in e_block:
                            line = line.rstrip()
                            if not line or line.startswith("#"): continue
                            if line == "break": return "break"
                            if line == "continue": return "continue"
                            parts = shlex.split(line)
                            sub_cmd, sub_args = parts[0], parts[1:]
                            if sub_cmd in commands:
                                commands[sub_cmd](sub_args)
                    return

        # 3. Nhánh ELSE
        if else_block:
            for line in else_block:
                line = line.rstrip()
                if not line or line.startswith("#"): continue
                if line == "break": return "break"
                if line == "continue": return "continue"
                parts = shlex.split(line)
                sub_cmd, sub_args = parts[0], parts[1:]
                if sub_cmd in commands:
                    commands[sub_cmd](sub_args)

    commands["if"] = if_cmd