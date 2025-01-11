import socket
import struct
import time
from threading import Thread

# Server configuration
serverIP = '192.168.1.24'  # Replace with your specific IP
serverUDPPort = 12000
serverTCPPort = 12345
magic_cookie = 0xabcddcba

# Create UDP socket
udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSocket.bind((serverIP, serverUDPPort))

# Create TCP socket
tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSocket.bind((serverIP, serverTCPPort))
tcpSocket.listen(5)

print(f"Server started, listening on IP address {serverIP}")

# Broadcast offers via UDP
def send_offer():
    offer_message = struct.pack('!IBHH', magic_cookie, 0x2, serverUDPPort, serverTCPPort)
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        broadcast_socket.sendto(offer_message, ('<broadcast>', serverUDPPort))
        time.sleep(1)

# Handle TCP clients
def handle_tcp_clients():
    """Handle incoming TCP client connections."""
    while True:
        client_socket, client_address = tcpSocket.accept()
        print(f"TCP connection established with {client_address}")

        def handle_client(client_socket, client_address):
            try:
                file_size_request = client_socket.recv(1024).decode('utf-8').strip()
                if not file_size_request:
                    print(f"No file size received from {client_address}")
                    client_socket.close()
                    return

                file_size = int(file_size_request)
                print(f"TCP client requested {file_size} bytes.")

                bytes_sent = 0
                chunk_size = 1024  # Sending 1KB chunks
                while bytes_sent < file_size:
                    remaining = file_size - bytes_sent
                    to_send = b'x' * min(chunk_size, remaining)
                    client_socket.sendall(to_send)
                    bytes_sent += len(to_send)

                print(f"Finished sending {bytes_sent} bytes to {client_address}")
            except Exception as e:
                print(f"Error during communication with {client_address}: {e}")
            finally:
                client_socket.close()

        Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()

# Start the server threads
Thread(target=send_offer, daemon=True).start()
Thread(target=handle_tcp_clients, daemon=True).start()

# Keep the main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutting down the server.")
    udpSocket.close()
    tcpSocket.close()