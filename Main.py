import client
from server import tcpserver

#define server ip and server port
serverIP = '192.168.1.24'  # Replace with your machine's IP
serverPort = 12000

tcpserver(serverIP,serverPort)
client.send_data_tcp(serverIP,serverPort)