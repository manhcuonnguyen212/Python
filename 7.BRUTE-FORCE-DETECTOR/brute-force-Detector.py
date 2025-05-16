from scapy.all import *
def full_Duplex_session(x):
    sess = 'other'
    if x.haslayer('Ether'):
    else:
        sess = print('{}'.format())
def main():

    try: 
        captured_packets = sniff(offline="ftp.pcap")
    except Exception as e:
        print(e)
    FullduplexSessions = {}
    for packet in captured_packets: 
        session = full_Duplex_Session(packet)
main()