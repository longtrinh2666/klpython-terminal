author = "longtrinh2666"
version = "1.0.0"
import os, time

def register(commands, name="help"):
    def help_command(args):
        print("""
 __________________________________________________________________________ 
|______________________________Command List________________________________|
| cd <path>        Change current directory or show current path.          |
| dir / ls         List files and folders in current directory.            |
| mkdir <name>     Create a new folder.                                    |
| mkfile <name>    Create an empty file.                                   |
| rm <file>        Delete a file.                                          |
| rm -f <folder>   Delete a folder tree.                                   |
| copy <src> <dst> Copy a file.                                            |
| copy -f <src> <dst> Copy a folder tree.                                  |
| rename/rem <old> <new> Rename a file or folder.                          |
| edit <file>      Edit a text file (':save' to save, ':exit' to discard). |
| echo <text>      Print text to screen.                                   |
| echo <text> > <file>   Write text to file (overwrite).                   |
| echo <text> >> <file>  Append text to file.                              |
| python           Enter Python interactive shell.                         |
| date / time      Show current date and time.                             |
| ver / version    Show shell version.                                     |
| exit             Quit the shell.                                         |
| run <file>       Run a file (.py/.exe/.bat/.com/.sh/.kl).                |
| zip <zip> <files...>   Compress files into a zip archive.                |
| unzip <zip> [dst]     Extract a zip archive.                             |
| tar <tar> <files...>   Compress files into a tar archive.                |
| untar <tar> [dst]     Extract a tar archive.                             |
| zip -f <zip> <folder> Compress a folder into zip.                        |
| tar -f <tar> <folder> Compress a folder into tar.                        |
| zip ls <zip>     List contents of a zip archive.                         |
| tar ls <tar>     List contents of a tar archive.                         |
| clear / cls      Clear the console screen.                               |
| nwm              Enter network manager mode.                             |
|   ipconfig/ifconfig   Show network interfaces and IP addresses.          |
|   wifi scan           Scan for available Wi-Fi networks.                 |
|   wifi connect <SSID> [password] Connect to Wi-Fi (creates profile).     |
|   wifi disconnect     Disconnect from Wi-Fi.                             |
|   ping <host>         Ping a hostname or IP.                             |
|   speedtest           Run a network speed test.                          |
|   publicip            Show current public IP address.                    |
| help             Show this help information.                             |
|__________________________________________________________________________|
""")

    commands["help"] = help_command
