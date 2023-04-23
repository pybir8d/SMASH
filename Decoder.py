from scapy.packet import Raw
from scapy.utils import rdpcap
import click
import pyDes


@click.command()
@click.option("--pcap", "-o", default='output.pcap', help="pcap file with message encoded")
@click.option("--key", "-k", default='SULLIVAN', help="Input an 8 letter word (8 bytes) as the encryption key")
@click.option("--file", "-f", default=None, help="File message to be hidden in file")
def decode(pcap, key, file):
    packets = rdpcap(pcap)  # "reading" pcap file
    message = []
    decrypt_key = key
    is_there_a_file = file

    packet_counter = 0
    length_counter = 0
    length = 200000000000000000

    for packet in packets:
        if packet.haslayer(Raw):
            temp = packet["Raw"].load

            ind = temp.find(b'\xff\xff\xff\xff')
            if ind >= 0:  # checking that the four values above do exist in the packet
                second_temp = temp[ind + 4:]
                end = second_temp.find(b'\xff\xff\xff\xff')  # finding second instance of four 0xFF
                end1 = end + ind + 4

                if end >= 0 and length_counter < length:  # second ff
                    target = temp[ind + 4:end1]  # making a list of only the possible message
                    if packet_counter == 0: # checking within first relevant packet
                        j = 6
                        ind_of_end_len = 0
                        while j > 0:
                            try:
                                length = int(target[0:j]) # trying to find length hidden at beginning
                                ind_of_end_len = j
                                j = 0
                            except:
                                j -= 1
                                continue

                        target = temp[ind + 4 + ind_of_end_len: end1] # taking out length to make sure decryption works later
                    length_counter += len(target)
                    message.append(target)
                    packet_counter += 1
    return message, decrypt_key, is_there_a_file


def decrypt(message, key, file):
    strM = b''.join(message)
    k = pyDes.des(bytes(key, 'ascii'), pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    strM = k.decrypt(strM)

    strMs = str(strM)
    finalS = strMs[2:-1]
    print(finalS)

    if file != None:
        strM = bytes(strM)
        with open(file, 'wb') as pcfile:
            pcfile.write(strM)
        pcfile.close()


if __name__ == "__main__":
    """
    This initiates and calls the main function for this application.

    Generally, this should be the last bit of code in this script.
    """
    mes, key, f = decode(standalone_mode=False)
    decrypt(mes, key, f)
