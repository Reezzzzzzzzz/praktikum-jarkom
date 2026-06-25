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
