# Author: Nguyen Dang Manh Cuong
# Created on: 2025-05-16

import wmi
import psutil
class GatheringInformation:
    def __init__(self, ip, user, password):
        self.host = ip
        self.user = user
        self.password = password
        self.conn = None
        print("[+] Starting the program...")

    def create_session(self):
        try:
            self.conn = wmi.WMI(computer=self.host,user=self.user,password=self.password)
            print("[+] Connected to server successfully!")
            print("-"*10+"OS INFOR"+"-"*10)
            for os in self.conn.win32_OperatingSystem(): 
                print(os)
            print("-"*10+"PROCESS INFOR"+"-"*10)
            for process in self.conn.win32_Process():
                print(process)
            print("-"*10+"LOGS INFOR"+"-"*10)
            for logs in self.conn.win32_NTLogEvent(Logfile="security"):
                print(logs)
        except Exception as e:
            print(f"[-] Failed to connect to server: {e}")
        finally:
            print("[+] The program has run completed!")

# Replace with actual IP, domain\user, and password
john = GatheringInformation("192.168.1.2", "PentestAD\\Administrator", "123ABC@")
john.create_session()
