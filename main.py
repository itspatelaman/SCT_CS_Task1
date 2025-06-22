# main.py

from cipher import caesar_encrypt, caesar_decrypt
from utils import save_to_file


def normalize_shift(shift):
    return shift % 26


def main():
    print("=" * 35)
    print("     🔐 Caesar Cipher Tool")
    print("=" * 35)

    choice = input("Do you want to (E)ncrypt or (D)ecrypt)? ").strip().upper()
    if choice not in ['E', 'D']:
        print("❌ Invalid choice. Choose E or D.")
        return

    message = input("Enter your message: ")
    
    try:
        shift = int(input("Enter shift value (e.g., 3): "))
        shift = normalize_shift(shift)
    except ValueError:
        print("❌ Shift must be a number.")
        return

    if choice == 'E':
        result = caesar_encrypt(message, shift)
        print(f"\n🔐 Encrypted Message: {result}")
    else:
        result = caesar_decrypt(message, shift)
        print(f"\n🔓 Decrypted Message: {result}")

    save = input("\n💾 Do you want to save the result to a file? (y/n): ").lower()
    if save == 'y':
        filename = input("Enter filename (e.g., output.txt): ").strip()
        if not filename:
            filename = "output.txt"
        save_to_file(filename, result)
        print(f"✅ Saved to {filename}")


if __name__ == "__main__":
    main()
