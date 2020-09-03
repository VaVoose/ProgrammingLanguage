"""
    testMain.py _ Dominic Ferrante - Brian Rexroth - Drew Battison
    Python Lexer Class
    Dr. Al-Haj
    ECCS 4411 - Programming Languages

    Main file for testing the lexer and associated functions

    Requirements:
    1. Read an input file and output all tokens
        a. Input file name is given as an argument when typing a command line
        b. Proper exception handling to handle wrong file name or if the file does not exists.
"""

#/usr/bin/python3

import lexer
import sys

def main():
    #While invalid file
    while True:
        fileName = input("Please enter testing file: ")
        #attempt to open and read
        try:
            f = open(fileName, 'r')
            break
        except:
            print("File not found/read")

    #instantiate a lexer and print the file that it has
    lex = lexer.Lexer(f)
    print(lex.next())
    print(lex.next())
    print(lex.next())
    print(lex.next())
    

#Runs the main function first
if __name__ == "__main__":
    main()


