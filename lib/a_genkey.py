import hashlib
from pathlib import Path
import os
import shutil
import subprocess
import urllib.parse
import urllib.request

directories = ["keys"]
for dir in directories:
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir, exist_ok=True)

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

print("----------------------------------------------------------------------------")
print_message("Generating OpenCore Secure Boot UUID", "yellow")
print("----------------------------------------------------------------------------")

keys_dir = "keys"
guid_file = Path(keys_dir, "guid.txt")
subprocess.run(["uuidgen", "--random"], stdout=open(guid_file, "w"), text=True)
guid_content = guid_file.read_text().strip()
print("Generated UUID:", guid_content)

print("----------------------------------------------------------------------------")
print_message("Generating Certificates", "yellow")
print("----------------------------------------------------------------------------")


def generate_certificate():
    choice = input("Press '1' for default certificate or '2' for custom certificate: ")
    if choice == "1":
        country = "US"
        state = "California"
        locality = "Cupertino"
        organization = "Archlinux"
        common_name = "Linux"
    elif choice == "2":
        country = input("Enter country code (i.e. US): ")
        state = input("Enter state (i.e. Washington): ")
        locality = input("Enter locality (i.e. Redmond): ")
        organization = input("Enter organization (i.e. Microsoft Corporation): ")
        common_name = input("Enter any common name: ")
    else:
        print("Invalid choice. Exiting.")
        return

    print("Certificate details:")
    print(f"Country: {country}")
    print(f"State: {state}")
    print(f"Locality: {locality}")
    print(f"Organization: {organization}")
    print(f"Common Name: {common_name}")

    keys_dir = "keys"

    try:
        print_message("Generating PK", "blue")
        ok_path = Path(keys_dir) / "PK"
        subprocess.run(
            [
                "openssl",
                "req",
                "-newkey",
                "rsa:4096",
                "-nodes",
                "-keyout",
                f"{ok_path}.key",
                "-new",
                "-x509",
                "-sha256",
                "-days",
                "3650",
                "-subj",
                f"/C={country}/ST={state}/L={locality}/O={organization}/CN={common_name} Platform Key/",
                "-out",
                f"{ok_path}.crt",
            ],
            check=True,
            stdout=subprocess.DEVNULL,  # Suppress stdout
            stderr=subprocess.DEVNULL,  # Suppress stderr
        )
        subprocess.run(
            [
                "openssl",
                "x509",
                "-outform",
                "DER",
                "-in",
                f"{ok_path}.crt",
                "-out",
                f"{ok_path}.cer",
            ],
            check=True,
            stdout=subprocess.DEVNULL,  # Suppress stdout
            stderr=subprocess.DEVNULL,  # Suppress stderr
        )
        subprocess.run(
            [
                "cert-to-efi-sig-list",
                "-g",
                guid_content,
                f"{ok_path}.crt",
                f"{ok_path}.esl",
            ],
            check=True,
            stdout=subprocess.DEVNULL,  # Suppress stdout
            stderr=subprocess.DEVNULL,  # Suppress stderr
        )
        subprocess.run(
            [
                "sign-efi-sig-list",
                "-g",
                guid_content,
                "-k",
                f"{ok_path}.key",
                "-c",
                f"{ok_path}.crt",
                "PK",
                f"{ok_path}.esl",
                f"{ok_path}.auth",
            ],
            check=True,
            stdout=subprocess.DEVNULL,  # Suppress stdout
            stderr=subprocess.DEVNULL,  # Suppress stderr
        )
        print_message("Generating PK successful.", "green")
        calculate_checksums(ok_path)

        print_message("Generating noPK", "blue")
        no_ok_path = Path(keys_dir) / "noPK"
        subprocess.run(
            [
                "sign-efi-sig-list",
                "-g",
                guid_content,
                "-c",
                f"{ok_path}.crt",
                "-k",
                f"{ok_path}.key",
                "PK",
                "/dev/null",
                f"{no_ok_path}.auth",
            ],
            check=True,
            stdout=subprocess.DEVNULL,  # Suppress stdout
            stderr=subprocess.DEVNULL,  # Suppress stderr
        )
        print_message("Generating noPK successful.", "green")
        calculate_checksums(no_ok_path)

        print_message("Generating KEK", "blue")
        kek_path = Path(keys_dir) / "KEK"
        subprocess.run(
            [
                "openssl",
                "req",
                "-newkey",
                "rsa:4096",
                "-nodes",
                "-keyout",
                f"{kek_path}.key",
                "-new",
                "-x509",
                "-sha256",
                "-days",
                "3650",
                "-subj",
                f"/C={country}/ST={state}/L={locality}/O={organization}/CN={common_name} Key Exchange Key/",
                "-out",
                f"{kek_path}.crt",
            ],
            check=True,
            stdout=subprocess.DEVNULL,  # Suppress stdout
            stderr=subprocess.DEVNULL,  # Suppress stderr
        )
        subprocess.run(
            [
                "openssl",
                "x509",
                "-outform",
                "DER",
                "-in",
                f"{kek_path}.crt",
                "-out",
                f"{kek_path}.cer",
            ],
            check=True,
            stdout=subprocess.DEVNULL,  # Suppress stdout
            stderr=subprocess.DEVNULL,  # Suppress stderr
        )
        subprocess.run(
            [
                "cert-to-efi-sig-list",
                "-g",
                guid_content,
                f"{kek_path}.crt",
                f"{kek_path}.esl",
            ],
            check=True,
            stdout=subprocess.DEVNULL,  # Suppress stdout
            stderr=subprocess.DEVNULL,  # Suppress stderr
        )
        subprocess.run(
            [
                "sign-efi-sig-list",
                "-g",
                guid_content,
                "-k",
                f"{kek_path}.key",
                "-c",
                f"{kek_path}.crt",
                "KEK",
                f"{kek_path}.esl",
                f"{kek_path}.auth",
            ],
            check=True,
            stdout=subprocess.DEVNULL,  # Suppress stdout
            stderr=subprocess.DEVNULL,  # Suppress stderr
        )
        print_message("Generating KEK successful.", "green")
        calculate_checksums(kek_path)

        print_message("Generating db", "blue")
        db_path = Path(keys_dir) / "db"
        subprocess.run(
            [
                "openssl",
                "req",
                "-newkey",
                "rsa:4096",
                "-nodes",
                "-keyout",
                f"{db_path}.key",
                "-new",
                "-x509",
                "-sha256",
                "-days",
                "3650",
                "-subj",
                f"/C={country}/ST={state}/L={locality}/O={organization}/CN={common_name} Authorized Signature Database Key/",
                "-out",
                f"{db_path}.crt",
            ],
            check=True,
            stdout=subprocess.DEVNULL,  # Suppress stdout
            stderr=subprocess.DEVNULL,  # Suppress stderr
        )
        subprocess.run(
            [
                "openssl",
                "x509",
                "-outform",
                "DER",
                "-in",
                f"{db_path}.crt",
                "-out",
                f"{db_path}.cer",
            ],
            check=True,
            stdout=subprocess.DEVNULL,  # Suppress stdout
            stderr=subprocess.DEVNULL,  # Suppress stderr
        )
        subprocess.run(
            [
                "cert-to-efi-sig-list",
                "-g",
                guid_content,
                f"{db_path}.crt",
                f"{db_path}.esl",
            ],
            check=True,
            stdout=subprocess.DEVNULL,  # Suppress stdout
            stderr=subprocess.DEVNULL,  # Suppress stderr
        )
        subprocess.run(
            [
                "sign-efi-sig-list",
                "-g",
                guid_content,
                "-k",
                f"{db_path}.key",
                "-c",
                f"{db_path}.crt",
                "db",
                f"{db_path}.esl",
                f"{db_path}.auth",
            ],
            check=True,
            stdout=subprocess.DEVNULL,  # Suppress stdout
            stderr=subprocess.DEVNULL,  # Suppress stderr
        )
        print_message("Generating db successful.", "green")
        calculate_checksums(db_path)
    except subprocess.CalledProcessError as e:
        print_message("Certificate generation failed.", "red")
        print(str(e))

