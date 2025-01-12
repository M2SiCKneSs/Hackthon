from socket import *
import struct
import time
import threading

# Configuration
magic_cookie = 0xabcddcba
serverUDPPort = 12000
broadcast_timeout = 10  # Time to listen for broadcast (in seconds)


def receive_broadcast():
    """Listen for the server's broadcast message."""
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    clientSocket.bind(('', serverUDPPort))
    clientSocket.settimeout(broadcast_timeout)

    print(f"Listening for server broadcast on UDP port {serverUDPPort}...")
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
def udp_transfer(serverIP, udpPort, file_size, connection_number, num_connections, results):
    """Run a single UDP transfer."""
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(15)

    try:
        # Split the file size for each UDP connection
        segment_file_size = file_size // num_connections
        start_time = time.time()

        # Send request
        request_message = struct.pack('!IBQ', magic_cookie, 0x3, segment_file_size)
        clientSocket.sendto(request_message, (serverIP, udpPort))

        # Receive data
        received_segments = 0
        total_segments = None
        while True:
            try:
                packet, _ = clientSocket.recvfrom(2048)

                if len(packet) < 21:
                    continue

                header = struct.unpack('!IBQQ', packet[:21])
                if header[0] != magic_cookie or header[1] != 0x4:
                    continue

                total_segments = header[2]
                received_segments += 1

                if received_segments == total_segments:
                    break
            except timeout:
                break

        # Calculate transfer summary
        end_time = time.time()
        elapsed_time = end_time - start_time
        speed = (segment_file_size * 8) / elapsed_time  # Speed in bits per second
        packet_success_rate = (received_segments / total_segments) * 100 if total_segments else 0
        results.append((f"UDP transfer #{connection_number}", elapsed_time, speed, packet_success_rate))
    finally:
        clientSocket.close()

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

if name == "__main__":
    main()
