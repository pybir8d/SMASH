#!/usr/bin/python

import getopt
import logging
import sys

def main(argv):
    """
    This function is the entry point for this application.

    :param argv: List of command line arguments
    """
    # Program Variables

    try:
        # Convert the list of user provided command line arguments into meaningful objects to manipulate.
        # The attributes as the second and third parameters are listed in more detail below.
        opts, args = getopt.getopt(argv, "ht:", ["help", "test="])
    except getopt.GetoptError:
        # Ran into an error while converting the user supplied options. User should check their arguments and rerun the application.
        # Printing application usage and exiting.
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
            print("User enter value for t = " + arg)

def get_usage():
    """
    Prints the applicaiton usage information

    :return: String that describes the application usage.
    """
    usage_text = """
smash.py [opts]

    -t value, --test=<value>:                         Test value
    -h, --help:                                       Diplays usage information.

    """

    return usage_text

if __name__ == "__main__":
    """
    This initiates and calls the main function for this applicaiton. 

    Generally, this should be the last bit of code in this script.
    """
    logging.basicConfig(level=logging.DEBUG)
    main(sys.argv[1:])