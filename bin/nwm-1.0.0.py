author = "longtrinh2666"
version = "1.0.0"
import os, platform, socket, subprocess, psutil, requests
import speedtest

def register(commands, name="nwm"):
    def nwm_command(args):
        print("network mgr (type exit to quit)")
        while True:
            user_input_nwm = input("(network mgr mode) >>>").strip().split()
            if not user_input_nwm:
                continue

            cmd = user_input_nwm[0]

            if cmd in ("ipconfig", "ifconfig"):
                print("=== Network Info ===")
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                print("Hostname:", hostname)
                print("IP Address:", ip_address)

                interfaces = psutil.net_if_addrs()
                for interface_name, interface_addresses in interfaces.items():
                    print(f"\nInterface: {interface_name}")
                    for addr in interface_addresses:
                        if addr.family == socket.AF_INET:
                            print("  IPv4:", addr.address)
                        elif addr.family == socket.AF_INET6:
                            print("  IPv6:", addr.address)
                        elif addr.family == psutil.AF_LINK:
                            print("  MAC:", addr.address)

            elif cmd == "wifi":
                if len(user_input_nwm) >= 2 and user_input_nwm[1] == "connect":
                    ssid = user_input_nwm[2] if len(user_input_nwm) > 2 else None
                    password = user_input_nwm[3] if len(user_input_nwm) > 3 else None
                    if ssid:
                        wifi_connect(ssid, password)
                    else:
                        print("Usage: wifi connect <SSID> [password]")
                elif len(user_input_nwm) >= 2 and user_input_nwm[1] == "disconnect":
                    wifi_disconnect()
                elif len(user_input_nwm) >= 2 and user_input_nwm[1] == "scan":
                    wifi_scan()
                else:
                    print("Usage: wifi connect <SSID> [password] | wifi disconnect | wifi scan")

            elif cmd == "ping":
                if len(user_input_nwm) >= 2:
                    host = user_input_nwm[1]
                    subprocess.run(["ping", host])
                else:
                    print("Usage: ping <hostname>")

            elif cmd == "speedtest":
                try:
                    st = speedtest.Speedtest()
                    print("Finding best server...")
                    st.get_best_server()
                    print("Download speed:", round(st.download() / 1e6, 2), "Mbps")
                    print("Upload speed:", round(st.upload() / 1e6, 2), "Mbps")
                    print("Ping:", st.results.ping, "ms")
                except Exception as e:
                    print("E: Cannot run speedtest:", e)

            elif cmd == "publicip":
                try:
                    ip = requests.get("https://api.ipify.org").text
                    print("Public IP:", ip)
                except Exception as e:
                    print("E: Cannot fetch public IP:", e)

            elif cmd == "exit":
                break
            else:
                print(f"E:'{' '.join(user_input_nwm)}' is not recognized as an internal.")

    commands["nwm"] = nwm_command


#__________________________network mgr helper functions____________________________
def wifi_connect(ssid, password=None):
    system = platform.system()
    if system == "Windows":
        if password:
            os.makedirs("profiles", exist_ok=True)
            profile_path = os.path.join("profiles", f"{ssid}.xml")
            profile_xml = f"""<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
  <name>{ssid}</name>
  <SSIDConfig>
    <SSID>
      <name>{ssid}</name>
    </SSID>
  </SSIDConfig>
  <connectionType>ESS</connectionType>
  <connectionMode>auto</connectionMode>
  <MSM>
    <security>
      <authEncryption>
        <authentication>WPA2PSK</authentication>
        <encryption>AES</encryption>
        <useOneX>false</useOneX>
      </authEncryption>
      <sharedKey>
        <keyType>passPhrase</keyType>
        <protected>false</protected>
        <keyMaterial>{password}</keyMaterial>
      </sharedKey>
    </security>
  </MSM>
</WLANProfile>
"""
            with open(profile_path, "w", encoding="utf-8") as f:
                f.write(profile_xml)
            subprocess.run(["netsh", "wlan", "add", "profile", f"filename={profile_path}", "user=all"], check=False)
            subprocess.run(["netsh", "wlan", "connect", f"name={ssid}"], check=False)
        else:
            subprocess.run(["netsh", "wlan", "connect", f"name={ssid}"], check=False)
    elif system == "Linux":
        if password:
            subprocess.run(["nmcli", "d", "wifi", "connect", ssid, "password", password])
        else:
            subprocess.run(["nmcli", "d", "wifi", "connect", ssid])
    elif system == "Darwin":
        device = "Wi-Fi"
        if password:
            subprocess.run(["networksetup", "-setairportnetwork", device, ssid, password])
        else:
            subprocess.run(["networksetup", "-setairportnetwork", device, ssid])
    else:
        print("Unsupported OS")

def wifi_disconnect():
    system = platform.system()
    if system == "Windows":
        subprocess.run(["netsh", "wlan", "disconnect"])
    elif system == "Linux":
        subprocess.run(["nmcli", "d", "disconnect", "wlan0"])
    elif system == "Darwin":
        subprocess.run(["networksetup", "-setairportpower", "Wi-Fi", "off"])
    else:
        print("Unsupported OS")

def wifi_scan():
    system = platform.system()
    if system == "Windows":
        result = subprocess.run(["netsh", "wlan", "show", "networks"], capture_output=True, text=True)
        print(result.stdout)
    elif system == "Linux":
        result = subprocess.run(["nmcli", "-t", "-f", "SSID,SIGNAL", "dev", "wifi"], capture_output=True, text=True)
        print(result.stdout)
    elif system == "Darwin":
        result = subprocess.run(
            ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"],
            capture_output=True, text=True
        )
        print(result.stdout)
    else:
        print("Unsupported OS")
