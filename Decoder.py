
from pytz import unicode
from scapy.layers.inet import IP
from scapy.packet import Raw
from scapy.utils import rdpcap


def decode():
    """syn = IP(dst='3.227.232.81') / TCP(dport=80, flags='S')
    syn_ack = sr1(syn)
    getStr = 'GET / HTTP/1.1\r\nHost: 3.227.232.81\r\n\r\n'
    request = IP(dst='3.227.232.81') / TCP(dport=80, sport=syn_ack[TCP].dport, seq=syn_ack[TCP].ack,
                                           ack=syn_ack[TCP].seq + 1, flags='A') / getStr
    reply = sr1(request)"""

    packets = rdpcap("newpackT.pcap")  # "reading" pcap file
    message = []

    for packet in packets:
        if packet.haslayer(Raw):
            temp = packet["Raw"].load

            ind = temp.find(b'\xff\xff\xff\xff')
            if ind != -1:  # checking that the four values above do exist in the packet
                second_temp = temp[ind + 4:]
                end = second_temp.find(b'\xff\xff\xff\xff')  # finding second instance of four 0xFF

                if end != -1:
                    target = temp[ind + 4:end]  # making a list of only the possible message
                    ntemp = ""
                    tar_wo = unicode(target, errors='ignore')  # allows target to be encoded without errors

                    if tar_wo.encode('utf-8') == target:
                        for i in target:
                            ntemp += chr(i)  # new temp for extracting the target in str form

                        if ntemp != "":
                            message.append(ntemp)



    print(message)


decode()
