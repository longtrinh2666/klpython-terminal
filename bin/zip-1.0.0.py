author = "longtrinh2666"
import zipfile, shutil, os

def register(commands, name="zip"):
    def zip_command(args):
        if not args or len(args) < 2:
            print("Usage: zip <zipfile> <file1> <file2> ... | zip -f <output.zip> <folder> | zip ls <zipfile>")
            return

        if args[0] == "-f":
            if len(args) == 3:
                output_name = args[1].replace(".zip", "")
                folder_path = args[2]
                try:
                    shutil.make_archive(output_name, 'zip', folder_path)
                    print(f"Folder '{folder_path}' compressed into '{output_name}.zip' ✅")
                except Exception as e:
                    print("E: Error zipping folder:", e)
            else:
                print("Usage: zip -f <output.zip> <folder>")

        elif args[0] == "ls":
            if len(args) == 2:
                zip_path = args[1]
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zipf:
                        for name in zipf.namelist():
                            print(name)
                except FileNotFoundError:
                    print("E: Zip file not found")
                except zipfile.BadZipFile:
                    print("E: Invalid zip file")
            else:
                print("Usage: zip ls <zipfile>")

        else:
            zip_name = args[0]
            files = args[1:]
            try:
                with zipfile.ZipFile(zip_name, 'w') as zipf:
                    for f in files:
                        zipf.write(f)
                print(f"Files compressed into {zip_name} ✅")
            except Exception as e:
                print("E: Error creating zip:", e)

    commands["zip"] = zip_command
