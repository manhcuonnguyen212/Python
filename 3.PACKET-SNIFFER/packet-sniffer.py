#Author: Nguyen Dang Manh Cuong
# Created on: 2025-05-15

from scapy.all import sniff
import argparse
class sniffer: 
    def __init__(self):
        print("[+]The program is running!") 
    def processing_packets(self,packets):
        if(packets.haslayer('ARP')):
            print(packets.summary())
    def sniffing_packets(self): 
        sniff(prn=self.processing_packets,iface='Wi-Fi',filter="tcp")
            # sniff function is used for sniffing packets in a specific interface
def main():
    try:
        Sniffer = sniffer()
        Sniffer.sniffing_packets()
    except Exception as e: 
        print("[-] An error has occured during running the program!: -> "+str(e))
main()