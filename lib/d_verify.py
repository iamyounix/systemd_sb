import os
import subprocess

def traverse_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.efi', '.EFI', 'vmlinuz-linux')):
                yield os.path.join(root, file)

def verify_file(file_path):
    try:
        output = subprocess.check_output(['sbverify', '--list', file_path], stderr=subprocess.STDOUT)
        return output.decode().strip()
    except subprocess.CalledProcessError as e:
        return f"Verification failed for {file_path}: {e.output.decode().strip()}"

def print_message(message, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "blue": "\033[94m",
        "yellow": "\033[93m",
        "end": "\033[0m",
    }
    print(f"{colors.get(color, colors['end'])}{message}{colors['end']}")

def main():
    boot_directory = '/boot'
    no_signature_files = False

    for file_path in traverse_directory(boot_directory):
        verification_result = verify_file(file_path)
        print(f"{file_path}: {verification_result}")

        if "No signature table present" in verification_result:
            no_signature_files = True

    if no_signature_files:
        print_message("Please sign again your files", "red")
    else:
        print_message("Your files are perfectly signed", "green")

if __name__ == "__main__":
    main()

print("----------------------------------------------------------------------------")
print_message("Option 4 Success", "green")
print("----------------------------------------------------------------------------")

