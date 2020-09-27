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
import sys

LINENUMBER = 0
VALUE = 1
CATEGORY = 2

ERR = -1
BRK = 0
CONT = 1
SUCCESS = 2

lex = []

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
    global lex
    lex = lexer.Lexer(f)
 
    result = program()
    if (result == SUCCESS):
        print("Finished Parsing Successfully")
    elif(result == ERR):
        print("Something went wrong with parsing, see above line")


    #Below this is old code
    print("Remaining Tokens")
    
    print("Line #          Value          Token Category")
    print("---------------------------------------------")
    #While their are tokens in the queue obtain and print the next token
    while True:
        token = lex.next()
        if (token == "EOF"): break
        
        print('{:<15} {:15} {:<20}'.format(token[0], token[1], token[2]))

def program():
    global lex

    if ((lex.next()[VALUE]) == "int"):
        print("int read")
        if (lex.next()[VALUE] == "main"):
            print("main read")
            if (lex.next()[VALUE] == "("):
                print("( read")
                if (lex.next()[VALUE] == ")"):
                    print(") read")
                    if (lex.next()[VALUE] == "{"):
                        print("{ read")
                        if (declarations() == ERR): 
                            return ERR
                        if (statements() == ERR): 
                            return ERR
                        if (lex.next()[VALUE] == "}"):
                            print("} read")
                            return SUCCESS
                        else:
                            print("Missing end right curly brace in program")
                            return ERR
                    else:
                        print("Missing left curly brace in program")
                        return ERR
                else:
                    print("Missing right paren in program")
                    return ERR
            else:
                print("Missing left paren in program")
                return ERR
        else:
            print("Missing 'main' in program")
            return ERR
    else:
        print("Missing 'int' in program")
        return ERR           

'''
Im not sure how to repeat this correctly
'''
def declarations():
    global lex

    while(True):
        tok = declaration()
        if (tok == ERR): return ERR
        elif (tok == BRK): break

    return CONT

def declaration():
    global lex

    if (Type() == ERR): return ERR
    if (identifier() == ERR): return ERR
    
    tok = lex.next()
    
    #If there is a square bracket -> integer + "]"
    if (tok[VALUE] == "["):
        if (integer() == ERR): return ERR
        if (lex.next()[VALUE] == "]"):
            pass
        else:
            print("Missing ']' in optional integer in declaration")
            return ERR
    else:
        while(True):
            if (tok[VALUE] == ","):
                print(", read")
                if (identifier() == ERR): return ERR
                tok = lex.next()
                
                if (tok[VALUE] == "["):
                    if (integer() == ERR): return ERR
                    if (lex.next()[VALUE] == "]"):
                        print("] read")
                        tok = lex.next()
                    else:
                        print("Missing ']' in optional integer in declaration")
                        return ERR
            else:
                break
    if (tok[VALUE] == ";"):
        print("; read")
        return BRK
    else:
        print("Missing Semicolon in declaration")
        return ERR
    
def Type():
    global lex

    tok = lex.next()[VALUE]
    
    if (tok == "bool" or tok == "int" or tok == "float" or tok == "char"):
        print(tok, " read")
        return CONT
    else:
        print("Invalid type")
        return ERR

'''
This is the only way to do this?
There doesn't need to be a seperate function for "letter" in this case because the lexer already determines that its a identifier?
'''
def identifier():
    global lex

    tok = lex.next()

    if (tok[CATEGORY] == "identifier"):
        print(tok[VALUE], " read")
        return CONT
    else:
        print("Invalid identifier")
        return ERR

'''
Running into a similar situation with integer as I did with letter
'''
def integer():
    global lex

    tok = lex.next()[VALUE]
    if (tok.isdigit()):
        print(tok, " read")
        return CONT
    else:
        print("Invlid Integer")
        return ERR

def letter():
    return CONT

def statements():
    return BRK


#Runs the main function first
if __name__ == "__main__":
    main()