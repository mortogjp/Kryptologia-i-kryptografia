import sys

# Hardcoded permutation of minimum length 6
# Index mapping: 0->2, 1->4, 2->5, 3->0, 4->1, 5->3
PERMUTATION = [2, 4, 5, 0, 1, 3]
BLOCK_SIZE = len(PERMUTATION)

# Pre-calculate inverse permutation for decryption process
INV_PERMUTATION = [0] * BLOCK_SIZE
for i, p in enumerate(PERMUTATION):
    INV_PERMUTATION[p] = i

def clean_text(text: str) -> str:
    """
    Cleans the input text by removing spaces, numbers, and special characters.
    Converts everything to uppercase.
    """
    # Keep only alphabetical characters and convert them to uppercase
    return ''.join(char.upper() for char in text if char.isalpha())

def get_key_shift_value(key_type: str, key_val) -> int:
    """
    Converts the user key (int or string) into a single integer shift value.
    Used for the special index modulo condition.
    """
    if key_type == 'int':
        # If the key is an integer, use it directly as the shift value
        return int(key_val)
    else:
        # If the key is a string, sum the ASCII values of all its characters
        return sum(ord(c) for c in key_val)

def process_text(text: str, key_type: str, key_val, encrypt: bool = True) -> str:
    """
    Core logic for both encryption and decryption.
    Applies the permutation and the special modulo condition.
    """
    # If encrypting, pad the text with 'X' so its length is a multiple of BLOCK_SIZE
    if encrypt:
        padding_length = (BLOCK_SIZE - (len(text) % BLOCK_SIZE)) % BLOCK_SIZE
        text += 'X' * padding_length

    # Initialize a list to hold the result characters
    result = [''] * len(text)
    
    # Calculate the shift value from the user's key
    shift_val = get_key_shift_value(key_type, key_val)
    
    # Select the correct permutation array (normal for encryption, inverted for decryption)
    perm = PERMUTATION if encrypt else INV_PERMUTATION

    # Process the text block by block
    for block_start in range(0, len(text), BLOCK_SIZE):
        for i in range(BLOCK_SIZE):
            # Break if we reach the end of the text
            if block_start + i >= len(text):
                break
                
            original_char = text[block_start + i]
            
            # Find the target index within the current block
            target_idx_in_block = perm[i]
            # Calculate the global target index in the entire text string
            target_global_idx = block_start + target_idx_in_block
            
            # Calculate the global starting index of the current character
            global_i = block_start + i
            
            # Check the special condition: "sum of index numbers modulo three equals two"
            if (global_i + target_global_idx) % 3 == 2:
                # Determine shift direction (positive for encryption, negative for decryption)
                shift = shift_val if encrypt else -shift_val
                
                # Shift the character using the standard Caesar cipher formula (A-Z)
                new_char_code = (ord(original_char) - 65 + shift) % 26 + 65
                char_to_place = chr(new_char_code)
            else:
                # If condition is not met, keep the original character without shifting
                char_to_place = original_char

            # Place the character at its new encrypted/decrypted position
            result[target_global_idx] = char_to_place

    # Join the list of characters back into a single string
    final_text = ''.join(result)
    
    # If decrypting, remove the 'X' padding from the end of the text
    if not encrypt:
        final_text = final_text.rstrip('X')
        
    return final_text

def get_valid_plaintext(prompt: str) -> str:
    """
    Forces the user to input valid text. 
    Ignores numbers/special characters automatically.
    """
    while True:
        try:
            # Read input and remove leading/trailing whitespaces
            raw_text = input(prompt).strip()
            
            # Clean the text (remove non-letters)
            text = clean_text(raw_text)
            
            # Check if the text is empty after cleaning process
            if not text:
                print("[ERROR] Text must contain at least one letter.")
                continue
            
            return text
            
        except (KeyboardInterrupt, EOFError):
            # Gracefully handle Ctrl+C or Ctrl+D interrupts
            print("\n[INFO] Operation cancelled by user.")
            sys.exit(0)

def get_valid_key():
    """
    Forces the user to provide a valid key based on the strict requirements.
    """
    while True:
        try:
            # Display menu for key type selection
            print("\n--- CHOOSE KEY TYPE ---")
            print("a) Integer (Liczba calkowita)")
            print("b) Keyword min. 8 letters (Slowo kluczowe)")
            
            key_type = input("Your choice (a/b): ").strip().lower()
            
            if key_type == 'a':
                raw_key = input("Enter integer key: ").strip()
                try:
                    # Try to convert input to an integer
                    key = int(raw_key)
                    return ("int", key)
                except ValueError:
                    print("[ERROR] Key must be a valid integer.")
            
            elif key_type == 'b':
                raw_key = input("Enter keyword (min. 8 letters): ").strip()
                
                # Clean the keyword (remove spaces, digits, special chars)
                key = clean_text(raw_key)
                
                # Check if the cleaned keyword meets the minimum length requirement
                if len(key) >= 8:
                    return ("str", key)
                else:
                    print(f"[ERROR] Cleaned keyword length is {len(key)}. Must be at least 8 letters.")
            else:
                print("[ERROR] Invalid choice. Please enter 'a' or 'b'.")
                
        except (KeyboardInterrupt, EOFError):
            print("\n[INFO] Operation cancelled by user.")
            sys.exit(0)

def main_menu():
    """
    Main TUI (Text User Interface) loop.
    """
    while True:
        try:
            # Display the main menu interface
            print("\n===============================")
            print("      PERMUTATION CIPHER       ")
            print("===============================")
            print("1. Encrypt message")
            print("2. Decrypt message")
            print("3. Exit")
            print("===============================")
            
            # Get user choice
            choice = input("Select an option (1-3): ").strip()
            
            if choice == '1':
                # Encryption flow
                text = get_valid_plaintext("Enter text to ENCRYPT: ")
                k_type, k_val = get_valid_key()
                encrypted = process_text(text, k_type, k_val, encrypt=True)
                
                print("\n[SUCCESS] Encryption complete!")
                print(f"Result: {encrypted}")
                
            elif choice == '2':
                # Decryption flow
                text = get_valid_plaintext("Enter text to DECRYPT: ")
                k_type, k_val = get_valid_key()
                decrypted = process_text(text, k_type, k_val, encrypt=False)
                
                print("\n[SUCCESS] Decryption complete!")
                print(f"Result: {decrypted}")
                
            elif choice == '3':
                # Exit the program
                print("[INFO] Shutting down...")
                sys.exit(0)
            else:
                print("[ERROR] Unrecognized option. Please enter 1, 2, or 3.")
                
        except (KeyboardInterrupt, EOFError):
            # Handle emergency exit gracefully (e.g. user pressed Ctrl+C)
            print("\n[INFO] Emergency exit. Shutting down...")
            sys.exit(0)

if __name__ == "__main__":
    # Start the main application loop
    main_menu()