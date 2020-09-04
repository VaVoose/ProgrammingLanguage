"""
    lexer.py _ Dominic Ferrante - Brian Rexroth - Drew Battison
    Python Lexer Class
    Dr. Al-Haj
    ECCS 4411 - Programming Languages

    This is the lexer class for our programming language implementation
    Requirements:
    1. Be implemented using Python3
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
        Line# Value Token Category 
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

KEYWORDS = {
    "main": "keyword",
    "int": "keyword",
    "float": "keyword",
    "char": "keyword",
    "if": "keyword",
    "else": "keyword",
    "true": "keyword",
    "false": "keyword"
}

INTEGERS = "\d+$"
REALNUMS = "\d+\.\d+$"
IDENTIFIER = "\[A-Za-z_]+[A-Za-z_0-9]*"

OPERATORS = {
    "+": "add_op",
    "-": "sub_op",
    "*": "mult_op",
    "/": "div_op",
    "=": "assign_op",
    "!": "not_op",
    ">": "gt_op",
    ">=": "gte_op",
    "<": "lt_op",
    "<=": "lte_op",
    "||": "or_op",
    "&&": "and_op"
}

PUNCTUATIONS = {
    ";": "semicolon",
    ",": "comma",
    "{": "l_curly",
    "}": "r_curly",
    "(": "l_paren",
    ")": "r_paren"
    }

class Lexer:

    """
    Default Lexer Constructor
    param f: the file that was read
    """
    def __init__(self, f):
        self.f = f
        self.lineNumber = 0
        self.tokenQueue = []

    def generateTokens(self):
        for curLine in self.f:
            self.lineNumber = self.lineNumber + 1
            splitWords = re.split('\s', curLine)
            #Lex each word in the line
            for word in splitWords:
                #print(word)
                if (not word):
                    continue
                elif (re.match("//", word)):
                    break
                self.lex(word)


    """
    Returns the next [lineNumber, value, token category] of the file
    """
    def next(self):
        if (self.tokenQueue): 
            return self.tokenQueue.pop(0)

        return "EOF"


    """
    Determines the category of the next token and 
    pushes the next [lineNumber, value, token category] pair to the queue
    param word: the current word being lexed
    """
    def lex(self, word):
        if (word in KEYWORDS):
            self.tokenQueue.append([self.lineNumber, word, KEYWORDS[word]])
        elif(word in OPERATORS):
            self.tokenQueue.append([self.lineNumber, word, OPERATORS[word]])
        elif(word in PUNCTUATIONS):
            self.tokenQueue.append([self.lineNumber, word, PUNCTUATIONS[word]])
        elif(re.match(INTEGERS, word)):
            self.tokenQueue.append([self.lineNumber, word, "integer"])
        elif(re.match(REALNUMS, word)):
            self.tokenQueue.append([self.lineNumber, word, "real"])
        else:
            self.tokenQueue.append([self.lineNumber, word, "unknown"])