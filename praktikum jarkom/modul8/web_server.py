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
