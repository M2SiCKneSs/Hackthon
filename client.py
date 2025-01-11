import socket
import time


def receive_broadcast():
    """Listen for the server's broadcast message."""
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    clientSocket.bind(('', serverUDPPort))
    clientSocket.settimeout(broadcast_timeout)
    try:
        message, serverAddress = clientSocket.recvfrom(2048)
        header = struct.unpack('!IBHH', message)
        if header[0] == magic_cookie and header[1] == 0x2:
            print(f"Offer received from {serverAddress[0]}: UDP Port {header[2]}, TCP Port {header[3]}")
            return serverAddress[0], header[2], header[3]
    except timeout:
        print("No broadcast received within timeout period.")
    finally:
        clientSocket.close()
    return None, None, None
def tcp_transfer(serverIP, tcpPort, file_size, connection_number, num_connections, results):
    """Run a single TCP transfer."""
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverIP, tcpPort))

    try:
        # Split the file size for each TCP connection
        segment_file_size = file_size // num_connections
        start_time = time.time()

        # Send request
        clientSocket.sendall(str(segment_file_size).encode('utf-8'))

        # Receive data
        received_bytes = 0
        print("Received offer ", serverIP)
        while received_bytes < segment_file_size:
            chunk = clientSocket.recv(1024)
            if not chunk:
                break
            received_bytes += len(chunk)

        # Calculate transfer summary
        end_time = time.time()
        elapsed_time = end_time - start_time
        speed = (segment_file_size * 8) / elapsed_time  # Speed in bits per second
        results.append((f"TCP transfer #{connection_number}", elapsed_time, speed))
    finally:
        clientSocket.close()

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

def main():
    # Step 1: Receive broadcast
    serverIP, udpPort, tcpPort = receive_broadcast()
    if not serverIP:
        print("No server found. Exiting.")
        return

    # Step 2: Enter test parameters
    file_size = int(input("Enter file size to request (in bytes): ").strip())
    num_tcp_connections = int(input("Enter number of TCP connections: ").strip())


    num_udp_connections = int(input("Enter number of UDP connections: ").strip())
    print(f"Listening for server broadcast on UDP port {serverUDPPort}...")
    # Step 3: Run tests using threads
    threads = []
    results = []

    # Start TCP connections
    for i in range(num_tcp_connections):
        thread = threading.Thread(target=tcp_transfer, args=(serverIP, tcpPort, file_size, i + 1, num_tcp_connections, results))
        threads.append(thread)
        thread.start()

    # Start UDP connections
    for i in range(num_udp_connections):
        thread = threading.Thread(target=udp_transfer, args=(serverIP, udpPort, file_size, i + 1, num_udp_connections, results))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Step 4: Display results
    for result in results:
        if "TCP" in result[0]:
            print(f"{result[0]} finished, total time: {result[1]:.2f} seconds, total speed: {result[2]:.2f} bits/second.")
        elif "UDP" in result[0]:
            print(f"{result[0]} finished, total time: {result[1]:.2f} seconds, total speed: {result[2]:.2f} bits/second, percentage of packets received successfully: {result[3]:.2f}%.")

    print("\nAll transfers complete, listening to offer requests")


if __name__ == '__main__':
    server_ip = '10.100.102.13'  # Replace with the server's IP address
    server_port = 12345  # Port to connect to (must match server)
    file_size = 10 * 1024 * 1024   # Example: 10 MB
    tcp_client(server_ip, server_port, file_size)
