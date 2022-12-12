#!/usr/bin/python

import getopt
import logging
import sys
import click

@click.command()
@click.option("--lowres", "-l", default = 'low.m3u8', help = "Low resolution video in .m3u8")
@click.option("--highres", "-h", default = 'high.m3u8', help = "High resolution video in .m3u8")
@click.option("--message", "-m", default = 'Hello, World',  help = "Message to be hidden in file")

def main(lowres, highres, message):
    #for actual steg process
    click.echo("Files: " + highres + " and " + lowres + ". Message: " + message)


if __name__ == "__main__":
    """
    This initiates and calls the main function for this application. 

    Generally, this should be the last bit of code in this script.
    """
    logging.basicConfig(level=logging.DEBUG)
    main()
