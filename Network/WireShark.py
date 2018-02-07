#from __future__ import print_function

import winreg as reg

from scapy.all import *

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


ADAPTER_KEY = r'SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}'

OpenVpnPath = "C:\\Program Files\\OpenVPN\\bin\\openvpn.exe"
ConfigPath = os.environ['USERPROFILE']+"\\OpenVPN\\config"

ConfTcp= "C:\\Users\\quent\\Downloads\\ovpn\\ovpn_tcp\\uk298.nordvpn.com.tcp.ovpn"
ConfUdp= "C:\\Users\\quent\\Downloads\\ovpn\\ovpn_udp\\uk298.nordvpn.com.udp.ovpn"

ConnectionKey = "SYSTEM\\CurrentControlSet\\Control\\Network\\{4D36E972-E325-11CE-BFC1-08002BE10318}"
interfaces = []
with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, ADAPTER_KEY) as adapters:
    try:
        for i in range(10000):
            key_name = reg.EnumKey(adapters, i)
            with reg.OpenKey(adapters, key_name) as adapter:
                try:
                    interfaces.append(reg.QueryValueEx(adapter, 'DriverDesc')[0])
                except :
                    pass

    except:
        pass

print(interfaces[6])

#conf.color_theme=RastaTheme

#Description du nom de la carte wifi
conf.iface=interfaces[6]

"""
def packet_callback(packet):
    if packet[TCP].payload:
        pkt = str(packet[TCP].payload)
        if packet[IP].dport == 80:
            print("\n{} ----HTTP----> {}:{}:\n{}".format(packet[IP].src, packet[IP].dst, packet[IP].dport, str(bytes(packet[TCP].payload))))

sniff(filter="tcp", prn=packet_callback, store=0) """
pkt = []

#pkt = sniff(prn=lambda x: x.summary())
#print(pkt.summary())

packet = {}
cpt_pkt =0


def packet_callback(pkt):
    global cpt_pkt
    if pkt.haslayer(TCP):

        packet[cpt_pkt]= {}
        packet[cpt_pkt]["source_Port"] = pkt[TCP].sport
        packet[cpt_pkt]["destination_Port"] = pkt[TCP].dport

        print("Port Src:", packet[cpt_pkt]["source_Port"], "Port Dst:", packet[cpt_pkt]["destination_Port"])

    if pkt.haslayer(IP):

        packet[cpt_pkt]= {}
        packet[cpt_pkt]["source_IP"] = pkt[IP].src
        packet[cpt_pkt]["destination_IP"] = pkt[IP].dst
        packet[cpt_pkt]["ttl"] = pkt.ttl
        print("IP Src:", packet[cpt_pkt]["source_IP"], "Ip Dst:", packet[cpt_pkt]["destination_IP"])

    packet[cpt_pkt] = {}
    packet[cpt_pkt]["source_MAC"] = pkt.src
    packet[cpt_pkt]["destination_MAC"] = pkt.dst
    print("Mac Src:", packet[cpt_pkt]["source_MAC"], "Mac Dst:", packet[cpt_pkt]["destination_MAC"])

    cpt_pkt += 1
    #pkt.show()


pkt = sniff(count=10, prn=packet_callback, filter="tcp")


wrpcap('packets.pcap', pkt)
print(cpt_pkt)

i=0

print("boucle debut\n")
for cle, valeur in packet.items():
    for key, value in packet[i].items():
        print(key, value)
        i =+1

print("boucle fin\n")

print("Packet 2\n")
print(packet[6])

print("Info packet 2 (IP:Port)\n")
print(packet[4]["source_IP"]+":"+packet[4]["source_Port"]+ "------>"+ packet[4]["destination_IP"]+":"+packet[4]["destination_Port"])
