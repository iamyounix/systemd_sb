#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Function to launch main.py
launch_a_genkey() {
    python3 "$SCRIPT_DIR/lib/a_genkey.py"
}

# Function to launch add.py
launch_b_sign() {
    python3 "$SCRIPT_DIR/lib/b_sign.py"
}

# Function to launch removesign.py
launch_c_rmsign() {
    python3 "$SCRIPT_DIR/lib/c_rmsign.py"
}

# Function to launch verify.py
launch_d_verify() {
    python3 "$SCRIPT_DIR/lib/d_verify.py"
}

# Main menu
while true; do
    echo "Choose an option:"
    echo "1. Generate keys (.auth, .cer, .crt, .esl & .key)"
    echo "2. Signing systemd-boot with current keys (require option 1)"
    echo "3. Remove .efi signature from current systemd-boot"
    echo "4. Verify .efi signatures from current systemd-boot"
    echo "5. Exit"
    read -p "Enter your choice: " choice

    case $choice in
        1) 
            launch_a_genkey
            ;;
        2) 
            launch_b_sign
            ;;
        3) 
            launch_c_rmsign
            ;;
        4) 
            launch_d_verify
            ;;
        5) 
            exit
            ;;
        *) 
            echo "Invalid choice. Please enter a number from 1 to 5."
            ;;
    esac

    # Ask user if they want to return to main menu or exit
    read -p "Press 'm' to return to the main menu, 'q' to quit: " continue_choice

    case $continue_choice in
        [mM]) 
            continue
            ;;
        [qQ]) 
            exit
            ;;
        *) 
            echo "Invalid choice. Exiting."
            exit
            ;;
    esac
done

