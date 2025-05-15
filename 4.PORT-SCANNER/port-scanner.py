# Author: Nguyen Dang Manh Cuong
# Created on: 2025-05-15

import argparse
import threading
import sys
from socket import socket, AF_INET, SOCK_STREAM, timeout
value = threading.Semaphore(1)
class PortScanner:
    def __init__(self, host, ports):
        print("[+] Starting the port scanner...")
        self.host = host
        self.ports = []
        self.parse_ports(ports)

    def parse_ports(self, ports):
        ### analyzing a range of ports
        try:
            if '-' in ports:
                start, end = map(int, ports.split('-'))
                self.ports = list(range(start, end + 1))
                ## list of ports 
            else:
                self.ports = [int(ports)]
        except ValueError:
            print("[-] Invalid port format. Use A-B or a single port (e.g., 22 or 20-25).")
            sys.exit(1)

    def tcp_connection(self, port):
        try:
            with socket(AF_INET, SOCK_STREAM) as conn:
                conn.settimeout(1)
                result = conn.connect_ex((self.host, port))
                value.acquire()
                if result == 0:
                    print(f"[+] Port {port} is OPEN on {self.host}")
        except timeout:
            print(f"[-] Timeout on port {port}")
        except Exception as e:
            print(f"[-] Error on port {port}: {e}")
        finally:
            value.release()

    def scan_ports(self):
        threads = []
        try:
            for port in self.ports:
                t = threading.Thread(target=self.tcp_connection, args=(port,))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

        except KeyboardInterrupt:
            print("\n[-] Scan interrupted by user.")
        except Exception as e:
            print(f"[-] Error during scan: {e}")
        finally:
            print("[+] Scan completed.")

def main():
    parser = argparse.ArgumentParser(description="Simple TCP Port Scanner")
    parser.add_argument("host", type=str, help="Target IP address or hostname")
    parser.add_argument("ports", type=str, help="Port or range (e.g., 80 or 20-25)")
    args = parser.parse_args()
    ## take arguments from command line
    scanner = PortScanner(args.host, args.ports)
    scanner.scan_ports()

if __name__ == "__main__":
    main()
