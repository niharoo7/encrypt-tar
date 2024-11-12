
# Encrypt-Tar

`encrypt-tar` is a Python command-line tool for encrypting and decrypting large `.tar` files using AES-GCM encryption. It’s designed to handle files over 30GB and provides secure password handling via command-line arguments or environment variables.

## Features

- Encrypt and decrypt large `.tar` files with AES-GCM.
- Password handling through command-line arguments, environment variables, or masked input.
- Flexible installation: use as a Python script, install as a command-line tool with `pip`, or create a standalone executable with PyInstaller.

## Requirements

- Python 3.6+
- The following Python libraries:
  - `cryptography`
  - `rich`
  - `pyinstaller` (optional, for creating standalone binaries)

## Installation Methods

### 1. Installing as a Command-Line Tool with `pip`

#### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/encrypt-tar.git
cd encrypt-tar
```

#### Step 2: Install Dependencies

Make sure to have `requirements.txt` in the project root with the following content:

```plaintext
cryptography==41.0.1
rich==13.5.2
```

Install the dependencies with:

```bash
pip install -r requirements.txt
```

#### Step 3: Set Up as a Command-Line Tool

This package can be installed directly as a command-line tool using `pip`.

1. **Create `setup.py`** with the following content in the project directory:

    ```python
    from setuptools import setup

    # Read requirements from requirements.txt
    with open("requirements.txt") as f:
        requirements = f.read().splitlines()

    setup(
        name="encrypt-tar",
        version="1.0",
        py_modules=["encrypt_tar"],
        entry_points={
            "console_scripts": [
                "encrypt-tar=encrypt_tar:main",
            ],
        },
        install_requires=requirements,
    )
    ```

2. **Install the Package**:

    ```bash
    pip install .
    ```

3. **Run the Command**:

    Now you can use `encrypt-tar` from any location in your terminal.

    ```bash
    encrypt-tar --encrypt --input large_file.tar --output large_file_encrypted.tar
    ```

### 2. Creating a Standalone Executable with PyInstaller (Optional)

If you want to create a single executable file that doesn’t require Python to be installed on the target machine, you can use PyInstaller.

#### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

#### Step 2: Create the Executable

Run the following command in the project root:

```bash
pyinstaller --onefile --name=encrypt-tar encrypt_tar.py
```

This will generate an executable named `encrypt-tar` in the `dist` directory.

#### Step 3: Run the Executable

After PyInstaller completes, you can use the binary from the `dist` directory:

```bash
./dist/encrypt-tar --encrypt --input large_file.tar --output large_file_encrypted.tar
```

If desired, move the executable to a system PATH location, like `/usr/local/bin`, for easier access.

## Usage

### Command-Line Arguments

- `--encrypt` / `--decrypt`: Specify the mode (required).
- `--input <input_file>`: Path to the input `.tar` file (required).
- `--output <output_file>`: Path for the encrypted or decrypted output (required).
- `--password <password>`: Optional password argument. If not provided, the script will use the `ENCRYPTION_PASSWORD` environment variable or prompt you securely.

### Examples

#### Encrypt a File

Using an environment variable for the password:

```bash
export ENCRYPTION_PASSWORD="your_strong_password"
encrypt-tar --encrypt --input large_file.tar --output large_file_encrypted.tar
```

Using a direct password argument:

```bash
encrypt-tar --encrypt --input large_file.tar --output large_file_encrypted.tar --password your_password
```

#### Decrypt a File

```bash
encrypt-tar --decrypt --input large_file_encrypted.tar --output large_file_decrypted.tar --password your_password
```

### Environment Variable for Password (Optional)

You can set the password as an environment variable `ENCRYPTION_PASSWORD` to avoid typing it every time:

```bash
export ENCRYPTION_PASSWORD="your_strong_password"
```

## Notes

- For large files, encryption and decryption may take some time depending on your system’s processing power and disk speed.
- If you’re using PyInstaller, the executable may have a slight startup delay due to the bundling of dependencies.

## License

This project is licensed under the MIT License.
