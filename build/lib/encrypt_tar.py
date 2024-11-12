#!/usr/bin/env python3
import os
import sys
from getpass import getpass
from rich.console import Console
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Constants
CHUNK_SIZE = 64 * 1024  # 64 KB chunk size
console = Console()


def generate_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return kdf.derive(password)


def encrypt_file(input_file_path: str, output_file_path: str, password: str):
    salt = os.urandom(16)
    key = generate_key(password.encode(), salt)
    iv = os.urandom(12)

    with open(input_file_path, 'rb') as infile, open(output_file_path, 'wb') as outfile:
        outfile.write(salt)
        outfile.write(iv)

        encryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=default_backend()
        ).encryptor()

        while chunk := infile.read(CHUNK_SIZE):
            outfile.write(encryptor.update(chunk))

        outfile.write(encryptor.finalize())
        outfile.write(encryptor.tag)


def decrypt_file(input_file_path: str, output_file_path: str, password: str):
    with open(input_file_path, 'rb') as infile:
        salt = infile.read(16)
        iv = infile.read(12)
        key = generate_key(password.encode(), salt)

        decryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=default_backend()
        ).decryptor()

        with open(output_file_path, 'wb') as outfile:
            while chunk := infile.read(CHUNK_SIZE):
                if infile.tell() == os.fstat(infile.fileno()).st_size:
                    tag = chunk[-16:]
                    outfile.write(decryptor.update(chunk[:-16]))
                else:
                    outfile.write(decryptor.update(chunk))

            decryptor.finalize_with_tag(tag)


def main():
    console.print("File Encryption/Decryption Utility", style="bold green")

    # Check for arguments and display help if needed
    args = sys.argv[1:]

    if not args or '--help' in args:
        console.print(
            "[bold yellow]Usage:[/] encrypt-tar --encrypt|--decrypt --input <input_file> --output <output_file> [--password <password> or set ENCRYPTION_PASSWORD]",
            style="bold green"
        )
        return

    # Parse arguments
    mode = None
    input_file = None
    output_file = None
    password = None

    if '--encrypt' in args:
        mode = 'encrypt'
    elif '--decrypt' in args:
        mode = 'decrypt'

    if '--input' in args:
        input_file = args[args.index('--input') + 1]

    if '--output' in args:
        output_file = args[args.index('--output') + 1]

    if '--password' in args:
        password = args[args.index('--password') + 1]
    else:
        password = os.getenv("ENCRYPTION_PASSWORD") or getpass("Enter password: ")

    # Validate arguments
    if not mode:
        console.print("[red]Error: Please specify --encrypt or --decrypt[/]", style="bold red")
        return
    if not input_file or not output_file:
        console.print("[red]Error: --input and --output are required arguments[/]", style="bold red")
        return
    if not password:
        console.print("[red]Error: Password is required![/]", style="bold red")
        return

    # Run encryption or decryption
    if mode == "encrypt":
        encrypt_file(input_file, output_file, password)
        console.print(f"[green]File encrypted successfully and saved to {output_file}[/]", style="bold green")
    elif mode == "decrypt":
        decrypt_file(input_file, output_file, password)
        console.print(f"[green]File decrypted successfully and saved to {output_file}[/]", style="bold green")


if __name__ == "__main__":
    main()
