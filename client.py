from socket import *
serverIP = '132.73.193.241'
serverPort = 12000



def send_data_tcp(serverIP,serverPort):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverIP, serverPort))
    sentence = input('Input lowercase sentence: ')
    clientSocket.send(sentence.encode())

    modifiedSentence = clientSocket.recv(1024).decode() #reads up to 1024 byts of data
    print('From Server:', modifiedSentence)

    clientSocket.close()
send_data_tcp(serverIP,serverPort)
