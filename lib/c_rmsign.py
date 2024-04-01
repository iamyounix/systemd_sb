import os
import subprocess
from pathlib import Path

def print_message(message, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "blue": "\033[94m",
        "yellow": "\033[93m",
        "end": "\033[0m",
    }
    print(f"{colors.get(color, colors['end'])}{message}{colors['end']}")

def remove_signatures(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.efi', '.EFI', 'vmlinuz-linux')):
                filepath = os.path.join(root, file)
                try:
                    subprocess.run(['sudo', 'sbattach', '--signum', '1', '--remove', filepath], check=True)
                    print_message(f"Signature removed from {file}", "green")
                except subprocess.CalledProcessError as e:
                    print_message(f"Error removing signature from {file}: {e}", "red")

boot_dir = "/boot"
remove_signatures(boot_dir)
