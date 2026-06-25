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
