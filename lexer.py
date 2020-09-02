"""
    lexer.py _ Dominic Ferrante - Brian Rexroth - Drew Battison
    Python Lexer Class
    Dr. Al-Haj
    ECCS 4411 - Programming Languages

    This is the lexer class for our programming language implementation
    Requirements:
    1. Be implemented using Python3
    2. Read an input file and output all tokens
        a. Input file name is given as an argument when typing a command line
        b. Proper exception handling to handle wrong file name or if the file does not exists.
    3. Recognize the following tokens:
        a. Keywords: main, int, float, char, if, else, true, false
        b. Terminal Literals: integer numbers, real numbers, true and false. An
            integer number is defined as a sequence of digits (0..9). 
            A real number is defined a sequence of digits followed by a decimal point (.) 
            followed by a sequence of digits (.9 and 9.0.5 are not allowed).
        c. Operators:+-*/!>>=<<=||&&
        d. Punctuations: ; , { } ( )
    4. Single line comments must be removed. Comments begin with //
    5. Remove all whitespaces
    6. Output all tokens in a readable format as follows:
        Line # Value Token Category 
        --------------------------------------------------------
        1   int   keyword
        1   main  keyword
        1   (     left parenthesis
        1   )     right parenthesis
        3   x1    identifier
        3   =     assignment_op
        3   ;     semicolon
        4   2y    unknown
    7. All classes and functions are properly documented including purpose and preconditions.
    8. Have a function named next, (i.e. next() ), that outputs a single token. This function will be used later in the Parser project.
    9. Your program must be organized. Your main function must be in a separate file
        ( if name == "__main__:"), the output must be produced from the main function using the next() function.
"""

#Using python3
#/usr/bin/python3

import re
import sys

class Lexer:

    def __init__(self, f):
        self.f = f
        self.lineNumber = 0

    def printFile(self):
        print(self.f)

    def next(self):
        lineNumber = lineNumber + 1
        curLine = f.readline()
        print(curLine)
        