def calculate_checksums(directory):
    extensions = (".auth", ".crt", ".esl", ".key")
    for ext in extensions:
        file = f"{directory}{ext}"
        if os.path.exists(file):
            with open(file, "rb") as f:
                data = f.read()
                sha1_hash = hashlib.sha1(data).hexdigest()
                md5_hash = hashlib.md5(data).hexdigest()
                print(f"SHA1: {sha1_hash}, MD5: {md5_hash} for file: {file}")
        else:
            print(f"File {file} does not exist.")

generate_certificate()



print("----------------------------------------------------------------------------")
print_message("Changing Key Permission", "yellow")
print("----------------------------------------------------------------------------")


def change_permissions(dir):
    files_by_dir = {}
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith((".auth", ".cer", ".crt", ".esl", ".key")):
                dir_path = os.path.relpath(root, dir)
                files_by_dir.setdefault(dir_path, []).append(file)
                filepath = Path(root, file)
                try:
                    os.chmod(filepath, 0o600)
                except Exception as e:
                    print_message(f"Error changing permissions for {filepath}: {e}", "red")

    for dir_path, files in files_by_dir.items():
        print(f"Changing permission:")
        file_list = ', '.join(files)
        print(f"{dir_path}: {file_list}")

keys_dir = "keys"
if os.path.exists(keys_dir):
    change_permissions(keys_dir)
    print_message("Permission changed", "green")
