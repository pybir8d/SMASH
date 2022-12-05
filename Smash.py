#!/usr/bin/python

import getopt
import logging
import sys
import click

@click.command()
@click.option("--test", "-t", default = 1, help = "Test Value")

def testVariable(test):
    #for test variables
    test_var = test
    click.echo("I'm doing something 1. This is test variable: " + str(test_var))

def main(argv):
    """
    This function is the entry point for this application.

    :param argv: List of command line arguments
    """
    # Program Variables
    test_var = 0
"""
    ####################################
    ### Command Line Processing
    ####################################
    try:
        # Convert the list of user provided command line arguments into meaningful objects to manipulate.
        # The attributes as the second and third parameters are listed in more detail below.
        opts, args = getopt.getopt(argv, "ht:t2:", ["help", "test=", "test2="])
    except getopt.GetoptError:
        # Ran into an error while converting the user supplied options. User should check their arguments and rerun the application.
        # Printing application usage and exiting.
        logging.warning("Did not use offered parameters")
        print(get_usage())
        sys.exit(2)

    # Stepping through each user supplied argument.
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            # User asked to print the help menu.
            # Exit after printing help.
            print(get_usage())
            sys.exit()
        elif opt in ("-t", "--test"):
            # Using user provided audio file.
            test_var = arg

    ####################################
    ### Main Code Section
    ####################################

    # Do something 1
    print("I'm doing something 1.")
    logging.info(" Doing something.")

    # Do something 2
    print("I'm doing something 2.")

    print("Oh by the way, test var is: " + str(test_var))


def get_usage():
    ""
    Prints the application usage information

    :return: String that describes the application usage.
    ""
    usage_text = ""
smash.py [opts]

    -t value, --test=<value>:                         Test value
    -h, --help:                                       Displays usage information.

    ""

    return usage_text"""

if __name__ == "__main__":
    """
    This initiates and calls the main function for this application. 

    Generally, this should be the last bit of code in this script.
    """
    logging.basicConfig(level=logging.DEBUG)
    #main(sys.argv[1:])
    testVariable()
