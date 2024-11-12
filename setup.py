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
            "encrypt-tar=encrypt_tar:main",  # Maps "encrypt-tar" command to main() in encrypt_tar.py
        ],
    },
    install_requires=requirements,  # Use the parsed requirements
)

