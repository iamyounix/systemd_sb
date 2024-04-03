import os
import subprocess
from pathlib import Path

# Color Definition
def print_message(message, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "blue": "\033[94m",
        "yellow": "\033[93m",
        "end": "\033[0m",
    }
    print(f"{colors.get(color, colors['end'])}{message}{colors['end']}")

keys_dir = "keys"

def show_notification():
    notification = """
    Warning:
    * The next process will automatically sign your systemd-boot drivers directly without making any copies.
    + "Ctrl+C" to kill the process, or;
    + "Ctrl+Z" to suspend the process.
    * This will sign:
            + BOOTX64.EFI
            + systemd-bootx64.efi
            + vmlinuz-linux
    * I am not responsible for any issues regarding the process. 
    """
    print_message(notification, "red")

def sign_systemd(dir):
    # Traverse the directory
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith((".efi", ".EFI", "vmlinuz-linux")):
                file_path = Path(root, file)
                # Sign the file
                result = subprocess.run(
                    [
                        "sudo",
                        "sbsign",
                        "--key",
                        f"{keys_dir}/db.key",
                        "--cert",
                        f"{keys_dir}/db.crt",
                        "--output",
                        str(file_path),
                        str(file_path),
                    ],
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    print_message(f"Signing successful for {file} in {root}", "green")
                else:
                    print_message(f"Signing failed for {file} in {root}. Error:", "red")
                    print(result.stderr)

if __name__ == "__main__":
    show_notification()
    # Specify the directory to traverse
    dir_to_sign = "/boot"
    # Call the function to sign files in the directory
    sign_systemd(dir_to_sign)

print("----------------------------------------------------------------------------")
print_message("Option 2 Success", "green")
print("----------------------------------------------------------------------------")
