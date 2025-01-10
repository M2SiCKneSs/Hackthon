import socket

# Client setup
SERVER_IP = '10.100.102.13'  # Replace with the server's IP address
SERVER_PORT = 12345      # Port to connect to (must match server)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# Send and receive data
message = input("Enter message to send to the server: ")
client_socket.sendall(message.encode('utf-8'))

response = client_socket.recv(1024).decode('utf-8')
print(f"Response from server: {response}")

client_socket.close()
