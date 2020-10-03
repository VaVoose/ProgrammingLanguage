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
    2. Your program must be organized. Your main function must be in a separate file
        ( if name == "__main__:"), the output must be produced from the main function using the next() function.
"""

#/usr/bin/python3

import lexer
import parse
import sys

ERR = -1
BRK = 0
CONT = 1
SUCCESS = 2

"""
Main testing function of the program, controls the logic of the program
"""
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
    par = parse.Parse(lex)

    #Run the Parser. The parser will crash with exit(0) if there is a parsing error and otherwise
    #will return to the main to print a successful parse.
    if (par.program()):
        print("File was Successfully Parsed!!!!\n")

'''
    #Below this is old code
    print("\nRemaining Tokens (Not including current token)")
    
    print("Line #          Value          Token Category")
    print("---------------------------------------------")
    #While their are tokens in the queue obtain and print the next token
    while True:
        token = lex.next()
        if (token == "EOF"): break
        
        print('{:<15} {:15} {:<20}'.format(token[0], token[1], token[2]))
'''

#Runs the main function first
if __name__ == "__main__":
    main()