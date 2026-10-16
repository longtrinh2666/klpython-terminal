author = "longtrinh2666"
import tarfile, os

def register(commands, name="tar"):
    def tar_command(args):
        if not args or len(args) < 2:
            print("Usage: tar <tarfile> <file1> <file2> ... | tar -f <output.tar> <folder> | tar ls <tarfile>")
            return

        if args[0] == "-f":
            if len(args) == 3:
                output_name = args[1]
                folder_path = args[2]
                try:
                    with tarfile.open(output_name, "w") as tarf:
                        tarf.add(folder_path, arcname=os.path.basename(folder_path))
                    print(f"Folder '{folder_path}' compressed into '{output_name}' ✅")
                except Exception as e:
                    print("E: Error creating tar:", e)
            else:
                print("Usage: tar -f <output.tar> <folder>")

        elif args[0] == "ls":
            if len(args) == 2:
                tar_path = args[1]
                try:
                    with tarfile.open(tar_path, 'r') as tarf:
                        for member in tarf.getmembers():
                            print(member.name)
                except FileNotFoundError:
                    print("E: Tar file not found")
                except tarfile.ReadError:
                    print("E: Invalid tar file")
            else:
                print("Usage: tar ls <tarfile>")

        else:
            tar_name = args[0]
            files = args[1:]
            try:
                with tarfile.open(tar_name, "w") as tarf:
                    for f in files:
                        tarf.add(f)
                print(f"Files compressed into {tar_name} ✅")
            except Exception as e:
                print("E: Error creating tar:", e)

    commands["tar"] = tar_command