else:
    print_message(f"dir '{keys_dir}' not found.", "red")

print("----------------------------------------------------------------------------")
print_message("Downloading MS Certificates", "yellow")
print("----------------------------------------------------------------------------")

def rename_files_and_replace_spaces(dir, filename_map):
    for file in os.listdir(dir):
        if file.endswith((".auth", ".cer", ".crt", ".esl", ".key")):
            old_filepath = Path(dir, file)
            new_filename = filename_map.get(file, file).replace("-", " ").replace("%20", " ")
            new_filepath = Path(dir, new_filename)
            os.rename(old_filepath, new_filepath)

def calculate_sha1(file_path):
    sha1 = hashlib.sha1()
    with open(file_path, "rb") as f:
        while True:
            data = f.read(65536)  # Read in 64k chunks
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

keys_dir = "keys"

urls = {
    "https://www.microsoft.com/pkiops/certs/MicWinProPCA2011_2011-10-19.crt": "Microsoft Windows Production PCA 2011",
    "https://www.microsoft.com/pkiops/certs/windows%20uefi%20ca%202023.crt": "Windows UEFI CA 2023",
    "https://www.microsoft.com/pkiops/certs/MicCorUEFCA2011_2011-06-27.crt": "Microsoft Corporation UEFI CA 2011",
    "https://www.microsoft.com/pkiops/certs/microsoft%20uefi%20ca%202023.crt": "Microsoft UEFI CA 2023",
    "https://www.microsoft.com/pkiops/certs/MicCorKEKCA2011_2011-06-24.crt": "Microsoft Corporation KEK CA 2011",
    "https://www.microsoft.com/pkiops/certs/microsoft%20corporation%20kek%202k%20ca%202023.crt": "Microsoft Corporation KEK 2K CA 2023",
}

download_failed = False

