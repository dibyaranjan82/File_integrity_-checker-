import hashlib
import os
import json

HASH_DB_FILE = 'file_hashes.json'

def calculate_file_hash(filepath, algorithm='sha256'):
    """Calculate the hash of a file."""
    hash_func = getattr(hashlib, algorithm)()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def load_hashes():
    """Load stored file hashes from JSON file."""
    if os.path.exists(HASH_DB_FILE):
        with open(HASH_DB_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_hashes(hashes):
    """Save updated hashes to JSON file."""
    with open(HASH_DB_FILE, 'w') as f:
        json.dump(hashes, f, indent=4)

def scan_directory(directory):
    """Scan all files in a directory and calculate hashes."""
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                file_hashes[filepath] = calculate_file_hash(filepath)
            except Exception as e:
                print(f"Could not hash {filepath}: {e}")
    return file_hashes

def check_integrity(current_hashes, stored_hashes):
    """Compare current hashes with stored hashes."""
    for filepath, hash_val in current_hashes.items():
        if filepath not in stored_hashes:
            print(f"[NEW] File added: {filepath}")
        elif stored_hashes[filepath] != hash_val:
            print(f"[MODIFIED] File changed: {filepath}")

    for filepath in stored_hashes:
        if filepath not in current_hashes:
            print(f"[DELETED] File removed: {filepath}")

def main():
    directory = input("Enter the directory to scan: ").strip()
    stored_hashes = load_hashes()
    current_hashes = scan_directory(directory)

    print("\n--- FILE INTEGRITY CHECK ---")
    check_integrity(current_hashes, stored_hashes)

    choice = input("\nUpdate hash records with current state? (y/n): ").lower()
    if choice == 'y':
        save_hashes(current_hashes)
        print("Hash records updated.")

if __name__ == "__main__":
    main()
