# utility/main.py
import platform
import psutil
import schedule
import time
import json
import requests
import configparser
import os

# --- Configuration ---
config = configparser.ConfigParser()
config.read('config.ini')
REPORTING_INTERVAL_SECONDS = int(config.get('utility', 'reporting_interval_minutes', fallback='15')) * 60
API_ENDPOINT = config.get('utility', 'api_endpoint', fallback='https://dummy.com/api/report')
MACHINE_ID = config.get('utility', 'machine_id', fallback='default_machine_id') # Ideally, generate a unique ID

# --- Platform-Specific Checks ---
def get_disk_encryption_status():
    system = platform.system()
    if system == "Darwin":  # macOS
        try:
            result = os.popen("diskutil info / | grep 'FileVault:'").read().strip()
            return "Encrypted" in result
        except Exception:
            return "Unknown"
    elif system == "Windows":
        try:
            result = os.popen("powershell -Command \"Get-BitLockerVolume -MountPoint 'C:' | Select-Object -ExpandProperty EncryptionPercentage\"").read().strip()
            return result == "100"
        except Exception:
            return "Unknown"
    elif system == "Linux":
        try:
            if os.path.exists("/sys/fs/ecryptfs"):
                return True
            result = os.popen("sudo cryptsetup isLuks /dev/sda* 2>/dev/null").read().strip() # Adjust /dev/sda* as needed
            return "is active" in result
        except Exception:
            return "Unknown"
    return "Unsupported OS"

def get_os_update_status():
    system = platform.system()
    if system == "Darwin":
        try:
            result = os.popen("softwareupdate -l | grep -E 'recommended|important'").read().strip()
            return "Up to date" if not result else "Updates available"
        except Exception:
            return "Unknown"
    elif system == "Windows":
        try:
            result = os.popen("powershell -Command \"(Get-HotFix | Measure-Object).Count\"").read().strip() # Basic check, needs refinement
            return f"{result} updates installed"
        except Exception:
            return "Unknown"
    elif system == "Linux":
        try:
            # This is highly distribution-dependent. Returning a generic status for now.
            return "Checking for updates..."
        except Exception:
            return "Unknown"
    return "Unsupported OS"

def get_antivirus_status():
    system = platform.system()
    if system == "Darwin":
        try:
            result = os.popen("mdfind 'kMDItemKind == \"Application\"' | grep -i 'antivirus'").read().strip()
            return "Antivirus likely present" if result else "Antivirus not detected"
        except Exception:
            return "Unknown"
    elif system == "Windows":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Security Center")
            value, _ = winreg.QueryValueEx(key, "AntiVirusProduct")
            return f"Antivirus: {value}" if value else "Antivirus not detected"
        except Exception:
            return "Unknown"
    elif system == "Linux":
        try:
            result = os.popen("dpkg --get-selections | grep -i 'clamav'").read().strip()
            return "ClamAV detected" if "clamav" in result else "Antivirus not readily detected"
        except Exception:
            return "Unknown"
    return "Unsupported OS"

def get_inactivity_sleep_settings():
    system = platform.system()
    max_inactivity = 600 # 10 minutes in seconds
    if system == "Darwin":
        try:
            idle_time = float(os.popen("ioreg -c IOHIDSystem | grep -i 'IdleSince' | awk '{print $NF / 1000000000.0}'").read().strip())
            return "OK" if idle_time <= max_inactivity else f"Too long ({int(idle_time / 60)} mins)"
        except Exception:
            return "Unknown"
    elif system == "Windows":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Power\PowerSettings\7516bcaa-f5b3-45ec-b38b-74c2999d6d17\8ec4b3a5-6868-48c2-be75-4f3044be9d16")
            value, _ = winreg.QueryValueEx(key, "AcValue") # For AC power
            return "OK" if value <= max_inactivity else f"Too long ({int(value / 60)} mins)"
        except Exception:
            return "Unknown"
    elif system == "Linux":
        try:
            # This is very desktop environment dependent (gnome, kde, etc.)
            # Returning a generic status for now.
            return "Checking sleep settings..."
        except Exception:
            return "Unknown"
    return "Unsupported OS"

def get_system_health_data():
    return {
        "machine_id": MACHINE_ID,
        "timestamp": time.time(),
        "os": platform.system(),
        "os_version": platform.version(),
        "disk_encrypted": get_disk_encryption_status(),
        "os_updates": get_os_update_status(),
        "antivirus": get_antivirus_status(),
        "inactivity_sleep": get_inactivity_sleep_settings()
    }

def report_data(data):
    # try:
    #     headers = {'Content-Type': 'application/json'}
    #     response = requests.post(API_ENDPOINT, json=data, headers=headers)
    #     response.raise_for_status()  # Raise an exception for bad status codes
    #     print(f"Data reported successfully: {response.status_code}")
    # except requests.exceptions.RequestException as e:
    #     print(f"Error reporting data: {e}")
    print("--- Reporting Data ---")
    print(json.dumps(data, indent=4))
    print("----------------------")

def check_and_report():
    current_data = get_system_health_data()
    global last_reported_data
    if current_data != last_reported_data:
        report_data(current_data)
        last_reported_data = current_data

def main():
    global last_reported_data
    last_reported_data = None # Initialize

    print("System Health Utility started...")
    check_and_report() # Initial report

    schedule.every(REPORTING_INTERVAL_SECONDS).seconds.do(check_and_report)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()