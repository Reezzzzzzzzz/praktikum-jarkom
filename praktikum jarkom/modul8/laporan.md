# Modul 8 — Web Server Sederhana Berbasis TCP Socket

## Tujuan
Setelah mencoba socket UDP di Modul 7, modul ini melanjutkan ke socket TCP dengan studi kasus yang lebih konkret: membangun web server sederhana yang bisa melayani permintaan HTTP GET dari browser, lengkap dengan penanganan kasus file tidak ditemukan (404).

## Implementasi

### `web_server.py`

```python
from socket import *
import sys

# Buat socket server dengan IPv4 (AF_INET) dan TCP (SOCK_STREAM)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Server akan mendengarkan permintaan di port ini
serverPort = 6789
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while True:
    # Menunggu dan menerima koneksi baru dari client
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
        # Membaca request line yang dikirim oleh client (browser)
        message = connectionSocket.recv(1024).decode()

        # Mengambil nama file yang diminta dari request, contoh: "GET /HelloWorld.html HTTP/1.1"
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

### Penjelasan Alur Kode
1. Socket dibuat dengan `SOCK_STREAM` (TCP), berbeda dari `SOCK_DGRAM` pada Modul 7.
2. Server di-*bind* ke port 6789, lalu `listen(1)` membuatnya siap menerima maksimal 1 koneksi yang menunggu di antrean.
3. Di dalam loop utama, `accept()` akan **memblokir** eksekusi sampai ada client yang benar-benar terhubung — ini berbeda dari UDP yang langsung membaca datagram begitu tiba, tanpa proses koneksi.
4. Begitu terhubung, server membaca request line dari client (contoh: `GET /HelloWorld.html HTTP/1.1`), lalu mengambil nama file-nya dengan `message.split()[1]`.
5. Jika file ditemukan, isinya dibaca lalu dikirim balik ke client didahului header `HTTP/1.1 200 OK`.
6. Jika file tidak ditemukan, `open()` akan melempar `IOError`, yang langsung ditangkap untuk mengirim balasan `404 Not Found` beserta halaman error sederhana.
7. Koneksi ditutup setiap selesai melayani satu permintaan, dan server kembali ke awal loop untuk menunggu koneksi berikutnya.

### Halaman Uji (`HelloWorld.html`)

```html
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Tes Web Server</title>
</head>
<body>
    <h1>Halo, Web Server!</h1>
    <p>Jika halaman ini muncul di browser, berarti web server TCP sederhana
    yang dibuat pada Modul 8 berhasil melayani permintaan HTTP GET dari client.</p>
</body>
</html>
```

## Cara Menjalankan dan Hasil
1. Jalankan `python3 web_server.py`. Server akan menampilkan `Ready to serve...` dan menunggu koneksi.
2. Buka browser, akses `http://localhost:6789/HelloWorld.html`.
3. Halaman "Halo, Web Server!" berhasil ditampilkan di browser, menandakan server berhasil membaca file di disk dan mengirimkannya sebagai respons HTTP 200 OK.
4. Sebagai pembanding, mengakses file yang tidak ada (misalnya `http://localhost:6789/tidakada.html`) memunculkan halaman `404 Not Found` sesuai blok `except IOError` di kode.

## Kesimpulan
* Socket TCP membutuhkan tahap `listen()` dan `accept()` sebelum bisa berkomunikasi dengan client, berbeda dari UDP yang langsung menerima data tanpa proses koneksi.
* Implementasi web server paling dasar pada akhirnya hanyalah soal membaca request, mencari file yang diminta di disk, dan mengirimkan isinya kembali dengan header HTTP yang sesuai.
* Penanganan error (404) penting agar server tidak crash begitu saja ketika client meminta file yang tidak ada.
