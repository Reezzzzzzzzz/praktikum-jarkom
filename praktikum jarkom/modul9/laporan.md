# Modul 9 — Web Server Sederhana (Revisi & Dokumentasi)

---

## Tujuan
Modul ini merupakan kelanjutan dari Modul 8: kode web server TCP yang sama dirapikan ulang dengan komentar penjelasan pada setiap baris, dan dijalankan di port yang berbeda (9999) supaya tidak bertabrakan dengan server Modul 8 jika keduanya dijalankan bersamaan.

## Implementasi Kode

### 1. TCP Server (`server.py`)

```python
from socket import *
import sys

# Buat socket server dengan IPv4 (AF_INET) dan TCP (SOCK_STREAM)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Server akan mendengarkan permintaan di port ini
serverPort = 9999
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while True:
    # Menunggu dan menerima koneksi baru dari client
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
        # Membaca request line yang dikirim oleh client (browser)
        message = connectionSocket.recv(1024).decode()

        # Mengambil nama file yang diminta dari request
        filename = message.split()[1]
        f = open(filename[1:])

        # Membaca seluruh isi file yang diminta
        outputdata = f.read()

        # Mengirim response header HTTP 200 OK ke client
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

        # Mengirim isi file ke client byte demi byte
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())

        connectionSocket.send("\r\n".encode())
        connectionSocket.close()

    except IOError:
        # Jika file tidak ditemukan, kirim response 404 Not Found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        connectionSocket.close()

serverSocket.close()
sys.exit()
```

Alur kerjanya sama seperti Modul 8: import library `socket`, lalu `sys` supaya bisa keluar dari program dengan rapi lewat `sys.exit()`. `serverSocket` dibuat dengan `AF_INET` (IPv4) dan `SOCK_STREAM` (TCP).

Port server kali ini ditetapkan ke `9999`, lalu di-*bind* lewat `serverSocket.bind(('', serverPort))` dan dibatasi hanya menerima 1 antrean koneksi lewat `serverSocket.listen(1)`.

Selanjutnya program masuk ke loop tanpa henti agar server bisa terus melayani permintaan. `connectionSocket` dibuat untuk berkomunikasi dengan client yang baru terhubung, sementara `addr` menyimpan informasi alamat IP client tersebut.

### 2. Halaman Uji (`HelloWorld.html`)

```html
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Modul 9 - Web Server</title>
</head>
<body>
    <h1>Halo dari Modul 9!</h1>
    <p>Halaman ini digunakan untuk menguji ulang web server sederhana berbasis
    TCP socket programming yang telah dirapikan dengan komentar penjelasan
    tiap baris kode.</p>
</body>
</html>
```

## Hasil Pengujian
Server dijalankan dengan `python3 server.py`, lalu diakses lewat browser di `http://localhost:9999/HelloWorld.html`. Halaman "Halo dari Modul 9!" tampil dengan benar, menandakan server berhasil membaca file HTML dari disk dan mengirimkannya kembali sebagai respons HTTP yang valid — sama seperti hasil Modul 8, hanya berjalan di port yang berbeda.

## Kesimpulan
Merapikan ulang kode yang sudah berjalan (refactoring) dengan menambahkan komentar pada setiap baris terbukti membantu memahami alur program secara lebih detail — mulai dari pembuatan socket, proses bind dan listen, sampai bagaimana server membaca dan mengirim isi file ke client. Menjalankan di port berbeda juga menunjukkan bahwa satu komputer bisa menjalankan beberapa server TCP sekaligus, selama masing-masing memakai port yang berbeda.
