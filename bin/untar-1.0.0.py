author = "longtrinh2666"
version = "1.0.0"
import tarfile

def register(commands, name="untar"):
    def untar_command(args):
        if not args:
            print("Usage: untar <tarfile> [destination]")
            return
        tar_path = args[0]
        extract_to = args[1] if len(args) > 1 else "."
        try:
            with tarfile.open(tar_path, "r") as tarf:
                tarf.extractall(extract_to)
            print(f"File {tar_path} extracted successfully to {extract_to} ✅")
        except Exception as e:
            print("E: Error extracting tar:", e)

    commands["untar"] = untar_command
