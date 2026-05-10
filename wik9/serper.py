from socket import *
import threading

def handle_client(connectionSocket):
    try:
        # menerima pesan user
        message = connectionSocket.recv(1024).decode()
        # index.html, hello.html
        # message = /GET /index.html HTTP /1.1
        message = message[4:16]
        # membuka index index.html serta menghilangkan "/"
        # membaca file html
        file = open("wik9/"+message[1:])
        outputData = file.read()
        
        # kirim respon
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

        # kirim data
        connectionSocket.sendall(outputData.encode())

        # tutup koneksi
        connectionSocket.close()

    except IOError:
        # kirim respon bila tidak ditemukan
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())

        # kirim data 404
        connectionSocket.send("<h1>404 Not Found</h1>".encode())

        # tutup koneksi
        connectionSocket.close()


serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', 6789))
serverSocket.listen(5) # dapat menerima sebanyak 5 client
print("[SYSTEM] server is running....")

while True:
    connectionSocket, addr = serverSocket.accept()
    
    # membuat thread dan target thread, beserta parameternya
    thread = threading.Thread(
        target=handle_client,
        args=(connectionSocket,)
    )
    # menjalankan
    thread.start()