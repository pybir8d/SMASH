#!/usr/bin/python

import getopt
import logging
import sys
import click

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


if __name__ == "__main__":
    """
    This initiates and calls the main function for this application. 

    Generally, this should be the last bit of code in this script.
    """
    logging.basicConfig(level=logging.DEBUG)
    main()
