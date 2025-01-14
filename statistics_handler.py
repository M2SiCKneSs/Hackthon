import time
import csv
import os
import threading

class StatisticsHandler:
    """
       A thread-safe utility class for storing, managing, and saving TCP and UDP connection statistics to a CSV file.

       Attributes:
           results (list): A list to store all results (both TCP and UDP).
           csv_file (str): The name of the CSV file where statistics are saved. Defaults to "statistics.csv".
           lock (threading.Lock): A threading lock to ensure thread-safe access to shared resources.
    """
    def __init__(self, csv_file="statistics.csv"):
        """
                Initializes the StatisticsHandler instance, setting up the results list and ensuring the CSV file has the correct headers.

                Args:
                    csv_file (str, optional): The name of the CSV file to write statistics to. Defaults to "statistics.csv".
        """
        self.results = []  # Combined list for all results (TCP/UDP)
        self.csv_file = csv_file
        self.lock = threading.Lock()  # Mutex for thread safety

        # Create the CSV file with headers if it doesn't exist
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Run Timestamp", "Protocol", "Connection ID", "File Size (Bytes)",
                    "Elapsed Time (s)", "Speed (bits/s)", "Success Rate (%)", "Lost Packets"
                ])

    def add_tcp_result(self, connection_id, file_size, elapsed_time, speed):
        """
               Adds a TCP connection's statistics to the results list.

               Args:
                   connection_id (int): The ID of the TCP connection.
                   file_size (int): The total size of the file transferred in bytes.
                   elapsed_time (float): The total time taken for the transfer in seconds.
                   speed (float): The calculated speed of the transfer in bits per second.
        """
        with self.lock:
            self.results.append({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "protocol": "TCP",
                "connection_id": connection_id,
                "file_size": file_size,
                "elapsed_time": elapsed_time,
                "speed": speed,
                "success_rate": None,
                "lost_packets": None
            })

    def add_udp_result(self, connection_id, file_size, elapsed_time, speed, success_rate, lost_packets):
        """
               Adds a UDP connection's statistics to the results list.

               Args:
                   connection_id (int): The ID of the UDP connection.
                   file_size (int): The total size of the file transferred in bytes.
                   elapsed_time (float): The total time taken for the transfer in seconds.
                   speed (float): The calculated speed of the transfer in bits per second.
                   success_rate (float): The percentage of packets successfully received.
                   lost_packets (int): The number of packets lost during the transfer.
        """
        with self.lock:
            self.results.append({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "protocol": "UDP",
                "connection_id": connection_id,
                "file_size": file_size,
                "elapsed_time": elapsed_time,
                "speed": speed,
                "success_rate": success_rate,
                "lost_packets": lost_packets
            })

    def save_statistics_to_csv(self):
        """
               Saves all collected statistics to the CSV file and clears the results list.

               Args:
                   None

               Returns:
                   None
        """
        with self.lock:
            with open(self.csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                for result in self.results:
                    writer.writerow([
                        result["timestamp"],
                        result["protocol"],
                        result["connection_id"],
                        result["file_size"],
                        result["elapsed_time"],
                        result["speed"],
                        result["success_rate"],
                        result["lost_packets"]
                    ])
            self.results.clear()  # Clear results after saving