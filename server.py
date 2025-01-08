from socket import *

# Use your IP address and port
serverIP = '192.168.1.24'  # Replace with your machine's IP
serverPort = 12000

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverIP, serverPort))
serverSocket.listen(1)
print("Server is ready to receive on", serverIP)

while True:
    connectionSocket, addr = serverSocket.accept()
    print("Connection from:", addr)
    sentence = connectionSocket.recv(1024).decode()
    modifiedSentence = sentence.upper()
    connectionSocket.send(modifiedSentence.encode())
    connectionSocket.close()
