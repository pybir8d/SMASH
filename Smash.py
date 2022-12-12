#!/usr/bin/python

import getopt
import logging
import sys
import click

@click.command()
@click.option("--test", "-t", default = 1, help = "Test Value")
@click.option("--inFile", "-i", default = 'out.mp4', prompt = "Enter the name of input file", help = "mp4 video file inputted by the user")
@click.option("--outFile", "-o", default = 'output.m3u8', prompt = "Enter the name of export file", help = "Name of the export file")

def testVariable(test):
    #for test variables
    click.echo("I'm doing something 1. This is test variable: " + str(test))

def fileConvert(inFile, outFile):
    #for file conversion
    temp = inFile
    temp2 = outFile
    click.echo("Files: " + inFile + " and " + outFile)

def main():
    """
    This function is the entry point for this application.

    :param argv: List of command line arguments
    """
    # Program Variables

if __name__ == "__main__":
    """
    This initiates and calls the main function for this application. 

    Generally, this should be the last bit of code in this script.
    """
    logging.basicConfig(level=logging.DEBUG)
    #testVariable()
    fileConvert()
