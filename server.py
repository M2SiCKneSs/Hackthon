from socket import *

# Use your IP address and port
serverIP = '132.73.193.241'  # Replace with your machine's IP
serverPort = 12000

def tcpserver(serverIP,serverPort):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((serverIP, serverPort))
    serverSocket.listen(1)
    print(f"\033[0;32mServer started, listening on IP address {serverIP}\033[0;32m")

    while True:
        connectionSocket, addr = serverSocket.accept()
        print("Connection from:", addr)
        sentence = connectionSocket.recv(1024).decode() #reads up to 1024 bytes of data
        modifiedSentence = sentence.upper()
        connectionSocket.send(modifiedSentence.encode())
        connectionSocket.close()
tcpserver(serverIP,serverPort)