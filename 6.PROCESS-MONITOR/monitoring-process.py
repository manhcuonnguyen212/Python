#Author: Nguyen Dang Manh Cuong
#Created on: 2025-05-16
import psutil
import pprint
def process_listing():
    processes = list()
    for p in psutil.process_iter():
        try: 
            processes.append(p)
        except: 
            pass 
    return processes
def search_childrenProcess(process,dict):
    for x in process.children():
        if len(x.children()) == 0:
            dict[x.pid] = [x,len(x.children())]
        else:
            dict[x.pid] = [x,len(x.children()),{}]
            search_childrenProcess(x,dict[x.pid][2])
def process_dictionary(listing):
    processes = {}
    for p in listing: 
        if p.pid != 0 and psutil.pid_exists(p.pid):
            if len(p.parents()) == 0:
                if len(p.children()) == 0:
                    processes[p.pid] = [p,len(p.children())]
                else:
                    processes[p.pid] = [p,len(p.children()),{}]
                    search_childrenProcess(p,processes[p.pid][2])   
    return processes

def main(): 
    #print(process_listing())
    processes = process_dictionary(process_listing())
    pprint.pprint(processes)
main()