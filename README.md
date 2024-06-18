# Program Enkripsi File

![Image](https://i.ibb.co/xDnjCKt/OIG1-s.jpg)

Program ini digunakan untuk mengenkripsi teks dari file dan menghasilkan file Python untuk mendekripsi teks tersebut.

## Fitur

- Enkripsi teks menggunakan algoritma AES (Advanced Encryption Standard).
- Opsi untuk memasukkan password sendiri atau menggunakan password acak.
- Pembuatan file Python untuk mendekripsi teks terenkripsi.

## Prasyarat

- Python 3.x
- Modul `pycryptodome` (akan diinstal secara otomatis jika belum ada)

## Instalasi

1. Clone repository ini:
    ```sh
    git clone https://github.com/DioneAlFarisi/encrypt-file-python.git
    cd encrypt-file-python
    ```

2. Jalankan script utama:
    ```sh
    python main.py
    ```

## Cara Penggunaan

1. Jalankan script `main.py`:
    ```sh
    python main.py
    ```

2. Ikuti instruksi yang muncul di terminal:
    - Masukkan nama file yang ingin dienkripsi.
    - Pilih apakah Anda ingin memasukkan password sendiri atau menggunakan password acak.
    - Jika memasukkan password sendiri, pastikan password terdiri dari 16 karakter.
    
3. Setelah proses enkripsi selesai, program akan menampilkan kunci enkripsi dalam format hex. Simpan kunci ini di tempat yang aman.

4. Program akan membuat file Python untuk mendekripsi teks yang telah dienkripsi. Nama file akan mengikuti format `<nama_file_asli>.decrypt.py`.

## Penjelasan Kode

### Fungsi `install_and_import`

Fungsi ini mencoba mengimpor modul yang diperlukan (`pycryptodome`). Jika modul tidak ada, ia akan mencoba menginstalnya menggunakan `pip`.

### Fungsi `clear_screen`

Fungsi ini membersihkan layar terminal, tergantung pada sistem operasi yang digunakan.

### Fungsi `get_password`

Fungsi ini meminta pengguna untuk memilih antara memasukkan password sendiri atau menggunakan password acak. Jika pengguna memilih untuk memasukkan password, password harus 16 karakter.

### Fungsi `encrypt`

Fungsi ini mengenkripsi teks menggunakan AES dalam mode CBC, kemudian mengembalikan vektor inisialisasi (IV) dan ciphertext yang telah dienkode dalam base64.

### Fungsi `create_decrypt_file`

Fungsi ini membuat file Python untuk mendekripsi ciphertext. Isi file tergantung pada apakah pengguna memilih untuk memasukkan password sendiri atau menggunakan password acak. Kode untuk dekripsi dimasukkan ke dalam file, kemudian file tersebut dikompilasi menjadi file `.pyc`.

### Fungsi `main`

Fungsi ini mengatur alur utama program:
1. Membersihkan layar.
2. Meminta nama file yang akan dienkripsi.
3. Membaca isi file.
4. Meminta pengguna untuk memasukkan password atau menggunakan password acak.
5. Mengenkripsi teks.
6. Membuat file untuk mendekripsi ciphertext.

## Lisensi

Proyek ini dilisensikan di bawah lisensi MIT. Lihat file [LICENSE](./LICENSE) untuk informasi lebih lanjut.

## Changelog

Lihat [CHANGELOG.md](./CHANGELOG.md) untuk rincian perubahan.
