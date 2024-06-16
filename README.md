### Fungsi Program:

1. **Instalasi dan Pengecekan Modul:**
   - **`install_and_import`**: Mengecek apakah modul `pycryptodome` sudah terinstal. Jika belum, modul tersebut akan diinstal.

2. **Enkripsi dan Dekripsi:**
   - **`encrypt`**: Mengenkripsi teks menggunakan AES dalam mode CBC.
   - **`decrypt`**: Mendekripsi teks yang terenkripsi menggunakan AES dalam mode CBC.

3. **Pembuatan File Dekripsi:**
   - **`create_decrypt_file`**: Membuat file Python yang mendekripsi teks terenkripsi dan mengeksekusinya setelah pengguna memasukkan kunci yang benar.

4. **Manajemen Trial:**
   - **`TrialScript` Class:
     - **`__init__`**: Menginisialisasi objek `TrialScript` dan memuat informasi trial dari file.
     - **`compute_hash`**: Menghitung hash SHA-256 dari data.
     - **`load_trial_info`**: Memuat informasi trial dari file `trial_info.json`. Jika file tidak ada, inisialisasi dengan data baru.
     - **`save_trial_info`**: Menyimpan informasi trial yang terenkripsi ke dalam file `trial_info.json` dan menyimpan hash ke `__pycache__`.
     - **`save_hash`**: Menyimpan hash ke dalam file di `__pycache__`.
     - **`verify_hash`**: Memverifikasi hash yang disimpan di `__pycache__` dengan hash yang dihitung dari data.
     - **`is_trial_valid`**: Mengecek validitas trial berdasarkan tanggal aktivasi dan jumlah penggunaan.
     - **`run`**: Menjalankan script trial jika masih valid. Jika tidak, memberikan pesan bahwa trial sudah habis atau sudah mencapai batas maksimum penggunaan.

5. **Enkripsi File:**
   - **`main`**: Mengatur enkripsi file yang dipilih pengguna dan membuat file dekripsi yang menyertakan kunci enkripsi.

### Kelebihan Program:

1. **Keamanan dengan Enkripsi:**
   - Informasi trial dienkripsi menggunakan AES, yang memastikan bahwa data tidak dapat dibaca atau dimodifikasi tanpa kunci yang benar.

2. **Integritas Data dengan Hashing:**
   - Hash SHA-256 digunakan untuk memastikan bahwa informasi trial tidak dimanipulasi. Ini memberikan lapisan keamanan tambahan.

3. **Pembatasan Penggunaan:**
   - Program membatasi penggunaan script hingga 10 kali atau selama 30 hari, sehingga mendorong pengguna untuk membeli versi penuh setelah masa trial habis.

4. **Otomatisasi Instalasi Modul:**
   - Script secara otomatis menginstal modul `pycryptodome` jika belum terinstal, memastikan bahwa pengguna tidak perlu melakukannya secara manual.

5. **Pembuatan File Dekripsi:**
   - Script membuat file dekripsi yang dapat dieksekusi oleh pengguna setelah memasukkan kunci yang benar, memastikan bahwa data terenkripsi hanya dapat diakses oleh pengguna yang berwenang.

6. **Pengelolaan Pengguna Baru:**
   - Program menangani skenario di mana pengguna baru menjalankan script dan file `trial_info.json` belum ada, dengan menginisialisasi informasi trial baru secara otomatis.

Dengan kombinasi fitur-fitur ini, program memberikan solusi yang efektif untuk melindungi dan membatasi penggunaan script, sambil tetap mudah digunakan oleh pengguna akhir.

Berikut adalah contoh penggunaan program yang mencakup inisialisasi, pembuatan file enkripsi, dan pembatasan trial:
- **Instalasi dan Inisialisasi Program:**
----
_Jalankan script utama untuk memulai proses enkripsi file dan menginisialisasi informasi trial._
- **Enkripsi File:**
----
_Pengguna memasukkan nama file yang ingin dienkripsi.Program mengenkripsi isi file tersebut dan mencetak kunci enkripsi serta teks terenkripsi._
- **Pembuatan File Dekripsi:**
----
_Program membuat file dekripsi yang dapat dieksekusi oleh pengguna untuk mendekripsi dan mengeksekusi file terenkripsi setelah memasukkan kunci yang benar._
