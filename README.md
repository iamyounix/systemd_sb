# systemd_sb

It is a **bash** + **python** script that provides a menu-driven interface for performing various tasks related to managing keys and signatures in the **systemd-boot bootloader** environment. 

## Functions for Different Task

- Option 1: Generate keys required for signing (a_genkey.py).
- Option 2: Sign systemd-boot using current keys (b_sign.py). Requires option 1.
- Option 3: Remove EFI signature from systemd-boot (c_rmsign.py).
- Option 4: Verify EFI signatures in systemd-boot (d_verify.py).
- Option 5: Exit the script.
- Input Handling: After each task is completed, the user is prompted to choose whether to return to the main menu or exit the script.

## Usage

- Make sure you have Python3 installed on your system.
- Ensure that the Python scripts (a_genkey.py, b_sign.py, c_rmsign.py, and d_verify.py) exist in the appropriate directories (lib) relative to the script (systemd_sb.sh).
- Run the script by executing ./systemd_sb.sh in your terminal.
  
  ```zsh
  sh systemd_sb.sh
  ```
  
- Follow the on-screen instructions to perform the desired tasks related to managing keys and signatures in systemd-boot.
This script provides a convenient way to interact with the underlying Python scripts for key generation, signing, signature removal, and verification within the systemd-boot environment.

## Menu

