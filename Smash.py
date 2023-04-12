#!/usr/bin/python

import click
from scapy.layers.inet import IP
from scapy.packet import Raw
from scapy.utils import rdpcap, wrpcap
import pyDes

@click.command()
@click.option("--inputpcap", "-i", default='pack3.pcap', help="The pcap file holding the packets from the stream")
@click.option("--outputpcap", "-o", default='output.pcap', help="The outfile name (pcap) where the encoded packets will go")
@click.option("--textmessage", "-t", default=None, help="Text message to be hidden in file")
@click.option("--filemessage", "-f", default=None, help="File message to be hidden in file")
@click.option("--key", "-k", default='SULLIVAN', help="Input an 8 letter word (8 bytes) as the encryption key")

def encrypt (inputpcap, outputpcap, textmessage, filemessage, key):
    inf = inputpcap
    outf = outputpcap
    message_befB = []
    if textmessage == None and filemessage == None:
        message_befB = ("I walked through the door with you The air was cold But something about it felt like home somehow "
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
    elif textmessage != None:
        message_befB = textmessage

    else:
        temporaryLIST = []
        with open(filemessage, 'rb') as f:
            byte = f.read(1)
            while byte != b'':
                temporaryLIST.append(byte)
                byte = f.read(1)
        mes = b''.join(temporaryLIST)


    k = pyDes.des(bytes(key, 'ascii'), pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)

    if filemessage == None:
        mes = bytearray(message_befB.encode('utf-8'))
    mes = k.encrypt(mes)

    return mes, inf, outf

def encode (message, inputpcap, outputpcap):
    packets = rdpcap(inputpcap)  # "reading" pcap file
    c = 0  # for packets counter
    lc = 0  # letter count for string
    newPackets = []

    for packet in packets:
        if packet.haslayer(Raw):
            temp = packet["Raw"].load

            ind = temp.find(b'\xff\xff\xff\xff\xff\xff\xff\xff\xff')
            if ind >= 0:  # checking that the nine values above do exist in the packet
                endIn = ind
                while temp[endIn] == 255 and endIn < len(temp) - 1:
                    endIn += 1

                strt = ind + 4
                endIn = endIn - 4
                numOfBytesToHide = endIn - ind + 1  # how many bytes i can hide

                if lc >= len(message):
                    break

                ntemp = temp[:strt] + message[lc:lc + numOfBytesToHide] + temp[endIn:]
                lc += numOfBytesToHide

                packet["Raw"].load = ntemp

        packet = packet[IP]
        del packet[IP].chksum
        del packet[IP].len
        del packet[IP].ihl
        newPackets.append(packet)
        c += 1

    wrpcap(outputpcap, newPackets)  # creating a new file after changing the packets "writing"


if __name__ == "__main__":
    """
    This initiates and calls the main function for this application.

    Generally, this should be the last bit of code in this script.
    """

    mesE, inputf, outputf = encrypt(standalone_mode=False)  # encrypted message
    encode(mesE, inputf, outputf)