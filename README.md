# TCP-UDP Client-Server Application
This project implements a multithreaded client-server application that supports both TCP and UDP communication protocols. The server handles multiple client requests simultaneously, enabling efficient data transmission and a comparison of TCP vs. UDP performance.

## Features
### Server:

* Handles TCP and UDP connections concurrently.
* Broadcasts availability over UDP using periodic "offer" messages.
* Processes client requests to send data of a specified size.
* Supports multithreading to handle multiple clients simultaneously.
### Client:

* Discovers the server via UDP broadcast messages.
* Supports both TCP and UDP communication protocols for testing.
* Measures and compares the performance (speed and reliability) of TCP and UDP.
* Logs errors in a CSV file for debugging.


## How It Works
1. The server broadcasts periodic UDP "offer" messages on a configurable port.
2. The client listens for these broadcasts to discover the server.
3. The client sends a request to the server, specifying the desired file size and protocol (TCP or UDP).
4. The server responds:
   * For TCP: The server establishes a connection and sends the requested file in chunks.
   * For UDP: The server sends packets with segment information, ensuring no persistent connection.
5. The client measures the transfer time and logs the results for both TCP and UDP.

## Directory Structure
`|-- client.py        # The client application

|-- server.py        # The server application

|-- Error_handler.py # A utility for error handling and logging

|-- README.md        # Project documentation

|-- logs/            # Directory for CSV logs (auto-created by the ErrorHandler)
`
## Requirements
* Python 3.x 
* Libraries:
* socket (built-in)
* struct (built-in)
* threading (built-in)
* csv (built-in)

## Logging and Error Handling
* Errors are logged in a CSV file (logs/error_log.csv), generated automatically by the ErrorHandler module.
* Each error log entry includes:
* Timestamp
* Error message
* Exception details (if any)

## Key Features and Highlights
* Multithreaded Design: Enables the server to handle multiple clients concurrently.
* Dynamic UDP Discovery: Clients dynamically discover the server using UDP broadcasts.
* Chunked Data Transmission: Ensures reliable data transfer in both TCP and UDP modes.
* Error Handling: Comprehensive error logging for debugging and troubleshooting.
* Performance Testing: Compare TCP and UDP speeds for file transfers.

## Example Usage
### Server Console Output:
Server started, listening on IP address 192.168.1.24

TCP connection established with ('192.168.1.10', 54321)

Finished sending 1024 bytes to ('192.168.1.10', 54321)

UDP client ('192.168.1.20', 54322) requested 1024 bytes.

Completed UDP transfer to ('192.168.1.20', 54322)

### Client Console Output:
Received offer from 192.168.1.24

Enter file size to request (in bytes): 10240

Enter number of TCP connections: 1

Enter number of UDP connections: 1


TCP transfer #1 finished, total time: 2.34 seconds, total speed: 35.1 bits/second

UDP transfer #1 finished, total time: 1.98 seconds, total speed: 41.3 bits/second, percentage of packets received successfully: 98.7%

All transfers complete, listening to offer requests...

## License
This project is licensed under NO ONE!!! It's a free country, do whatever you want with it.