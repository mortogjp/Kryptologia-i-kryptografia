import sys

def main_menu():
    """
    Main TUI (Text User Interface) loop skeleton.
    """
    while True:
        print("\n===============================")
        print("      PERMUTATION CIPHER       ")
        print("===============================")
        print("1. Encrypt message")
        print("2. Decrypt message")
        print("3. Exit")
        print("===============================")
        
        choice = input("Select an option (1-3): ").strip()
        
        if choice == '1':
            print("[INFO] Encryption logic will be here.")
        elif choice == '2':
            print("[INFO] Decryption logic will be here.")
        elif choice == '3':
            print("[INFO] Shutting down...")
            sys.exit(0)
        else:
            print("[ERROR] Invalid option.")

if __name__ == "__main__":
    main_menu()