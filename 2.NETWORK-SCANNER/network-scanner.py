#Author: Nguyen Dang Manh Cuong
#Created on: 2025-05-15
from scapy.all import ARP,Ether,ICMP,IP,RandIP,sr,sr1,srp
import sys 
import time
import argparse 

class Scanner: 
    count = 1
    def __init__(self,network,host):
        print("[+] Network scanner is running!")
        self.IP = network
        self.Host = host
    # initialize IP variable
    def creating_ARP(self,x):
        # arp packet = ether/arp
        ARP_header = ARP(op=1,pdst=x,psrc="192.168.1.14")
        Ether_header = Ether(dst="ff:ff:ff:ff:ff:ff")
        ARP_packet = Ether_header/ARP_header
        if self.count==1:
            print(ARP_packet.display())
            self.count=2
        return ARP_packet

    def sending_packet(self):
        mac_listing = list()
        try:
            for x in range(1,255):
                x = self.IP+"." +str(x)
                ARP_packet = self.creating_ARP(x)
                response,unresponse = srp(ARP_packet,verbose=False,timeout=2)
                if response:
                    ip_mac = dict()
                    for y in response:
                        ip_mac[x] = y[1].hwsrc
                        break
                    mac_listing.append(ip_mac)
        except KeyboardInterrupt:
            print("[-]the program has stopped!")
        finally: 
            for x,y in mac_listing:
                    print(x+" -> "+y)
            sys.exit()
            print("[+]the process of scanning network has completed!")           
def main():
    try: 
        argment = argparse.ArgumentParser(description="Network scan tool")
        argment.add_argument('Subnetwork',type=str,help="Enter the Subnetwork that you want to scan")
        argment.add_argument('host',type=str,help="host ip")
        arg = argment.parse_args()
            # take ip from commandline
        sc = Scanner(arg.network,arg.host)
        sc.sending_packet()
    except Exception as e: 
        print("[-]An error has occured during running the program!: "+str(e))
#main()

