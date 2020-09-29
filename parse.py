"""
    lexer.py _ Dominic Ferrante - Brian Rexroth - Drew Battison
    Python Lexer Class
    Dr. Al-Haj
    ECCS 4411 - Programming Languages
"""

LINENUMBER = 0
VALUE = 1
CATEGORY = 2

#There was an error reading the token
ERR = -1
#Break out from the previous called function
BRK = 0
#Continue on in the previous called function
CONT = 1
#A successful parse with no errors
SUCCESS = 2

class Parse:

    def __init__(self, lexer):
        self.lex = lexer
        self.token = ""

    '''
    Returns ERR if there was an error,
    if an error occurs within the scope it prints what went wrong
    Returns SUCCESS if it completed parsing without errors
    '''
    def program(self):
        self.token = self.lex.next()
        if (self.token[VALUE] == "int"):
            print("int read")
            self.token = self.lex.next()
            if (self.token[VALUE] == "main"):
                print("main read")
                self.token = self.lex.next()
                if (self.token[VALUE] == "("):
                    print("( read")
                    self.token = self.lex.next()
                    if (self.token[VALUE] == ")"):
                        print(") read")
                        self.token = self.lex.next()
                        if (self.token[VALUE] == "{"):
                            print("{ read")
                            self.token  = self.lex.next()
                            if (self.declarations() == ERR): 
                                return ERR
                            if (self.statements() == ERR): 
                                return ERR
                            if (self.token[VALUE] == "}"):
                                print("} read")
                                return SUCCESS
                            else:
                                print("Missing end right curly brace in program at line ", self.token[LINENUMBER])
                                return ERR
                        else:
                            print("Missing left curly brace in program at line ", self.token[LINENUMBER])
                            return ERR
                    else:
                        print("Missing right paren in program at line ", self.token[LINENUMBER])
                        return ERR
                else:
                    print("Missing left paren in program at line ", self.token[LINENUMBER])
                    return ERR
            else:
                print("Missing 'main' in program at line ", self.token[LINENUMBER])
                return ERR
        else:
            print("Missing 'int' in program at line ", self.token[LINENUMBER])
            return ERR
    
    '''
    Im not sure how to repeat this correctly

    Infinite loops until the declaration function returns BRK which breaks from the infinite loop <- this probably doesn't work for final implementation

    Returns ERR if there was an error in declaration
    Returns CONT if there are no more declarations
    '''
    def declarations(self):

        while(True):
            result = self.declaration()
            if (result == ERR): return ERR
            elif (result == BRK): break

        return CONT
    
    '''
    Returns ERR if there was an error,
    if the error is in scope it prints the error
    Returns BRK if there are no more declarations
    Returns CONT if there are more declarations
    '''
    def declaration(self):
        #If type is error, return ERR
        #If the token is not a type, we are done with declarations so return BRK
        t = self.Type()
        if (t == ERR): return ERR
        if (t == BRK): return BRK

        if (self.identifier() == ERR): return ERR
        
        #If there is a square bracket -> integer + "]"
        if (self.token[VALUE] == "["):
            print("[ read")
            self.token = self.lex.next()
            if (self.integer() == ERR): return ERR
            if (self.token[VALUE] == "]"):
                print("] read")
                self.token = self.lex.next()
                pass
            else:
                print("Missing ']' in optional integer in declaration at line ", self.token[LINENUMBER])
                return ERR
        #If not check for a comma
        #else:
        while(True):
            if (self.token[VALUE] == ","):
                print(", read")
                self.token = self.lex.next()
                if (self.identifier() == ERR): return ERR                  
                if (self.token[VALUE] == "["):
                    print("[ read")
                    self.token = self.lex.next()
                    if (self.integer() == ERR): return ERR
                    if (self.token[VALUE] == "]"):
                        print("] read")
                        self.token = self.lex.next()
                    else:
                        print("Missing ']' in optional integer in declaration at line ", self.token[LINENUMBER])
                        return ERR
                else:
                    #print("Missing '[' in optional integer in declration at line ", self.token[LINENUMBER])
                    continue
            else:
                break
        if (self.token[VALUE] == ";"):
            print("; read")
            self.token = self.lex.next()
            return CONT
        else:
            print("Missing Semicolon in declaration at line ", self.token[LINENUMBER])
            return ERR

    '''
    Returns CONT if there was a successful read
    Returns ERR if there was an error
    '''
    def Type(self):
        
        if (self.token[VALUE] == "bool" or self.token[VALUE] == "int" or self.token[VALUE] == "float" or self.token[VALUE] == "char"):
            print(self.token[VALUE], " read")
            self.token  = self.lex.next()
            return CONT
        else:
            print("Invalid type at line ", self.token[LINENUMBER], " - moving into statements")
            return BRK

    '''
    There doesn't need to be a seperate function for "letter" in this case because the lexer already determines that its a identifier?

    Returns CONT if successfull read
    Returns ERR if there was an error
    '''
    def identifier(self):

        #Check token category if it has been determined to be an identifier
        if (self.token[CATEGORY] == "identifier"):
            print(self.token[VALUE], " read")
            self.token = self.lex.next()
            return CONT
        else:
            print("Invalid identifier at line ", self.token[LINENUMBER])
            return ERR

    '''
    Running into a similar situation with integer as I did with letter

    Returns CONT on successful read
    Returns ERR if there was an error
    '''
    def integer(self):

        #Checks to see if the token is a digit
        if (self.token[VALUE].isdigit()):
            print(self.token[VALUE], " read")
            self.token = self.lex.next()
            return CONT
        else:
            print("Invlid Integer at line ", self.token[LINENUMBER])
            return ERR

    def boolean(self):
        if (self.token[VALUE] == "true" or self.token[VALUE] == "false"):
            print(self.token[VALUE], " read")
            self.token = self.lex.next()
            return CONT
        else:
            print("reading boolean failed")
            return ERR

    def Float(self):
        if (self.integer() == ERR): return ERR
        if (self.token[VALUE] == "."):
            print(". read")
            self.token = self.lex.next()
            if (self.integer() == ERR): return ERR
        else:
            print("missing . in float at line ", self.token[VALUE])
            return ERR
        return CONT

    def char(self):
        if (self.token[VALUE].isascii() and len(self.token[VALUE]) == 1): return CONT
        else:
            print("ASCII character not found at line ", self.token[LINENUMBER])
            return ERR

    '''
    Returns ERR if there was an error
    Returns CONT if there was no errors
    '''
    def statements(self):
        while(True):
            result = self.statement()
            if (result == ERR): return ERR
            elif (result == BRK): break

        return CONT

    def statement(self):
        #Test to see if the token is a ;
        if (self.token[VALUE] == ";"):
            print("; read in statement")
            self.token = self.lex.next()
            return CONT
        #Test for block
        result = self.block()
        if (result == ERR): return ERR
        elif (result == CONT): return CONT
        #elif (result == CONT): pass
        #test for Assignment
        result = self.assignment()
        #if (result == ERR): return ERR
        if (result == CONT): return CONT
        #test for IfStatement
        result = self.ifStatement()
        if (result == ERR): return ERR
        if (result == CONT): return CONT
        #test for WhileStatement
        result = self.whileStatement()
        if (result == ERR): return ERR
        if (result == CONT): return CONT
        #If its none of the above return BRK
        return BRK

    '''
    Returns CONT if the block was fully read 
    Returns ERR if there was an error reading the statements or the right curly was not found
    Returns BRK if the first token is not a curly brace (aka its not a block -> move on)
    '''
    def block(self):
        if (self.token[VALUE] == "{"):
            print("{ read inside block")
            self.token = self.lex.next()
            if (self.statements() == ERR): return ERR
            if (self.token[VALUE] == "}"):
                print('} read - inside block')
                self.token = self.lex.next()
                return CONT
            else:
                print("'}' missing in block at line ", self.token[LINENUMBER])
                return ERR
        else:
            print("not a block")
            return BRK

    '''

    '''
    def assignment(self):
        if (self.identifier() == ERR): return ERR
        if (self.token[VALUE] == "["):
            print("[ read")
            self.token = self.lex.next()
            if (self.expression() == ERR): return ERR
            if (self.token[VALUE] == "]"):
                print("] read")
                self.token = self.lex.next()
            else:
                print("] mising in assignment in line ", self.token[LINENUMBER])
                return ERR
        if (self.token[VALUE] == "="):
            print("= read")
            self.token = self.lex.next()
            if (self.expression() == ERR): return ERR
        else:
            print("= missing from assignment in line ", self.token[LINENUMBER])
            return ERR
        return BRK

    def expression(self):
        if (self.conjunction() == ERR): return ERR
        while (True):
            if (self.token[VALUE] == "|"):
                print("| read")
                self.token = self.lex.next()
                if (self.token[VALUE] == "|"):
                    print("| read")
                    self.token = self.lex.next()
                    if (self.conjunction() == ERR): return ERR
                else:
                    print("second | in expression missing in line ", self.token[LINENUMBER])
                    return ERR
            else:
                break
        return BRK

    def conjunction(self):
        if (self.equality() == ERR): return ERR
        while (True):
            if (self.token[VALUE] == "&"):
                print("& read")
                self.token = self.lex.next()
                if (self.token[VALUE] == "&"):
                    print("& read")
                    self.token = self.lex.next()
                    if (self.equality() == ERR): return ERR
                else:
                    print("second & in conjunction missing in line ", self.token[LINENUMBER])
                    return ERR
            else:
                break

        return BRK 

    def equality(self):
        if (self.relation() == ERR): return ERR
        if (self.equOp() == CONT):
            if (self.relation() == ERR): return ERR
        return BRK
        
    def relation(self):
        if (self.addition() == ERR): return ERR
        if (self.relOp() == CONT):
            if (self.addition() == ERR): return ERR
        return BRK

    def addition(self):
        if (self.term() == ERR): return ERR
        while (True):
            if (self.addOp() == ERR): break
            if (self.term() == ERR): return ERR

        return BRK

    def term(self):
        if (self.factor() == ERR): return ERR
        while (True):
            if (self.mulOp() == ERR): break
            if (self.factor() == ERR): return ERR
        return BRK

    def factor(self):
        if (self.unaryOp() == ERR): pass
        if (self.primary() == ERR): return ERR
        return BRK

    def unaryOp(self):
        if (self.token[VALUE] == "-" or self.token[VALUE] == "!"):
            print(self.token[VALUE], " read")
            self.token = self.lex.next()
            return CONT
        else:
            print("unary operator expected at line ", self.token[LINENUMBER])
            return ERR

    def primary(self):
        if (self.identifier() == CONT):
            if (self.token[VALUE] == "["):
                print("[ read")
                self.token = self.lex.next()
                if (self.expression() == ERR): return ERR
                if (self.token[VALUE] == "]"):
                    print("] read")
                    self.token = self.lex.next()
                    return CONT
                else:
                    print("] mising in assignment in line ", self.token[LINENUMBER])
                    return ERR
        elif(self.literal() == CONT): return CONT
        elif(self.token[VALUE] == "("):
            print("( read in primary")
            self.token = self.lex.next()
            if (self.expression() == ERR): return ERR
            if (self.token[VALUE] == ")"):
                print(") read in primary")
                self.token = self.lex.next()
                return CONT
            else:
                print(") missing from primary at line ", self.token[LINENUMBER])
                return ERR
        elif(self.Type() == CONT):
            if(self.token[VALUE] == "("):
                print("( read in primary")
                self.token = self.lex.next()
                if (self.expression() == ERR): return ERR
                if (self.token[VALUE] == ")"):
                    print(") read in primary")
                    self.token = self.lex.next()
                    return CONT
                else:
                    print(") missing from primary at line ", self.token[LINENUMBER])
                    return ERR
            else:
                print("( missing from primary at line ", self.token[LINENUMBER])
                return ERR
        #no option in primary was found
        else:
            print("primry expression failed, line ", self.token[LINENUMBER])
            return ERR

    def literal(self):
        if (self.integer() == CONT): return CONT
        elif (self.boolean() == CONT): return CONT
        elif (self.Float() == CONT): return CONT
        elif (self.char() == CONT): return CONT
        else:
            print("missing literal at line ", self.token[LINENUMBER])
            return ERR

    def mulOp(self):
        if (self.token[VALUE] == "*" or self.token[VALUE] == "/" or self.token[VALUE] == "%"):
            print(self.token[VALUE], " read")
            self.token = self.lex.next()
            return CONT
        else:
            print("multiplication operator expected at line ", self.token[LINENUMBER])
            return ERR

    def addOp(self):
        if (self.token[VALUE] == "+" or self.token[VALUE] == "-"):
            print(self.token[VALUE], " read")
            self.token = self.lex.next()
            return CONT
        else:
            print("addition operator expected at line ", self.token[LINENUMBER])
            return ERR

    def relOp(self):
        if (self.token[VALUE] == "<" or self.token[VALUE] == "<=" or self.token[VALUE] == ">" or self.token[VALUE] == ">="):
            print(self.token[VALUE], " read")
            self.token = self.lex.next()
            return CONT
        else:
            print("relative operator expected at line ", self.token[LINENUMBER])
            return ERR

    def equOp(self):
        if (self.token[VALUE] == "==" or self.token[VALUE] == "!="):
            print(self.token[VALUE], " read")
            self.token = self.lex.next()
            return CONT
        else:
            print("equallity operator expected at line ", self.token[LINENUMBER])
            return ERR

    def ifStatement(self):
        if (self.token[VALUE] == "if"):
            print("if read")
            self.token = self.lex.next()
            if (self.token[VALUE] == "("):
                print("( read")
                self.token = self.lex.next()
                if (self.expression() == ERR): return ERR
                if (self.token[VALUE] == ")"):
                    print(") read")
                    self.token = self.lex.next()
                    if (self.statement() == ERR): return ERR
                    if (self.token[VALUE] == "else"):
                        print("else read")
                        self.token = self.lex.next()
                        if (self.statement() == ERR): return ERR
                else:
                    print("missing ')' in if statement at line ", self.token[LINENUMBER])
            else:
                print("missing '(' in if statement at line ", self.token[LINENUMBER])
                return ERR
        else:
            print("'if' missing in if statement at line ", self.token[LINENUMBER])
            return BRK
        return CONT

    def whileStatement(self):
        if (self.token[VALUE] == "while"):
            print("while read")
            self.token = self.lex.next()
            if (self.token[VALUE] == "("):
                print("( read")
                self.token = self.lex.next()
                if (self.expression() == ERR): return ERR
                if (self.token[VALUE] == ")"):
                    print(") read")
                    self.token = self.lex.next()
                    if (self.statement() == ERR): return ERR
                else:
                    print("missing ')' in while statement at line ", self.token[LINENUMBER])
            else:
                print("missing '(' in while statement at line ", self.token[LINENUMBER])
                return ERR
        else:
            print("'while' missing in while statement at line ", self.token[LINENUMBER])
            return BRK
        return CONT

    '''
    Not Currenlty used
    '''
    def letter(self):
        return CONT

    '''
    Not Currently used
    '''
    def digit(self):
        return CONT