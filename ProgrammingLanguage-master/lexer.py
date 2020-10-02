"""
    lexer.py _ Dominic Ferrante - Brian Rexroth - Drew Battison
    Python Lexer Class
    Dr. Al-Haj
    ECCS 4411 - Programming Languages

    This is the lexer class for our programming language implementation
    Requirements:
    1. Be implemented using Python3
    2. Recognize the following tokens:
        a. Keywords: main, int, float, char, if, else, true, false
        b. Terminal Literals: integer numbers, real numbers, true and false. An
            integer number is defined as a sequence of digits (0..9). 
            A real number is defined a sequence of digits followed by a decimal point (.) 
            followed by a sequence of digits (.9 and 9.0.5 are not allowed).
        c. Operators:+-*/!>>=<<=||&&
        d. Punctuations: ; , { } ( )
    3. Single line comments must be removed. Comments begin with //
    4. Remove all whitespaces
    5. Output all tokens in a readable format as follows:
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
    6. All classes and functions are properly documented including purpose and preconditions.
    7. Have a function named next, (i.e. next() ), that outputs a single token. This function will be used later in the Parser project.
"""

#Using python3
#/usr/bin/python3

import re
import sys

#Keyword dictionary
KEYWORDS = {
    "main": "keyword",
    "int": "keyword",
    "float": "keyword",
    "char": "keyword",
    "if": "keyword",
    "else": "keyword",
    "true": "keyword",
    "false": "keyword",
    "bool": "keyword",
    "while": "keyword"
}

#Operator dictionary
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

#Punctuation dictionary
PUNCTUATIONS = {
    ";": "semicolon",
    ",": "comma",
    "{": "l_curly",
    "}": "r_curly",
    "(": "l_paren",
    ")": "r_paren"
    }

#RegEx expressions for integers real numbers and identifiers
INTEGERS = r"\d+$"
REALNUMS = r"\d+\.\d+$"
IDENTIFIER = r"[A-Za-z_]+[A-Za-z_0-9]*"

class Lexer:

    """
    Default Lexer Constructor
    param f: the file that was read
    """
    def __init__(self, f):
        self.f = f
        self.lineNumber = 0
        self.tokenQueue = []
        self.generateTokens()

    """
    Generates all tokens from a passed in file
    """
    def generateTokens(self):
        comment = 0
        for curLine in self.f:
            self.lineNumber = self.lineNumber + 1
            splitWords = re.split(r'\s|([\[\]:;,(){}]|//|\*/|/\*|==|!=|<=|>=|\+=|-=|\*=|/=|&&|\|\||=|>|<|\*|/|\+\+|--|%|\+|-|!)', curLine)
            #Lex each word in the line
            for word in splitWords:
                #print(word)
                if (not word):
                    continue
                #Do not tokenize words within comments
                elif (re.match("//", word)):
                    break
                elif (re.match(r"/\*", word)):
                    comment = 1
                    continue
                elif (re.match(r"\*/", word)):
                    comment = 0
                    continue
                if (comment == 0):
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
        elif(re.match(IDENTIFIER, word)):
            self.tokenQueue.append([self.lineNumber, word, "identifier"])
        else:
            self.tokenQueue.append([self.lineNumber, word, "unknown"])