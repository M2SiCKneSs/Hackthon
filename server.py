import socket

# Server setup
HOST = '10.100.102.13'  # Connect to my network CHANGE IF NEEDED
PORT = 12345  # Port to listen on (ensure this is not in use)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # Listen for up to 5 connections

print(f"Server started, listening on IP address {HOST}:{PORT}")

try:
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        try:
            # Step 1: Receive the file size requested by the client
            file_size_request = client_socket.recv(1024).decode('utf-8').strip()
            if not file_size_request:
                print(f"No file size received from {client_address}")
                client_socket.close()
                continue

            file_size = int(file_size_request)
            print(f"Client requested {file_size} bytes of data.")

            # Step 2: Send the requested amount of data in chunks
            bytes_sent = 0
            chunk_size = 1024  # Sending 1KB chunks
            while bytes_sent < file_size:
                # Calculate how much to send in this iteration
                remaining = file_size - bytes_sent
                to_send = b'x' * min(chunk_size, remaining)
                client_socket.sendall(to_send)
                bytes_sent += len(to_send)

            print(f"Finished sending {bytes_sent} bytes to {client_address}")
        except Exception as e:
            print(f"Error during communication with {client_address}: {e}")
        finally:
            client_socket.close()
except KeyboardInterrupt:
    print("\nShutting down the server.")
    server_socket.close()
