#!/usr/bin/python

import getopt
import logging
import sys
import click
import scapy
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sr1


@click.command()
@click.option("--lowres", "-l", default = 'low.m3u8', help = "Low resolution video in .m3u8")
@click.option("--highres", "-h", default = 'high.m3u8', help = "High resolution video in .m3u8")
@click.option("--textmessage", "-t", default = 'Hello, World',  help = "Text message to be hidden in file")
@click.option("--filemessage", "-f", default = 'C:\\Users\\livia\\PycharmProjects\\SMASH\\message.idk',  help = "File message to be hidden in file")

def main(lowres, highres, textmessage, filemessage):
    #for actual steg process
    if textmessage != "":
        click.echo("Files: " + highres + " and " + lowres + ". Message: " + textmessage)
    else:
        click.echo("Files: " + highres + " and " + lowres + ". Message: " + filemessage)

def connect_to_server():
    syn = IP(dst='3.227.232.81') / TCP(dport=80, flags='S')
    syn_ack = sr1(syn)
    getStr = 'GET / HTTP/1.1\r\nHost: 3.227.232.81\r\n\r\n'
    request = IP(dst='3.227.232.81') / TCP(dport=80, sport=syn_ack[TCP].dport, seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A') / getStr
    reply = sr1(request)

if __name__ == "__main__":
    """
    This initiates and calls the main function for this application. 

    Generally, this should be the last bit of code in this script.
    """
    logging.basicConfig(level=logging.DEBUG)
    main()
