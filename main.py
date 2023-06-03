import subprocess


def get_active_interface():
    output = subprocess.check_output("ipconfig", shell=True).decode('utf-8')

    active_interfaces = []
    current_interface = ""
    media_disconnected = False

    for line in output.split('\n'):
        if "adapter" in line:
            current_interface = line.strip().rstrip(':')
            media_disconnected = False
            if "(WSL)" in current_interface:
                current_interface = ""
                continue
        elif "Media State" in line:
            if "Media disconnected" in line:
                media_disconnected = True
        elif "IPv4 Address" in line and not media_disconnected and current_interface:
            active_interfaces.append(current_interface)

    return active_interfaces

