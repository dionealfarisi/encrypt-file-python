import os
import subprocess
import sys
import importlib
import base64
import datetime
import json
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import py_compile

# Fungsi untuk membersihkan layar
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fungsi untuk menginstal modul jika diperlukan
def install_and_import():
    try:
        import pycryptodome
        return True  # Modul sudah ada, tidak perlu diinstal
    except ImportError:
        print("Check Module....\n Menginstal...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pycryptodome"])
            print("Instalasi berhasil.")
            return True  # Instalasi berhasil
        except subprocess.CalledProcessError:
            print("Instalasi gagal.")
            return False  # Instalasi gagal

install_and_import()

# Fungsi enkripsi
def encrypt(text, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(text.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv, ct

# Fungsi dekripsi
def decrypt(iv, ct, key):
    iv_bytes = base64.b64decode(iv)
    ct_bytes = base64.b64decode(ct)
    cipher = AES.new(key, AES.MODE_CBC, iv_bytes)
    pt = unpad(cipher.decrypt(ct_bytes), AES.block_size)
    return pt.decode('utf-8')

# Fungsi untuk membuat file dekripsi
def create_decrypt_file(file_name, iv, ct, key_hex):
    file_name_without_extension = os.path.splitext(file_name)[0]

    decrypt_code = f"""
import subprocess
import sys
import importlib
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def install_and_import():
    try:
        import pycryptodome
        return True  # Modul sudah ada, tidak perlu diinstal
    except ImportError:
        print("Modul pycryptodome tidak ditemukan.\\n Menginstal...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pycryptodome"])
            print("Instalasi berhasil.")
            return True  # Instalasi berhasil
        except subprocess.CalledProcessError:
            print("Instalasi gagal.")
            return False  # Instalasi gagal

install_and_import()

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
print("n=== Dibutuhkan Password ===\\n  by Dione")
key = bytes.fromhex(input("\\nPassword: "))
try:
    decrypted_text = decrypt(iv, ct, key)
    clear_screen()
    exec(decrypted_text)
except Exception as e:
    print("Error executing decrypted code:", e)
"""

    decrypt_file_name = file_name_without_extension + ".decrypt.py"
    with open(decrypt_file_name, "w") as f:
        f.write(decrypt_code)
    py_compile.compile(decrypt_file_name, cfile=decrypt_file_name + "c")
    os.remove(decrypt_file_name)
    os.rename(decrypt_file_name + "c", decrypt_file_name)

class TrialScript:
    def __init__(self, filename='trial_info.json'):
        self.filename = filename
        self.hash_filename = os.path.join('__pycache__', 'trial_info_hash')
        self.trial_duration = datetime.timedelta(days=30)
        self.max_usage = 10
        self.key = b'16byteslongkey!!'  # Key for encryption/decryption (16 bytes)
        self.load_trial_info()

    def compute_hash(self, data):
        return hashlib.sha256(data.encode()).hexdigest()

    def load_trial_info(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    iv, ct = json.load(file).values()
                    decrypted_data = decrypt(iv, ct, self.key)
                    data = json.loads(decrypted_data)
                    self.activation_date = datetime.datetime.fromisoformat(data['activation_date'])
                    self.current_usage = data['current_usage']
                    
                    # Verify the hash
                    hash_value = self.compute_hash(json.dumps(data))
                    if not self.verify_hash(hash_value):
                        print("Hash verification failed. Trial information might have been tampered with.")
                        self.activation_date = None
                        self.current_usage = None
            except Exception as e:
                print(f"Error loading trial info: {e}")
                self.activation_date = None
                self.current_usage = None
        else:
            self.activation_date = datetime.datetime.now()
            self.current_usage = 0
            self.save_trial_info()

    def save_trial_info(self):
        data = {
            'activation_date': self.activation_date.isoformat(),
            'current_usage': self.current_usage
        }
        encrypted_data = encrypt(json.dumps(data), self.key)
        with open(self.filename, 'w') as file:
            json.dump({
                'iv': encrypted_data[0],
                'ct': encrypted_data[1]
            }, file)
        
        # Save the hash in __pycache__
        hash_value = self.compute_hash(json.dumps(data))
        self.save_hash(hash_value)

    def save_hash(self, hash_value):
        os.makedirs('__pycache__', exist_ok=True)
        with open(self.hash_filename, 'w') as hash_file:
            hash_file.write(hash_value)

    def verify_hash(self, hash_value):
        if os.path.exists(self.hash_filename):
            with open(self.hash_filename, 'r') as hash_file:
                stored_hash = hash_file.read()
                return stored_hash == hash_value
        return False

    def is_trial_valid(self):
        if self.activation_date is None or self.current_usage is None:
            return False

        expiration_date = self.activation_date + self.trial_duration
        return datetime.datetime.now() < expiration_date and self.current_usage < self.max_usage

    def run(self):
        if self.is_trial_valid():
            if self.current_usage < self.max_usage:
                clear_screen()
                print("Trial script is running...")
                self.current_usage += 1
                self.save_trial_info()
                print(f"Remaining usages: {self.max_usage - self.current_usage}")
                main()
            else:
                print("Maximum usage reached. Please purchase the full version.")
        else:
            print("Trial period has expired or trial info file is missing. Please purchase the full version.")

def main():
    clear_screen()
    print("\t===== Program Enkripsi =====\n  by Dione\n")
    file_path = input("Nama File: ")
    with open(file_path, 'r') as file:
        text = file.read()
    key = get_random_bytes(16)
    print("Key:", key.hex())
    print("> Simpan Key di Tempat yang aman!!")
    iv, ciphertext = encrypt(text, key)
    print("Encrypted:", ciphertext)
    
    create_decrypt_file(file_path, iv, ciphertext, key.hex())
    print("File decrypt.py telah dibuat.")

if __name__ == "__main__":
    trial_script = TrialScript()
    trial_script.run()