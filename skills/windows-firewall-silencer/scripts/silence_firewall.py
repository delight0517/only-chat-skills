#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows Firewall Silencer Script for OmniChat / Only Chat.
Executes diagnosis, rule clearing, and notification silencing.
"""

import sys
import subprocess
import os

def check_admin():
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def silence_notifications():
    print("[*] Setting InboundUserNotification to Disable across all profiles...")
    cmd = ["netsh", "advfirewall", "set", "allprofiles", "settings", "inboundusernotification", "disable"]
    res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if res.returncode == 0:
        print("[+] Successfully disabled firewall popups!")
        return True
    else:
        print("[-] Failed:", res.stderr.strip() or res.stdout.strip())
        return False

def clear_and_allow(exe_path, app_name):
    if not exe_path or not os.path.exists(exe_path):
        print(f"[-] Target executable not found: {exe_path}")
        return False

    base_name = os.path.basename(exe_path)
    print(f"[*] Removing existing conflicting rules for {base_name}...")
    subprocess.run(f'netsh advfirewall firewall delete rule name="{base_name}"', shell=True, capture_output=True)

    print(f"[*] Adding Allow rule for {exe_path}...")
    add_in = f'netsh advfirewall firewall add rule name="{app_name}_Allow_In" dir=in action=allow program="{exe_path}" profile=any'
    add_out = f'netsh advfirewall firewall add rule name="{app_name}_Allow_Out" dir=out action=allow program="{exe_path}" profile=any'
    subprocess.run(add_in, shell=True, capture_output=True)
    subprocess.run(add_out, shell=True, capture_output=True)
    print("[+] Executable permanently allowed through firewall!")
    return True

if __name__ == "__main__":
    if not check_admin():
        print("[!] Script needs administrative privileges to change firewall settings.")
        print("[*] Re-launching with elevation...")
        import ctypes
        params = " ".join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        sys.exit(0)

    if len(sys.argv) > 1 and sys.argv[1] == "allow" and len(sys.argv) > 2:
        exe = sys.argv[2]
        name = sys.argv[3] if len(sys.argv) > 3 else "OmniChat_App"
        clear_and_allow(exe, name)
    else:
        silence_notifications()
