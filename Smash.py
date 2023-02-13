#!/usr/bin/python

import logging
import click
import scapy
from scapy.layers.inet import IP, TCP
from scapy.packet import Raw
from scapy.sendrecv import sr1, sendp
#from scapy.all import *
from scapy.utils import rdpcap, hexdump, wrpcap


@click.command()
@click.option("--lowres", "-l", default='low.m3u8', help="Low resolution video in .m3u8")
@click.option("--highres", "-h", default='high.m3u8', help="High resolution video in .m3u8")
@click.option("--textmessage", "-t", default='Hello, World', help="Text message to be hidden in file")
@click.option("--filemessage", "-f", default='C:\\Users\\livia\\PycharmProjects\\SMASH\\message.idk',
              help="File message to be hidden in file")
def main(lowres, highres, textmessage, filemessage):
    # for actual steg process
    if textmessage != "":
        click.echo("Files: " + highres + " and " + lowres + ". Message: " + textmessage)
        connect_to_server()
    else:
        click.echo("Files: " + highres + " and " + lowres + ". Message: " + filemessage)


def connect_to_server():
    """syn = IP(dst='3.227.232.81') / TCP(dport=80, flags='S')
    syn_ack = sr1(syn)
    getStr = 'GET / HTTP/1.1\r\nHost: 3.227.232.81\r\n\r\n'
    request = IP(dst='3.227.232.81') / TCP(dport=80, sport=syn_ack[TCP].dport, seq=syn_ack[TCP].ack,
                                           ack=syn_ack[TCP].seq + 1, flags='A') / getStr
    reply = sr1(request)"""


    packets = rdpcap("pack3.pcap")
    c = 0
    listp = []
    newPackets = []

    for packet in packets:
        if packet.haslayer(Raw):
            temp = packet["Raw"].load
            ind = temp.find(b'\xff\xff\xff\xff\xff\xff\xff\xff\xff')
            if ind != -1:
                i = ind
                b = temp[i]
                for byte in temp:
                    while (b == '\xff'):
                        b = temp[i]
                        i += 1
                num = (i - 4) - (ind + 4) #number of bytes I can hide info in
                strt = ind + 4

                #inserting that number of bytes (num) from secret message (use zeros)
                for byte in temp:
                    while strt < i - 4:
                        temp[strt] = b'00'
                        strt += 1

                packet["Raw"].load = temp
                listp.append(c)
        newPackets.append(packet)
        c += 1


    wrpcap('newpack.pcap', newPackets) #may want a file name with a comma
        ## after can look up in wireshark to validate it worked
    print(listp)



if __name__ == "__main__":
    """
    This initiates and calls the main function for this application. 

    Generally, this should be the last bit of code in this script.
    """
    logging.basicConfig(level=logging.DEBUG)
    main()
