"""
    testMain.py _ Dominic Ferrante - Brian Rexroth - Drew Battison
    Python Lexer Class
    Dr. Al-Haj
    ECCS 4411 - Programming Languages

    Main file for testing the lexer and associated functions
"""

#/usr/bin/python3

import lexer
import sys

def main():
    #While invalid file
    while True:
        fName = input("Please enter testing file: ")
        #attempt to open and read
        try:
            with open(fName, 'r') as f:
                readFile = f.read()
            break
        except:
            print("File not found/read")

    #instantiate a lexer and print the file that it has
    lex = lexer.Lexer(readFile)
    lex.next()

#Runs the main function first
if __name__ == "__main__":
    main()


