#!/usr/bin/python

import logging

import click
from scapy.layers.inet import IP
from scapy.packet import Raw
# from scapy.all import *
from scapy.utils import rdpcap, wrpcap
from struct import *


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

    atwS = ("I walked through the door with you The air was cold But something about it felt like home somehow "
            "And I, left my scarf there at your sister's house And you've still got it in your drawer even now "
            "Oh, your sweet disposition And my wide-eyed gaze We're singing in the car, getting lost upstate "
            "Autumn leaves falling down like pieces into place And I can picture it after all these days "
            "And I know it's long gone and that magic's not here no more And I might be okay but I'm not fine at all "
            "'Cause there we are again on that little town street You almost ran the red 'cause you were lookin' over at me "
            "Wind in my hair, I was there I remember it all too well Photo album on the counter "
            "Your cheeks were turning red You used to be a little kid with glasses in a twin-sized bed "
            "And your mother's telling stories 'bout you on the tee-ball team You told me 'bout your past thinking your future was me "
            "And I know it's long gone and there was nothing else I could do And I forget about you long enough to forget why I needed to "
            "'Cause there we are again in the middle of the night We're dancing 'round the kitchen in the refrigerator light "
            "Down the stairs, I was there I remember it all too well, yeah And maybe we got lost in translation "
            "Maybe I asked for too much But maybe this thing was a masterpiece 'til you tore it all up "
            "Running scared, I was there I remember it all too well And you call me up again just to break me like a promise "
            "So casually cruel in the name of being honest I'm a crumpled up piece of paper lying here "
            "'Cause I remember it all, all, all Too well Time won't fly, it's like I'm paralyzed by it I'd like to be my old self again "
            "But I'm still trying to find it After plaid shirt days and nights when you made me your own Now you mail back my things and "
            "I walk home alone But you keep my old scarf from that very first week 'Cause it reminds you of innocence And it smells like me "
            "You can't get rid of it 'Cause you remember it all too well, yeah "
            "'Cause there we are again when I loved you so Back before you lost the one real thing you've ever known")
    atwS_inB = bytearray(atwS, "ascii")

    packets = rdpcap("pack3.pcap")  # "reading" pcap file
    c = 0  # for packets counter
    lc = 0  # letter count for string
    listp = []  # list of packets with target
    ntemp = ""  # new temp
    newPackets = []

    lc = 0
    for packet in packets:
        if packet.haslayer(Raw):
            temp = packet["Raw"].load  # bytearray allows the array to be mutable

            ind = temp.find(b'\xff\xff\xff\xff\xff\xff\xff\xff\xff')
            if ind != -1:  # checking that the nine values above do exist in the packet
                endIn = ind
                while temp[endIn] == 255 and endIn < len(temp) - 1:
                    endIn += 1

                strt = ind + 4
                endIn = endIn - 4
                numOfBytesToHide = endIn - ind + 1  # how many bytes i can hide

                if lc >= len(atwS):
                    lc = 0

                ntemp = temp[:strt] + atwS_inB[lc:lc + numOfBytesToHide] + temp[endIn:]
                lc += numOfBytesToHide  # letter counter

                packet["Raw"].load = ntemp
                listp.append(packet)  # finding the packets with nine ff values

        packet = packet[IP]
        del packet[IP].chksum
        del packet[IP].len
        del packet[IP].ihl
        newPackets.append(packet)
        c += 1

    wrpcap('newpackT.pcap', newPackets)  # creating a new file after changing the packets "writing"


if __name__ == "__main__":
    """
    This initiates and calls the main function for this application. 

    Generally, this should be the last bit of code in this script.
    """
    logging.basicConfig(level=logging.DEBUG)
    main()

# load = b"\xaa\xbb\xff\xcc\xee"
# secret_msg = "c" # even though this is one character, it is still a string
# Need to hide "c" where "\xff" is in the load variable
# "\xff" is located at index value 2 (e.g. load[2])
# Use list slicing to concatenate the parts together
# load[2]
# load[:2] # Keeps the first two characters
# b'\xaa\xbb'
# load[len(load)-2:] # Keeps the last two characters
# b'\xcc\xee'
# Convert string into byte array
# secret_char_in_bytes = bytearray(secret_msg, "ascii") # This will return a list of len = 1
# secret_char_in_bytes
# bytearray(b'c')
# secret_char_in_bytes[0]
# Now concatenate it all together
# new_load = load[:2] + secret_char_in_bytes + load[len(load)-2:]
# new_load
# b'\xaa\xbbc\xcc\xee'
# the character "c" is in between \xbb and \xcc --> \xbbc\xcc
