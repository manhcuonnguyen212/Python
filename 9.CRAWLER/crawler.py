import requests
from termcolor import colored
import threading
value = threading.Semaphore(1)
class request:
    def __init__(self):
        print("[+] Requests creating....")
        ## domain
    def creating_requests(self,subdomain):
        try: 
            response = requests.get("https://"+subdomain,timeout=2)
            if response.status_code==200:
                
                value.acquire()
                print(subdomain) ## a critical section
                value.release()
        except:
            pass 
class domain_discoverer(request):
    def __init__(self,target):
        self.target = target
        print(colored("[+] Starting scan domain...",'green'))
    def discover(self):
        with open('D:\CodePyThon\PROJECT\Python\9.CRAWLER\subdomain.txt','r') as output:
            listing = list()
            for line in output:
                try:
                    subdomain = line.strip() + "." + self.target
                    t = threading.Thread(target=self.creating_requests,args=(subdomain,))
                    t.start()
                    listing.append(t)
                except Exception as e:
                    print(e)
                    break
            for x in listing:
                x.join()
class folder_discoverer(request):
    def __init__(self,target2):
        self.target2 = target2
        print(colored("[+] Starting scan folder...",'green'))
    def discover2(self):
        with open("D:\CodePyThon\PROJECT\Python\9.CRAWLER\\folder_file.txt",'r') as output:
            listing = list()
            for line in output:
                path = self.target2 + "/"+line.strip()
                t = threading.Thread(target=self.creating_requests,args=(path,))
                listing.append(t)
                t.start()
            for x in listing:
                t.join()                
crwler = domain_discoverer("ptithcm.edu.vn")
crwler.discover()
# crwler = folder_discoverer("ptithcm.edu.vn")
# crwler.discover2()