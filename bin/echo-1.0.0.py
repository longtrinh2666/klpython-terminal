author = "longtrinh2666"
version = "1.0.0"
import os

def register(commands, ENV, name="echo"):
    def echo(args):
        if not args:
            print()
            return

        if ">" in args or ">>" in args:
            if ">>" in args:
                idx = args.index(">>")
                filename = args[idx+1] if idx+1 < len(args) else None
                text = " ".join(args[:idx])
                if filename:
                    with open(filename, "a") as f:
                        f.write(text + "\n")
                    print(f"Appended to {filename}")
                else:
                    print("No filename specified")
            else:
                idx = args.index(">")
                filename = args[idx+1] if idx+1 < len(args) else None
                text = " ".join(args[:idx])
                if filename:
                    with open(filename, "w") as f:
                        f.write(text + "\n")
                    print(f"Wrote to {filename}")
                else:
                    print("No filename specified")
        else:
            out_parts = []
            for arg in args:
                if arg.startswith("$"):
                    varname = arg[1:]
                    if varname in ENV:
                        out_parts.append(str(ENV[varname]))
                    elif varname in os.environ:
                        out_parts.append(os.environ[varname])
                    else:
                        out_parts.append("")
                else:
                    out_parts.append(arg)
            print(" ".join(out_parts))

    commands[name] = echo
