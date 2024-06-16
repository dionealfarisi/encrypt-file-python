import os
import subprocess
import sys
import time
import importlib
import base64

def install_and_import(package):
    try:
        importlib.import_module(package)
        return True
    except ImportError:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            return True
        except subprocess.CalledProcessError:
            return False

if not install_and_import('pycryptodome'):
    sys.exit("Gagal menginstal modul 'pycryptodome'. Keluar...")

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import py_compile

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_password():
    key_choice = input("Apakah Anda ingin memasukkan password sendiri? (y/n): ").strip().lower()
    if key_choice == 'y':
        while True:
            key_input = input("Masukkan password (16 karakter): ").strip()
            if len(key_input) == 16:
                return key_input.encode(), key_choice
            else:
                print("Password harus 16 karakter.")
    else:
        return get_random_bytes(16), key_choice

def encrypt(text, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(text.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv, ct

def create_decrypt_file(file_name, iv, ct, key_hex, key_choice):
    file_name_without_extension = os.path.splitext(file_name)[0]

    if key_choice == 'y':
        decrypt_code = f"""
import subprocess
import sys
import importlib
import os
import time

def install_and_import():
    try:
        import pycryptodome
        return True
    except ImportError:
        print("Loading...")
        time.sleep(3)
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pycryptodome"])
            print("Instalasi berhasil.")
            return True
        except subprocess.CalledProcessError:
            print("Instalasi gagal.")
            return False

install_and_import()

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

def decrypt(iv, ct, key):
    iv_bytes = base64.b64decode(iv)
    ct_bytes = base64.b64decode(ct)
    cipher = AES.new(key, AES.MODE_CBC, iv_bytes)
    pt = unpad(cipher.decrypt(ct_bytes), AES.block_size)
    return pt.decode('utf-8')

iv = '{iv}'
ct = '{ct}'

clear_screen()
print("\\n===== Dibutuhkan Password =====\\n  by Dione\\n  Versi: 1.2\\n")
key_input = input("Password: ").strip()
if len(key_input) != 16:
    print("Password harus 16 karakter.")
    sys.exit(1)
try:
    key = key_input.encode()
    decrypted_text = decrypt(iv, ct, key)
    clear_screen()
    print("Dekripsi berhasil...")
    time.sleep(3)
    clear_screen()
    exec(decrypted_text)
except Exception as e:
    print("Error :", e)
"""
    else:
        decrypt_code = f"""
import subprocess
import sys
import importlib
import os
import time

def install_and_import():
    try:
        import pycryptodome
        return True
    except ImportError:
        print("Loading...")
        time.sleep(3)
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pycryptodome"])
            print("Instalasi berhasil.")
            return True
        except subprocess.CalledProcessError:
            print("Instalasi gagal.")
            return False

install_and_import()

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

def decrypt(iv, ct, key):
    iv_bytes = base64.b64decode(iv)
    ct_bytes = base64.b64decode(ct)
    cipher = AES.new(key, AES.MODE_CBC, iv_bytes)
    pt = unpad(cipher.decrypt(ct_bytes), AES.block_size)
    return pt.decode('utf-8')

iv = '{iv}'
ct = '{ct}'

clear_screen()
print("\\n===== Dibutuhkan Password =====\\n  by Dione\\n  Versi: 1.2\\n")
key_hex = input("Password): ").strip()
if len(key_hex) != 32:
    print("Kunci harus 32 karakter (16 byte dalam format hex).")
    sys.exit(1)
try:
    key = bytes.fromhex(key_hex)
    decrypted_text = decrypt(iv, ct, key)
    clear_screen()
    print("Dekripsi berhasil...:")
    time.sleep(3)
    exec(decrypted_text)
except Exception as e:
    print("Error:", e)
"""

    decrypt_file_name = file_name_without_extension + ".decrypt.py"
    with open(decrypt_file_name, "w") as f:
        f.write(decrypt_code)
    py_compile.compile(decrypt_file_name, cfile=decrypt_file_name + "c")
    if os.path.exists(decrypt_file_name + "c"):
        os.remove(decrypt_file_name)
        os.rename(decrypt_file_name + "c", decrypt_file_name)

def main():
    clear_screen()
    print("\t===== Program Enkripsi =====\n  by Dione\n  Versi: 1.2\n")
    file_path = input("Nama File: ")
    with open(file_path, 'r') as file:
        text = file.read()
    
    key, key_choice = get_password()
    print("> Simpan Key di Tempat yang aman!!")
    key_hex = key.hex()
    print(f"Key (hex): {key_hex}")
    
    iv, ciphertext = encrypt(text, key)
    print("Encrypted:", ciphertext)
    
    create_decrypt_file(file_path, iv, ciphertext, key_hex, key_choice)
    print("File decrypt.py telah dibuat.")

if __name__ == "__main__":
    main()
