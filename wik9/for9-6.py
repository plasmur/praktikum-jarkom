from socket import *
import threading

def handle_client(connectionSocket):
    try:
        # menerima pesan user
        message = connectionSocket.recv(1024).decode()

        # mengambil nama file dari request
        message = message[4:16]

        # membuka file dari folder wik9
        file = open("wik9/" + message[1:])
        outputData = file.read()

        # kirim respon berhasil
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

        # kirim data HTML
        connectionSocket.sendall(outputData.encode())

        # tutup koneksi
        connectionSocket.close()

    except IOError:
        # kirim respon bila file tidak ditemukan
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())

        # kirim data 404
        connectionSocket.send("<h1>404 Not Found</h1>".encode())

        # tutup koneksi
        connectionSocket.close()


serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', 6789))
serverSocket.listen(5)

print("[SYSTEM] server is running....")

while True:
    connectionSocket, addr = serverSocket.accept()

    # membuat thread baru untuk setiap client
    thread = threading.Thread(
        target=handle_client,
        args=(connectionSocket,)
    )

    # menjalankan thread
    thread.start()