for url, filename in urls.items():
    filename = filename + os.path.splitext(urllib.parse.urlparse(url).path)[1]  # Keep the original extension
    filepath = Path(keys_dir, filename)
    try:
        urllib.request.urlretrieve(url, str(filepath))
        file_sha1 = calculate_sha1(filepath)
        print(f"Downloaded {filename} - SHA1: {file_sha1}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
        download_failed = True
        break

if not download_failed:
    print_message("MS keys downloaded and saved successfully", "blue")
    rename_files_and_replace_spaces(keys_dir, {os.path.basename(urllib.parse.urlparse(url).path): name for url, name in urls.items()})
    print_message("Files renamed and spaces replaced", "green")
else:
    print_message("MS keys downloading failed.", "red")

print("----------------------------------------------------------------------------")
print_message("Creating EFI Signature Format", "yellow")
print("----------------------------------------------------------------------------")

owner_guid = "77fa9abd-0359-4d32-bd60-28f4e78f784b"
keys_dir = "keys"

subprocess.run(
    [
        "sbsiglist",
        "--owner",
        owner_guid,
        "--type",
        "x509",
        "--output",
        f"{keys_dir}/Microsoft Windows db 2011.esl",
        f"{keys_dir}/Microsoft Windows Production PCA 2011.crt",
    ],
    check=True,
)
subprocess.run(
    [
        "sbsiglist",
        "--owner",
        owner_guid,
        "--type",
        "x509",
        "--output",
        f"{keys_dir}/Microsoft Windows db 2023.esl",
        f"{keys_dir}/Windows UEFI CA 2023.crt",
    ],
    check=True,
)

subprocess.run(
    [
        "sbsiglist",
        "--owner",
        owner_guid,
        "--type",
        "x509",
        "--output",
        f"{keys_dir}/Microsoft UEFI db 2011.esl",
        f"{keys_dir}/Microsoft Corporation UEFI CA 2011.crt",
    ],
    check=True,
)
subprocess.run(
    [
        "sbsiglist",
        "--owner",
        owner_guid,
        "--type",
        "x509",
        "--output",
        f"{keys_dir}/Microsoft UEFI db 2023.esl",
        f"{keys_dir}/Microsoft UEFI CA 2023.crt",
    ],
    check=True,
)

print("MS Keys:", owner_guid)

file_paths = [
    Path(keys_dir, "Microsoft Windows db 2011.esl"),
    Path(keys_dir, "Microsoft Windows db 2023.esl"),
    Path(keys_dir, "Microsoft UEFI db 2011.esl"),
    Path(keys_dir, "Microsoft UEFI db 2023.esl"),
]

try:
    with open(file_paths[0], "rb") as f1, open(file_paths[1], "rb") as f2, open(
        file_paths[2], "rb"
    ) as f3, open(file_paths[3], "rb") as f4, open(
        Path(keys_dir, "Microsoft db.esl"), "wb"
    ) as fout:
        fout.write(f1.read())
        fout.write(f2.read())
        fout.write(f3.read())
        fout.write(f4.read())
    print("Microsoft db.esl generate success")
except Exception as e:
    print("Microsoft db.esl generate failed:", e)

subprocess.run(
    [
        "sbsiglist",
        "--owner",
        owner_guid,
        "--type",
        "x509",
        "--output",
        f"{keys_dir}/Microsoft Windows KEK 2011.esl",
        f"{keys_dir}/Microsoft Corporation KEK CA 2011.crt",
    ],
    check=True,
)
subprocess.run(
    [
        "sbsiglist",
        "--owner",
        owner_guid,
        "--type",
        "x509",
        "--output",
        f"{keys_dir}/Microsoft Windows KEK 2023.esl",
        f"{keys_dir}/Microsoft Corporation KEK 2K CA 2023.crt",
    ],
    check=True,
)

file_paths = [
    Path(keys_dir, "Microsoft Windows KEK 2011.esl"),
    Path(keys_dir, "Microsoft Windows KEK 2023.esl"),
]

try:
    with open(file_paths[0], "rb") as f1, open(file_paths[1], "rb") as f2, open(
        Path(keys_dir, "Microsoft Windows KEK.esl"), "wb"
    ) as fout:
        fout.write(f1.read())
        fout.write(f2.read())
    print("Microsoft Windows KEK.esl generate success")
except Exception as e:
    print("Microsoft Windows KEK.esl generate failed:", e)

keys_dir = "keys"
kek_path = Path(keys_dir)
ok_path = Path(keys_dir)

kek_cert = kek_path / "KEK.crt"
pk_cert = ok_path / "PK.crt"

try:
    subprocess.run(
        [
            "sign-efi-sig-list",
            "-a",
            "-g",
            owner_guid,
            "-k",
            f"{kek_path}/KEK.key",
            "-c",
            kek_cert,
            "db",
            f"{keys_dir}/Microsoft db.esl",
            f"{keys_dir}/Additional Microsoft db.auth",
        ],
        check=True,
    )
    print("Additional Microsoft db.auth generate success")
except Exception as e:
    print("Additional Microsoft db.auth generate failed:", e)

try:
    subprocess.run(
        [
            "sign-efi-sig-list",
            "-a",
            "-g",
            owner_guid,
            "-k",
            f"{ok_path}/PK.key",
            "-c",
            pk_cert,
            "KEK",
            f"{keys_dir}/Microsoft Windows KEK.esl",
            f"{keys_dir}/Additional Microsoft Windows KEK.auth",
        ],
        check=True,
    )
    print_message("Additional Microsoft Windows KEK.auth generate success", "green")
except Exception as e:
    print_message("Additional Microsoft Windows KEK.auth generate failed:", e, "red")
    
print("----------------------------------------------------------------------------")
print_message("Option 1 Success", "green")
print("----------------------------------------------------------------------------")
