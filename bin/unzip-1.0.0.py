author = "longtrinh2666"
version = "1.0.0"
import zipfile

def register(commands, name="unzip"):
    def unzip_command(args):
        if not args:
            print("Usage: unzip <zipfile> [destination]")
            return
        zip_path = args[0]
        extract_to = args[1] if len(args) > 1 else "."
        try:
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                zipf.extractall(extract_to)
            print(f"File {zip_path} extracted successfully to {extract_to} ✅")
        except Exception as e:
            print("E: Error extracting zip:", e)

    commands["unzip"] = unzip_command
