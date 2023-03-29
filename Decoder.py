from scapy.packet import Raw
from scapy.utils import rdpcap
import click
import pyDes

@click.command()
@click.option("--pcap", "-i", default='output.pcap', help="pcap file with message encoded")
@click.option("--key", "-k", default='SULLIVAN', help="Input an 8 letter word (8 bytes) as the encryption key")

def decode(pcap, key):
    packets = rdpcap(pcap)  # "reading" pcap file
    message = []
    decrypt_key = key

    for packet in packets:
        if packet.haslayer(Raw):
            temp = packet["Raw"].load

            ind = temp.find(b'\xff\xff\xff\xff')
            if ind >= 0:  # checking that the four values above do exist in the packet
                second_temp = temp[ind + 4:]
                end = second_temp.find(b'\xff\xff\xff\xff')  # finding second instance of four 0xFF
                end1 = end + ind + 4

                if end >= 0:  # second ff
                    target = temp[ind + 4:end1]  # making a list of only the possible message
                    message.append(target)
    return message, decrypt_key


def decrypt(message, key):
    strM = b''.join(message)
    k = pyDes.des(bytes(key, 'ascii'), pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    strM = k.decrypt(strM)
    print(strM)


if __name__ == "__main__":
    """
    This initiates and calls the main function for this application.

    Generally, this should be the last bit of code in this script.
    """
    mes, key = decode(standalone_mode=False)
    decrypt(mes, key)
