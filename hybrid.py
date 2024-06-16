import os
import subprocess
import sys
import time
import importlib
import base64
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import py_compile

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

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_file(text, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(text.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv, ct

def encrypt_symmetric_key(sym_key, public_key):
    rsa_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    enc_sym_key = cipher_rsa.encrypt(sym_key)
    return base64.b64encode(enc_sym_key).decode('utf-8')

def create_decrypt_file(file_name, iv, ct, enc_sym_key, private_key):
    file_name_without_extension = os.path.splitext(file_name)[0]

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

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import unpad
from Crypto.PublicKey import RSA
import base64

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def decrypt_file(iv, ct, enc_sym_key, private_key):
    iv_bytes = base64.b64decode(iv)
    ct_bytes = base64.b64decode(ct)
    enc_sym_key_bytes = base64.b64decode(enc_sym_key)

    rsa_key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    sym_key = cipher_rsa.decrypt(enc_sym_key_bytes)

    cipher = AES.new(sym_key, AES.MODE_CBC, iv_bytes)
    pt = unpad(cipher.decrypt(ct_bytes), AES.block_size)
    return pt.decode('utf-8')

iv = '{iv}'
ct = '{ct}'
enc_sym_key = '{enc_sym_key}'
private_key = \"\"\"{private_key}\"\"\"

clear_screen()
print("\\n\\033[1;34m====== Dekripsi Program ======\\n\\033[1;35mby Dione\\n\\033[1;36mVersi: 1.2f\\n")

try:
    decrypted_text = decrypt_file(iv, ct, enc_sym_key, private_key)
    clear_screen()
    print("\\033[1;33mDekripsi berhasil...\\033[0m")
    time.sleep(3)
    clear_screen()
    exec(decrypted_text)
except Exception as e:
    print("\\033[1;31mError:", e, "\\033[0m")
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
    print("\t\033[1;34m====== Program Enkripsi ======\n\033[1;35mby Dione\n\033[1;36mVersi: 1.2f\n")
    file_path = input("\033[1;32mNama File: \033[0m")
    
    with open(file_path, 'r') as file:
        text = file.read()
    
    sym_key = get_random_bytes(16)
    private_key, public_key = generate_rsa_keys()

    print("\033[1;33m> Simpan kunci privat di tempat yang aman!!\033[0m")
    print(f"\033[1;33mPrivate Key:\n{private_key.decode()}\033[0m")

    iv, ciphertext = encrypt_file(text, sym_key)
    enc_sym_key = encrypt_symmetric_key(sym_key, public_key)
    print("\033[1;33mEncrypted:\n", ciphertext, "\033[0m")
    
    create_decrypt_file(file_path, iv, ciphertext, enc_sym_key, private_key.decode())
    print("\033[1;32mFile decrypt telah dibuat.\033[0m")

if __name__ == "__main__":
    main()