![menu](https://github.com/iamyounix/systemd_sb/assets/72515939/9da5d424-78ee-4b82-83c0-8eafc485de15)

## Example

![option 1](https://github.com/iamyounix/systemd_sb/assets/72515939/0f25dff8-b5ba-4c8d-8bee-afd77ff996ee)

- `1` will generate default certificate info
  -  country = "US"
  -  state = "California"
  -  locality = "Cupertino"
  -  organization = "Archlinux"
  -  common_name = "Linux"
 
- `2` to generate custon info
  -  country = "editable"
  -  state = "editable"
  -  locality = "editable"
  -  organization = "editable"
  -  common_name = "editable"

**Option `1`:**

```zsh
❯ sh systemd_sb.sh 
Choose an option:
1. Generate keys (.auth, .cer, .crt, .esl & .key)
2. Signing systemd-boot with current keys (require option 1)
3. Remove .efi signature from current systemd-boot
4. Verify .efi signatures from current systemd-boot
5. Exit
Enter your choice: 1
----------------------------------------------------------------------------
Generating OpenCore Secure Boot UUID
----------------------------------------------------------------------------
Generated UUID: cb2071f0-0538-4ceb-8f51-7e05cf9c2e4e
----------------------------------------------------------------------------
Generating Certificates
----------------------------------------------------------------------------
Press '1' for default certificate or '2' for custom certificate: 1
Certificate details:
Country: US
State: California
Locality: Cupertino
Organization: Archlinux
Common Name: Linux
Generating PK
Generating PK successful.
SHA1: 7f632332b799bb752feeba3fbaa2b15f6c4d0795, MD5: 1b643e5f24194019a1bd4ce9cc922dfc for file: keys/PK.auth
SHA1: 6328cf7bd3b3495d04a4ef462cca43fb94528a6f, MD5: 4dba10df7b764394127c6b4c6730a661 for file: keys/PK.crt
SHA1: ccb487605ba6514baf62c86e3dd377451becef2e, MD5: 381949e33efa79baeccc23343fb44cff for file: keys/PK.esl
SHA1: fb0d2423cc6bf84e02db1c23f498c4b9b2f4ed41, MD5: df495b2ff998a336105a02d3d1a4ac13 for file: keys/PK.key
Generating noPK
Generating noPK successful.
SHA1: 7f90bf5a1fe2411e5eb3ec97b2ed34863425e8d9, MD5: 1d102117dd36a03352b11bab06c4165d for file: keys/noPK.auth
File keys/noPK.crt does not exist.
File keys/noPK.esl does not exist.
File keys/noPK.key does not exist.
Generating KEK
Generating KEK successful.
SHA1: f9593e0320e43040c96bc80e6336c074af1212bf, MD5: 485afeca1a1b44d451c1fd0c187f95f7 for file: keys/KEK.auth
SHA1: de678917649a9ed77caacb02ba78a63b12a51c55, MD5: ccf0f8c4787b8b91996dfedaad0c3e72 for file: keys/KEK.crt
SHA1: ddf32c24d85f6a5d69ceb1ffef2212ee81e986a3, MD5: 9de79c5a72c08031450c667d2a561a76 for file: keys/KEK.esl
SHA1: 8c3fb1ede628add0973d4a6b5b17a0ed6fa2d285, MD5: 8a166d6ace490a5a72ae5ff5018855f5 for file: keys/KEK.key
Generating db
Generating db successful.
SHA1: bc35ad42d337c1271c8716fed8d5bd37ec594c00, MD5: 3935f90ec000dc69cd073cac4450a9f5 for file: keys/db.auth
SHA1: b298c84cafcbcd0bd45f79e94483250ef1b38b95, MD5: 66d1301c3583a4af681893eea90b524c for file: keys/db.crt
SHA1: c84baec8d3e63d75cdc7c16254a6895a22c0839c, MD5: b8794393b5888700fe6cc6075b5fb4f7 for file: keys/db.esl
SHA1: c0452544e0eff51d8ae026583c5055d358f209e4, MD5: 58aecce3cec3f2b659687748dc4d6363 for file: keys/db.key
----------------------------------------------------------------------------
Changing Key Permission
----------------------------------------------------------------------------
Changing permission:
.: KEK.esl, PK.key, PK.esl, db.crt, KEK.auth, KEK.key, db.cer, PK.auth, KEK.cer, PK.crt, noPK.auth, db.esl, db.key, db.auth, PK.cer, KEK.crt
Permission changed
----------------------------------------------------------------------------
Downloading MS Certificates
----------------------------------------------------------------------------
Downloaded Microsoft Windows Production PCA 2011.crt - SHA1: 580a6f4cc4e4b669b9ebdc1b2b3e087b80d0678d
Downloaded Windows UEFI CA 2023.crt - SHA1: 45a0fa32604773c82433c3b7d59e7466b3ac0c67
Downloaded Microsoft Corporation UEFI CA 2011.crt - SHA1: 46def63b5ce61cf8ba0de2e6639c1019d0ed14f3
Downloaded Microsoft UEFI CA 2023.crt - SHA1: b5eeb4a6706048073f0ed296e7f580a790b59eaa
Downloaded Microsoft Corporation KEK CA 2011.crt - SHA1: 31590bfd89c9d74ed087dfac66334b3931254b30
Downloaded Microsoft Corporation KEK 2K CA 2023.crt - SHA1: 459ab6fb5e284d272d5e3e6abc8ed663829d632b
MS keys downloaded and saved successfully
Files renamed and spaces replaced
----------------------------------------------------------------------------
Creating EFI Signature Format
----------------------------------------------------------------------------
MS Keys: 77fa9abd-0359-4d32-bd60-28f4e78f784b
Microsoft db.esl generate success
Microsoft Windows KEK.esl generate success
Timestamp is 0-0-0 00:00:00
Authentication Payload size 6173
Signature of size 2199
Signature at: 40
Additional Microsoft db.auth generate success
Timestamp is 0-0-0 00:00:00
Authentication Payload size 3108
Signature of size 2186
Signature at: 40
Additional Microsoft Windows KEK.auth generate success
----------------------------------------------------------------------------
Option 1 Success
----------------------------------------------------------------------------
Press 'm' to return to the main menu, 'q' to quit: 
```

**Option `1` Generated Keys**

```zsh
❯ ls     
'Additional Microsoft db.auth'              'Microsoft UEFI CA 2023.crt'
'Additional Microsoft Windows KEK.auth'     'Microsoft UEFI db 2011.esl'
 db.auth                                    'Microsoft UEFI db 2023.esl'
 db.cer                                     'Microsoft Windows db 2011.esl'
 db.crt                                     'Microsoft Windows db 2023.esl'
 db.esl                                     'Microsoft Windows KEK 2011.esl'
 db.key                                     'Microsoft Windows KEK 2023.esl'
 guid.txt                                   'Microsoft Windows KEK.esl'
 KEK.auth                                   'Microsoft Windows Production PCA 2011.crt'
 KEK.cer                                     noPK.auth // required to remove current/older keys (mostly need on older bios)
 KEK.crt                                     PK.auth
 KEK.esl                                     PK.cer
 KEK.key                                     PK.crt
'Microsoft Corporation KEK 2K CA 2023.crt'   PK.esl
'Microsoft Corporation KEK CA 2011.crt'      PK.key
'Microsoft Corporation UEFI CA 2011.crt'    'Windows UEFI CA 2023.crt'
'Microsoft db.esl'
```

**References**

- Authorized Keys (db) — These are the key types that are used to verify the the utility that is going to be loaded when the secure boot is enabled on system. db will contain a list of public keys that are from sources that are considered to be secure. db can also hold the hash of binaries that are considered to be secure. Validation of source of utility being secure is validated using signature whereas validation of utility itself being secure is done using hash. db is signed using KEK’s private counterpart.
- Key Exchange Keys (KEK) — The KEK’s private counterpart is used to sign db or dbx holding the list of keys marked as secure or unsecure. Without the KEK, the firmware would have no way of knowing whether the key present in db or dbx was valid or was being fed by malware. Secure boot is designed in a way that db can only be updated if signed by KEK otherwise rejected. KEK is signed using PK’s private counterpart.
- Platform Key (PK) — This the top level key in secure boot architecture. PK is self signed i.e. PK is signed by its own private counterpart.

## Enroll

This key is required to be enroll via BIOS

- db.auth    
- Additional Microsoft db.auth
- KEK.auth
- Additional Microsoft Windows KEK.auth
- PK.auth

Step

- Go to BIOS, find secureboot option, delete current keys
- Enroll db.auth and Additional Microsoft db.auth for Authorized Signature Database option.
- Enroll KEK.auth and Additional Microsoft Windows KEK.auth for Key Exchange Key option.
- Enroll PK.auth for Platform Key.
- Enable Secureboot option.
