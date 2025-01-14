import socket
import struct
import time
from threading import Thread
from Error_handler import ErrorHandler
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
# Server configuration
serverIP = '192.168.1.24'  # Replace with your specific IP
serverUDPPort = 12000
serverTCPPort = 12345
magic_cookie = 0xabcddcba
error_handler = ErrorHandler()

try:

    # Create UDP socket
    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSocket.bind((serverIP, serverUDPPort))

    # Increase send buffer size for UDP
    udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024)

    # Create TCP socket
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSocket.bind((serverIP, serverTCPPort))
    tcpSocket.listen(5)

    print(f"{GREEN}Server started, listening on IP address {serverIP}{GREEN}")
except Exception as e:
    error_handler.handle_error(f"{RED}Error initializing server sockets{RED}", e)
    exit(1)

# Broadcast offers via UDP
def send_offer():
    """
        Sends periodic offer messages via UDP broadcast.

        Description:
            This function broadcasts a structured offer message over UDP to all clients
            on the network. The offer contains a magic cookie, message type, and the
            server's UDP and TCP port numbers. It runs continuously, sending the
            broadcast every 1 second. If an error occurs, it is logged using the
            `ErrorHandler`.

        Args:
            None

        Returns:
            None
    """
    try:
        offer_message = struct.pack('!IBHH', magic_cookie, 0x2, serverUDPPort, serverTCPPort)
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            broadcast_socket.sendto(offer_message, ('<broadcast>', serverUDPPort))
            time.sleep(1)
    except Exception as e:
        error_handler.handle_error(f"{RED}Error in send_offer,coudnlt send the offer{RED}", e)

# Handle a single UDP request
def handle_single_udp_request(message, clientAddress):
    """
        Description:
            This function processes a UDP request sent by a client. It first validates the request
            by checking the message size and magic cookie. If the request is valid, it extracts the
            requested file size and sends the data back to the client in chunks. Each chunk is
            accompanied by a payload header that includes the magic cookie, message type, and segment
            information. If an error occurs during processing, it is logged using the `ErrorHandler`.

        Args:
            message (bytes): The incoming UDP request message sent by the client.
            clientAddress (tuple): A tuple containing the client's IP address and port.

        Returns:
            None
    """
    try:
        # Parse the request
        if len(message) != 13:  # Expected size for '!IBQ'
            return

        header = struct.unpack('!IBQ', message)
        if header[0] != magic_cookie or header[1] != 0x3:
            print(f"\n{YELLOW}Ignoring invalid message from {clientAddress}. Incorrect magic cookie or type.")
            return

        file_size = header[2]
        print(f"\n{YELLOW}UDP client {clientAddress} requested {file_size} bytes.{YELLOW}")

        # Send payload in chunks
        segment_count = file_size // 1024 + (1 if file_size % 1024 else 0)
        for segment_number in range(segment_count):
            payload_header = struct.pack('!IBQQ', magic_cookie, 0x4, segment_count, segment_number)
            payload_data = b'a' * min(1024, file_size - segment_number * 1024)
            udpSocket.sendto(payload_header + payload_data, clientAddress)
        print(f"\n{GREEN}Completed UDP transfer to {clientAddress}{GREEN}")
    except Exception as e:
        error_handler.handle_error(f"\n{RED}Error handling UDP request from {clientAddress}{RED}", e)


# Handle all UDP requests
def handle_udp_requests():
    """
        Handles incoming UDP requests from clients.

        Description:
            This function listens for incoming UDP messages from clients on the specified socket.
            When a message is received, it spawns a new thread to process the request using the
            `handle_single_udp_request` function. This allows multiple UDP requests to be processed
            concurrently. If an exception occurs, it is logged using the `ErrorHandler`.

        Args:
            None

        Returns:
            None
    """
    try:
        while True:
            message, clientAddress = udpSocket.recvfrom(2048)
            Thread(target=handle_single_udp_request, args=(message, clientAddress), daemon=True).start()
    except Exception as e:
        error_handler.handle_error(f"{RED}Error in handle_udp_requests{RED}", e)

# Handle TCP clients
def handle_client(client_socket, client_address):
    """
        Handles a single TCP client request.

        Description:
            This function manages the interaction with a single TCP client. It first receives the
            requested file size from the client. Once the file size is received and validated, it sends
            the requested amount of data to the client in chunks of 1KB. The process continues until the
            full file size has been sent. If no file size is received or an error occurs during the
            process, the connection is closed.

        Args:
            client_socket (socket.socket): The socket object for the TCP connection with the client.
            client_address (tuple): A tuple containing the client's IP address and port.

        Returns:
            None
    """
    #Receive the file size requested by the client
    file_size_request = client_socket.recv(1024).decode('utf-8').strip()
    if not file_size_request:
        print(f"\n{YELLOW}No file size received from {client_address}{YELLOW}")
        client_socket.close()
        return

    file_size = int(file_size_request)
    print(f"\n{YELLOW}TCP client requested {file_size} bytes.{YELLOW}")

    #Send the requested amount of data in chunks
    bytes_sent = 0
    chunk_size = 1024  # Sending 1KB chunks , standard size
    while bytes_sent < file_size:
        remaining = file_size - bytes_sent
        to_send = b'x' * min(chunk_size, remaining)
        client_socket.sendall(to_send)
        bytes_sent += len(to_send)

    print(f"\n{GREEN}Finished sending {bytes_sent} bytes to {client_address}{GREEN}")


def handle_tcp_clients():
    """
        Handles incoming TCP client connections.

        Description:
            This function listens for incoming TCP connections on the server's TCP socket. When a client connects,
            it accepts the connection and spawns a new thread to handle the client using the `handle_client` function.
            This allows the server to process multiple TCP clients concurrently. If an exception occurs during the
            connection process, the error is logged using the `ErrorHandler`.

        Args:
            None

        Returns:
            None
    """
    try:
        while True:
            client_socket, client_address = tcpSocket.accept()
            print(f"\n{GREEN}TCP connection established with {client_address}{GREEN}")
            Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()
    except Exception as e:
        error_handler.handle_error(f"{RED}Error in handle_tcp_clients{RED}", e)

# Start the server threads
Thread(target=send_offer, daemon=True).start()
Thread(target=handle_udp_requests, daemon=True).start()
Thread(target=handle_tcp_clients, daemon=True).start()

# Keep the main thread alive
try:
    while True:
        time.sleep(1)
    else:
        print(f"\n{RED}Shutting down the server{RED}")
        udpSocket.close()
        tcpSocket.close()
except KeyboardInterrupt as e:
    print(f"\n{RED}Shutting down the server.{RED}")
    error_handler.handle_error("Error in main", e)