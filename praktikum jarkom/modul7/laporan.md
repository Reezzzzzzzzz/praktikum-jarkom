# Modul 7 — Socket Programming UDP

## Tujuan
Setelah memahami protokol UDP secara konsep di Modul 5, modul ini mempraktikkan langsung bagaimana membuat aplikasi client-server sederhana berbasis UDP menggunakan socket programming di Python.

## Konsep Dasar
Berbeda dengan TCP, UDP tidak membentuk koneksi terlebih dahulu (*connectionless*). Setiap kali mengirim data, alamat tujuan harus selalu disertakan secara eksplisit pada pemanggilan `sendto()`, dan setiap kali menerima data, alamat pengirimnya otomatis ikut diberikan lewat `recvfrom()`. Tidak ada proses handshake seperti SYN/SYN-ACK/ACK pada TCP.

## Implementasi

### 1. Server (`udp_server.py`)

```python
from socket import *

# Server akan mendengarkan di port ini
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

print('Server UDP siap menerima pesan di port', serverPort)

while True:
    # UDP tidak memiliki konsep koneksi, jadi setiap kali ada data
    # masuk, server langsung membacanya bersama alamat pengirimnya
    message, clientAddress = serverSocket.recvfrom(2048)

    # Ubah isi pesan menjadi huruf kapital sebagai bentuk balasan
    modifiedMessage = message.decode().upper()

    # Kirim balasan langsung ke alamat client yang tadi mengirim pesan
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
```

Socket dibuat dengan `SOCK_DGRAM` (bukan `SOCK_STREAM` seperti TCP) untuk menandai bahwa ini adalah socket UDP. Server di-*bind* ke port 12000, lalu masuk ke loop tanpa henti: menunggu datagram masuk lewat `recvfrom()`, mengubah isinya menjadi huruf kapital, lalu mengirim balasannya langsung ke alamat client yang tercatat — tanpa perlu `accept()` seperti pada TCP, karena memang tidak ada koneksi yang harus dibangun.

### 2. Client (`udp_client.py`)

```python
from socket import *

serverName = '127.0.0.1'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

message = input('Masukkan kalimat yang ingin dikirim: ')

# Kirim pesan ke server. Karena UDP, kita harus menyertakan
# alamat tujuan setiap kali mengirim data (tidak ada handshake)
clientSocket.sendto(message.encode(), (serverName, serverPort))

# Tunggu balasan dari server
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

print('Balasan dari server:', modifiedMessage.decode())

clientSocket.close()
```

Client meminta input dari pengguna, mengirimkannya ke alamat dan port server lewat `sendto()`, lalu menunggu balasan lewat `recvfrom()`. Setelah balasan diterima dan ditampilkan, socket ditutup.

## Cara Menjalankan
1. Jalankan `python3 udp_server.py` di satu terminal — server akan menunggu pesan masuk tanpa henti.
2. Di terminal lain, jalankan `python3 udp_client.py`, lalu masukkan kalimat apa saja.
3. Client akan menampilkan balasan dari server berupa kalimat yang sama, tapi dalam huruf kapital semua.

## Hasil Pengujian
Pengujian dilakukan dengan mengirim kalimat `"halo dari client"` dari client ke server. Server menerima pesan tersebut, mengubahnya menjadi `"HALO DARI CLIENT"`, dan mengirimkannya balik — client berhasil menampilkan balasan tersebut sesuai yang diharapkan, membuktikan bahwa komunikasi dua arah lewat UDP socket berjalan dengan benar.

## Kesimpulan
* UDP socket programming jauh lebih sederhana dibanding TCP karena tidak ada proses `listen()`/`accept()` untuk membangun koneksi.
* Setiap pengiriman data lewat UDP wajib menyertakan alamat tujuan secara eksplisit, karena tidak ada "jalur" yang sudah terbentuk sebelumnya seperti pada TCP.
* Karena sifatnya yang ringan, UDP cocok untuk aplikasi sederhana semacam ini, tapi pengirim juga harus sadar bahwa UDP tidak menjamin data benar-benar diterima (tidak ada retransmission otomatis seperti TCP).
