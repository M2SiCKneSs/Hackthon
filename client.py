import socket
import time


def tcp_client(server_ip, server_port, file_size):
    try:
        # Create the client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        print(f"Connected to server at {server_ip}:{server_port}")

        # Send the file size to the server
        client_socket.send(f"{file_size}\n".encode('utf-8'))
        print(f"Requested file size: {file_size} bytes")

        # Start receiving data
        start_time = time.time()
        bytes_received = 0

        while bytes_received < file_size:
            data = client_socket.recv(1024)  # Receive 1 KB at a time
            if not data:
                break
            bytes_received += len(data)

        # Calculate transfer stats
        end_time = time.time()
        duration = end_time - start_time
        transfer_rate = bytes_received / duration / (1024 * 1024)  # Convert to MB/s

        print(f"Received {bytes_received} bytes in {duration:.2f} seconds ({transfer_rate:.2f} MB/s).")
    except Exception as e:
        print(f"Error in client: {e}")
    finally:
        # Ensure the socket is closed
        client_socket.close()


if __name__ == '__main__':
    server_ip = '10.100.102.13'  # Replace with the server's IP address
    server_port = 12345  # Port to connect to (must match server)
    file_size = 10 * 1024 * 1024   # Example: 10 MB
    tcp_client(server_ip, server_port, file_size)