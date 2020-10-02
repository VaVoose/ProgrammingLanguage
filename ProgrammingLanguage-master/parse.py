"""
    Parse.py _ Dominic Ferrante - Brian Rexroth - Drew Battison
    Python Parser Class
    Dr. Al-Haj
    ECCS 4411 - Programming Languages
"""
import sys

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
        self.QUIT = False
        print("")

    '''
    Returns ERR if there was an error,
    if an error occurs within the scope it prints what went wrong
    Returns SUCCESS if it completed parsing without errors
    '''
    #A Program should always begin with int main() {<Declarations> <Statements>}
    def program(self):
        self.token = self.lex.next()

        #Format of the first program statement should always be int main() {.....}
        if (self.token[VALUE] == "int" and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Program")
            self.token = self.lex.next()

            if (self.token[VALUE] == "main" and self.QUIT == False):
                print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Program")
                self.token = self.lex.next()

                if (self.token[VALUE] == "(" and self.QUIT == False):
                    print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Program")
                    self.token = self.lex.next()
                    
                    if (self.token[VALUE] == ")" and self.QUIT == False):
                        print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Program")
                        self.token = self.lex.next()
                        
                        if (self.token[VALUE] == "{" and self.QUIT == False):
                            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Program")
                            self.token = self.lex.next()
                            
                            #Get delarations
                            result = self.declarations()
                            if (result == ERR):
                                return ERR
                            elif (result == BRK):
                                return BRK

                            #Get statements
                            result = self.statements()
                            if (result == ERR):
                                return ERR
                            elif (result == BRK):
                                return BRK

                            #Program Ends successfully
                            if (self.token[VALUE] == "}" and self.QUIT == False):
                                print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Program")
                                print("File was successfully parsed!!!!")
                                return SUCCESS
                            else:
                                if (self.QUIT == True):
                                    return ERR
                                if (self.token == "EOF"):
                                    print("Parsing failed - read:", "NULL", "but expected '}' to end program at line ", "EOF")
                                else: print("Parsing failed - read:", self.token[VALUE], "but expected '}' to end program at line ", self.token[LINENUMBER])
                                self.QUIT = True
                                return ERR
                        else:
                            if (self.QUIT == True):
                                return ERR
                            if (self.token == "EOF"):
                                print("Parsing failed - read:", "NULL", "but expected '{' in program at line ", "EOF")
                            else: print("Parsing failed - read:", self.token[VALUE], "but expected '{' in program at line ", self.token[LINENUMBER])
                            self.QUIT = True
                            return ERR
                    else:
                        if (self.QUIT == True):
                            return ERR
                        if (self.token == "EOF"):
                             print("Parsing failed - read:", "NULL", "but expected ')' in program at line ", "EOF")
                        else: print("Parsing failed - read:", self.token[VALUE], "but expected ')' in program at line ", self.token[LINENUMBER])
                        self.QUIT = True
                        return ERR
                else:
                    if (self.QUIT == True):
                        return ERR
                    if (self.token == "EOF"):
                        print("Parsing failed - read:", "NULL", "but expected '(' in program at line ", "EOF")
                    else: print("Parsing failed - read:", self.token[VALUE], "but expected '(' in program at line ", self.token[LINENUMBER])
                    self.QUIT = True
                    return ERR
            else:
                if (self.QUIT == True):
                    return ERR
                if (self.token == "EOF"):
                    print("Parsing failed - read:", "NULL", "but expected 'main' in program at line ", "EOF")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected 'main' in program at line ", self.token[LINENUMBER])
                self.QUIT = True
                return ERR
        else:
            if (self.QUIT == True):
                return ERR
            if (self.token == "EOF"):
                print("Parsing failed - read:", "NULL", "but expected 'int' in program at line ", "EOF")
            else: print("Parsing failed - read:", self.token[VALUE], "but expected 'int' in program at line ", self.token[LINENUMBER])
            self.QUIT = True
            return ERR

    #<declarations> --> <declaration>
    #                   ^^^^ Repeatable
    def declarations(self):
        while(True):
            result = self.declaration()
            if (self.QUIT == True):
                return ERR
            if (result == ERR):
                return ERR            
            elif (result == BRK):
                self.declaration()
                break
        return CONT

    #<declaration> --> <Type> <Identifier>   [<Integer>]     , <Identifier>    [<integer>]     ;
    #                                        ^^^Optional    ^^^^^^Repeatable  ^^Optional       ^^^needed
    def declaration(self):

        #A declaration must begin with a type 
        #If a type does not exist, then the statement is not a declaration!
        if (self.Type() == ERR): 
            return BRK

        #A declaration must also have an identifier
        if (self.identifier() == ERR): 
            if (self.QUIT == True):
                return ERR
            if (self.token == "EOF"):
                print("Parsing failed - read:", "NULL", "but expected an identifier for declaration at line ", "EOF")
            else: print("Parsing failed - read:", self.token[VALUE], "but expected an identifer for delcaration at line", self.token[LINENUMBER])
            self.QUIT = True
            return ERR

        #The identifer can also have an optional array location
        if (self.token[VALUE] == "[" and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Declaration")
            self.token = self.lex.next()

            #After [ was read, there must be an integer for the array location
            if (self.integer() == ERR): 
                if (self.QUIT == True):
                    return ERR
                if (self.token == "EOF"):
                    print("Parsing failed - read:", "NULL", "but expected an an integer for the array location of identifier during declaration at line ", "EOF")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected an integer for the array location of identifier during declaration at line", self.token[LINENUMBER])
                self.QUIT = True
                return ERR

            #The array must have ] as a closing bracket
            if (self.token[VALUE] == "]" and self.QUIT == False):
                print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Declaration")
                self.token = self.lex.next()
            else:
                if (self.QUIT == True):
                    return ERR
                if (self.token == "EOF"):
                    print("Parsing failed - read:", "NULL", "but expected ']' to close identifier's array location during declaration at line ", "EOF")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected ']' to close identifier's array location during declaration at line ", self.token[LINENUMBER])
                self.QUIT = True
                return ERR

        #Possibly adding more identifiers
        while(True):

            #Look for optional comma for additional identifiers
            if (self.token[VALUE] == "," and self.QUIT == False):
                print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Declaration")
                self.token = self.lex.next()

                #Adding additional identifier if a comma was read
                if (self.identifier() == ERR): 
                    if (self.QUIT == True):
                        return ERR
                    if (self.token == "EOF"):
                        print("Parsing failed - read:", "NULL", "but expected an additional identifier during declaration after comma at line ", "EOF")
                    else: print("Parsing failed - read:", self.token[VALUE], "but expected an additonal identifier during declaration after comma at line", self.token[LINENUMBER])
                    self.QUIT = True
                    return ERR   

                #Checking to see if the identifier has an array location     
                if (self.token[VALUE] == "[" and self.QUIT == False):
                    print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Declaration")
                    self.token = self.lex.next()

                    #After [ was read, there must be an integer for the array location
                    if (self.integer() == ERR): 
                        if (self.QUIT == True):
                            return ERR
                        if (self.token == "EOF"):
                            print("Parsing failed - read:", "NULL", "but expected an integer for the array location of additional identifier during declaration at line ", "EOF")
                        else: print("Parsing failed - read:", self.token[VALUE], "but expected an integer for the array location of additonal identifier during declaration at line", self.token[LINENUMBER])
                        self.QUIT = True
                        return ERR

                    #The array must have ] as a closing bracket
                    if (self.token[VALUE] == "]" and self.QUIT == False):
                        print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Declaration")
                        self.token = self.lex.next()
                    else:
                        if (self.QUIT == True):
                            return ERR
                        if (self.token == "EOF"):
                            print("Parsing failed - read:", "NULL", "but expected ']' to close additional identifier's array location during declaration at line ", "EOF")
                        else: print("Parsing failed - read:", self.token[VALUE], "but expected ']' to close additional identifier's array location during declaration at line ", self.token[LINENUMBER])
                        self.QUIT = True
                        return ERR    
                else:
                    #Look for more identifiers
                    continue
            else:
                #Stop looking for identifers and look for declaration end
                break

        #Look for semicolon to end declaration
        if (self.token[VALUE] == ";" and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Declaration")
            self.token = self.lex.next()
            return CONT
        else:
            if (self.QUIT == True):
                return ERR
            if (self.token == "EOF"):
                print("Parsing failed - read:", "NULL", "but expected ';' to end declaration at line ", "EOF")
            else: print("Parsing failed - read:", self.token[VALUE], "but expected ';'' to end declaration at line ", self.token[LINENUMBER])
            self.QUIT = True
            return ERR

    #<Type> --> int | bool | float | char
    #           ^^^^^^^^^^ one of the above
    def Type(self):
        if (self.QUIT == True):
            return ERR
        result = self.token[VALUE]
        if (result == "bool" or result == "int" or result == "float" or result == "char"):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Type")
            self.token = self.lex.next()
            return CONT
        else:
            return ERR

    #<statements> --> <statement>
    #                ^^^^Repeatable
    def statements(self):
        while(True):
            result = self.statement()
            if (self.QUIT == True):
                return ERR
            if (result == ERR): 
                return ERR
            elif (result == BRK):
                self.statement()
                break
        return CONT
    
    #<statement> --> ; | <block> | <assignment> | <iftstatement> | <whilestatement>
    #               ^^^^One of the above
    def statement(self):
        #Go through the possible options for statement
        if (self.token[VALUE] == ";" and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Statement")
            self.token = self.lex.next()
            return CONT
        else:
            if (self.block() == CONT):
                return CONT
            else:
                if (self.assignment() == CONT):
                    return CONT
                else:
                    if (self.ifStatement() == CONT):
                        return CONT
                    else:
                        result = self.whileStatement()
                        if (result == CONT):
                            return CONT
                        else:
                            return BRK
        return CONT

    #<block> --> { <Statements> }
    def block(self):
        #Check to see if the statement is a block. A block begins with {
        if (self.token[VALUE] == "{" and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Block")
            self.token = self.lex.next()

            #Get statements to place within block
            result = self.statements()
            if (result == ERR): 
                return ERR
            elif (result == BRK): 
                return BRK

            #Get closing bracket of block
            if (self.token[VALUE] == "}" and self.QUIT == False):
                print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Block")
                self.token = self.lex.next()
                return CONT
            else:
                if (self.QUIT == True):
                    return ERR
                if (self.token == "EOF"):
                    print("Parsing failed - read:", "NULL", "but expected '}' to close the block at line ", "EOF")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected '}' to close the block at line ", self.token[LINENUMBER])
                self.QUIT = True
                return ERR
        else:
            #Not a block
            return BRK

    #<Assignment> --> <Identifier>[<expression>] = <expression>
    #                               ^^^ optional [expression]
    def assignment(self):
        #readin an identifier, if no identifier is found then this is not an assignment
        result = self.identifier()
        if (result == ERR): 
            return ERR
        elif (result == BRK): 
            return BRK

        #Look for possible [ for expression
        if (self.token[VALUE] == "[" and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Assignment")
            self.token = self.lex.next()

            #Fining expressions
            if (self.expression() == ERR): 
                return ERR

            #Closing ] to end 
            if (self.token[VALUE] == "]" and self.QUIT == False):
                print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Assignment")
                self.token = self.lex.next()
            else:
                if (self.QUIT == True):
                    return ERR
                if (self.token == "EOF"):
                    print("Parsing failed - read:", "NULL", "but expected ']' for assignment in line ", "EOF")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected ']' for assignment in line ", self.token[LINENUMBER])
                self.QUIT = True
                return ERR

        #Need to continue assignment with =
        if (self.token[VALUE] == "=" and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Assignment")
            self.token = self.lex.next()

            if (self.expression() == ERR): 
                return ERR

        else:
            if (self.QUIT == True):
                return ERR
            if (self.token == "EOF"):
                print("Parsing failed - read:", "NULL", "but expected '=' for assignmnet in line ", "EOF")
            else: print("Parsing failed - read:", self.token[VALUE], "but expected '=' from assignment in line ", self.token[LINENUMBER])
            self.QUIT = True
            return ERR
        return CONT

    #<ifStatement> --> if( <expression> ) <statement>    else <statement>
    #                                                  ^^^^^^^ Optional additions    
    def ifStatement(self):

        #If the statement does not begin with 'if', it is not an ifstatement
        if (self.token[VALUE] == "if" and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- ifStatement")
            self.token = self.lex.next()
        else:
            return BRK

        #If an if statement, there needs to be '(' to look for expressions
        if (self.token[VALUE] == "(" and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- ifStatement")
            self.token = self.lex.next()
        else: 
            if (self.QUIT == True):
                return ERR
            if (self.token == "EOF"):
                print("Parsing failed - read:", "NULL", "but expected '(' in ifstatement at line ", "EOF")
            else: print("Parsing failed - read:", self.token[VALUE], "but expected '(' in ifstatement at line ", self.token[LINENUMBER])
            self.QUIT = True
            return ERR

        #Look for expressions within parenthesis
        if (self.expression() == ERR): 
            return ERR

        #Looking for closing parenthesis
        if (self.token[VALUE] == ")" and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- ifStatement")
            self.token = self.lex.next()
        else:
            if (self.QUIT == True):
                return ERR
            if (self.token == "EOF"):
                print("Parsing failed - read:", "NULL", "but expected ')' in ifstatemen at line ", "EOF")
            else: print("Parsing failed - read:", self.token[VALUE], "but expected ')' in ifstatement at line ", self.token[LINENUMBER])
            self.QUIT = True
            return ERR

        #Looking for closing statement to end ifstatement
        if (self.statement() == ERR): 
            return ERR
                    
        #Look for possible else statement for additional ifstatements
        if (self.token[VALUE] == "else" and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- ifStatement")
            self.token = self.lex.next()
        else:
            return BRK

        #Look for statement
        if (self.statement() == ERR): 
            return ERR
        return CONT

    #<whileStatement> --> while( <expression> ) <Statement>
    def whileStatement(self):

        #If the statement does not begin with 'while', it is not a whilestatement
        if (self.token[VALUE] == "while" and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- whileStatement")
            self.token = self.lex.next()
        else:
            return BRK

        #If while statement, you need to begin with '('
        if (self.token[VALUE] == "(" and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- whileStatement")
            self.token = self.lex.next()
        else:
            if (self.QUIT == True):
                return ERR
            if (self.token == "EOF"):
                print("Parsing failed - read:", "NULL", "but expected '(' tin whilestatement at line ", "EOF")
            else: print("Parsing failed - read:", self.token[VALUE], "but expected'(' in whilestatement at line ", self.token[LINENUMBER])
            self.QUIT = True
            return ERR

        #Looking for expression between parenthesis for whilestatement
        if (self.expression() == ERR): 
            return ERR

        if (self.token[VALUE] == ")" and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- whileStatement")
            self.token = self.lex.next()
        else:
            if (self.QUIT == True):
                return ERR
            if (self.token == "EOF"):
                print("Parsing failed - read:", "NULL", "but expected ')' in whilestatement at line ", "EOF")
            else: print("Parsing failed - read:", self.token[VALUE], "but expected ')' in whilestatement at line ", self.token[LINENUMBER])
            self.QUIT = True
            return ERR

        #Look for statement
        if (self.statement() == ERR): 
            return ERR

        return CONT

    #<expression> --> <Conjunction>    || <Conjunction>
    #                                ^^^^^Repeatable
    def expression(self):
        #Looking for conjunction. If not found, not an expression
        if (self.conjunction() == ERR): 
            return BRK

        #Looking for additional conjunctions if '||' is read
        while (True):
            #Looking for optional or statement
            if (self.token[VALUE] == "||" and self.QUIT == False):
                print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Expression")
                self.token = self.lex.next()

                #Looking for additional conjunction
                if (self.conjunction() == ERR): 
                    return ERR            
            else:
                break
        return CONT   

    # <Conjuncion> --> <Equality>     && <Equality>
    #                              ^^^^Repeatable
    def conjunction(self):

        #Looking for equality. If not found then there is no conjunction
        if (self.equality() == ERR): 
            return BRK

        #Looking for additional equalities if '%+&&' is read
        while (True):

            #Looking for optional and statement with '&&'
            if (self.token[VALUE] == "&&" and self.QUIT == False):
                print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Conjunction")
                self.token = self.lex.next()

                #Looking for equality        
                if (self.equality() == ERR): 
                    return ERR
            else:
                break

        return CONT

    #<equality> --> <Relation>     <EquOp> <Relation>
    #                            ^^^^^^^Optional
    def equality(self):
        #Looking for relation. if relation is not found then this is not an equality
        if (self.relation() == ERR): 
            return BRK

        #Looking for option equOp and second relation
        if (self.equOp() == CONT):
            #Looking for second relation
            if (self.relation() == ERR): 
                return ERR
        return CONT

    #<equOp> --> == | !=
    #           ^^^^^^^^^ one of the above
    def equOp(self):
        if ((self.token[VALUE] == "==" or self.token[VALUE] == "!=") and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- equOp")
            self.token = self.lex.next()
            return CONT
        else:
            return ERR    

    #<relation> --> <Addition>      <relOp> <Addition>
    #                           ^^^^^^^Optional
    def relation(self):
        #Looking for addition. If not found, this is not a relation
        if (self.addition() == ERR): 
            return BRK
        #Looking for optional relative operator
        if (self.relOp() == CONT):

            #If optional relop is found, find addition
            if (self.addition() == ERR): 
                return ERR
        return CONT

    #<relOp> --> < | <= | > | >=
    #            ^^^^^^^^^^^^^ one of the above
    def relOp(self):
        if ((self.token[VALUE] == "<" or self.token[VALUE] == "<=" or self.token[VALUE] == ">" or self.token[VALUE] == ">=") and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- relOp")
            self.token = self.lex.next()
            return CONT
        else:
            return ERR

    #<addition> --> <term>    <addOp> <Term>
    #                       ^^^^repeatable
    def addition(self):
        #Looking for term, if not found then this is not addition
        if (self.term() == ERR): 
            return BRK

        #Looking for additional terms to add
        while (True):
            
            #Looking for addOp
            if (self.addOp() == CONT):

                #Looking for term to add if addOp was found
                if (self.term() == ERR): 
                    return ERR
            else:
                break
        return CONT

    #<addOp> --> + | -
    #            ^^^^^ One of the above
    def addOp(self):
        if ((self.token[VALUE] == "+" or self.token[VALUE] == "-") and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- addOp")
            self.token = self.lex.next()
            return CONT
        else:
            return ERR

    #<term> --> <Factor>     <MulOp> <Factor>
    #                      ^^^^^Repeatable
    def term(self):
        #Looking for factor. If not found, this is not a term
        if (self.factor() == ERR): 
            return BRK
        #Looking for additional factors to multiply
        while (True):
            
            #Looking for possible multiply operator
            if (self.mulOp() == CONT):
                if (self.factor() == ERR): 
                    return ERR
            else:
                break
        return CONT

    #<mulOp> --> * | / | %
    #            ^^^^^^ one of the above
    def mulOp(self):
        if ((self.token[VALUE] == "*" or self.token[VALUE] == "/" or self.token[VALUE] == "%") and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- mulOp")
            self.token = self.lex.next()
            return CONT
        else:
            return ERR

    #<factor> --> <UnaryOp>    <Primary>
    #            ^^^Optional   ^^^^Needed
    def factor(self):
        #Looking for Optional unaryOp
        self.unaryOp()

        #Looking for primary
        if (self.primary() == ERR): 
            return ERR
        
        return CONT

    #<unaryOp> --> - | !
    #              ^^^^One of the above
    def unaryOp(self):
        if ((self.token[VALUE] == "-" or self.token[VALUE] == "!") and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- unaryOp")
            self.token = self.lex.next()
            return CONT
        else:
            return ERR

    #<primary> --> <Identifier>    [<Expression>]    |     <Literal>      |     (<Expression>)      |   <Type> (<Expression>)
    #Choose one of the above       ^^^^^Optional
    def primary(self):
        #Option 1 - Looking for identifier. If not found then not a primary
        if (self.identifier() == CONT):

            #Looking for optional '[' to begin array
            if (self.token[VALUE] == "[" and self.QUIT == False):
                print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Primary")
                self.token = self.lex.next()

                #Looking for expression for array
                if (self.expression() == ERR): 
                    return ERR

                #Looking for array closing bracket, ']'
                if (self.token[VALUE] == "]" and self.QUIT == False):
                    print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Primary")
                    self.token = self.lex.next()
                    return CONT
                else:
                    if (self.QUIT == True):
                        return ERR
                    if (self.token == "EOF"):
                        print("Parsing failed - read:", "NULL", "but expected ']' to close expression array in primary at line ", "EOF")
                    else: print("Parsing failed - read:", self.token[VALUE], "but expected ']' to close expression array in primary at line ", self.token[LINENUMBER])
                    self.QUIT = True
                    return ERR

        #Option 2 - If not identifier, look for Literal
        elif(self.literal() == CONT): 
            return CONT

        #Option 3 - Looking for (<expression>)
        elif(self.token[VALUE] == "(" and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Primary")
            self.token = self.lex.next()

            #Looking for expression
            if (self.expression() == ERR): return ERR

            #Looking for closing parenthesis
            if (self.token[VALUE] == ")" and self.QUIT == False):
                print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Primary")
                self.token = self.lex.next()
                return CONT
            else:
                if (self.QUIT == True):
                    return ERR
                if (self.token == "EOF"):
                    print("Parsing failed - read:", "NULL", "but expected ')'in primary at line ", "EOF")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected ')'in primary at line", self.token[LINENUMBER])
                self.QUIT = True
                return ERR

        #Option 4 -Looking for <Type> (<Expression>)
        elif(self.Type() == CONT):

            #if type is found, look for opening parenthesis
            if(self.token[VALUE] == "(" and self.QUIT == False):
                print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Primary")
                self.token = self.lex.next()
            else:
                if (self.QUIT == True):
                    return ERR
                if (self.token == "EOF"):
                    print("Parsing failed - read:", "NULL", "but expected '(' in primary at line ", "EOF")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected '(' in primary at line ", self.token[LINENUMBER])
                self.QUIT = True
                return ERR
            
            #Look for expression
            if (self.expression() == ERR): 
                return ERR

            #Look for closing parenthesis
            if (self.token[VALUE] == ")" and self.QUIT == False):
                print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Primary")
                self.token = self.lex.next()
                return CONT
            else:
                if (self.QUIT == True):
                    return ERR
                if (self.token == "EOF"):
                    print("Parsing failed - read:", "NULL", "but expected ')' in primary at line ", "EOF")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected ')' in primary at line  ", self.token[LINENUMBER])
                self.QUIT = True
                return ERR

        #no option in primary was found
        return CONT

    #<literal> --> <Integer> | <Boolean> | <Float> | <Char>
    #               ^^^^^^One of the above
    def literal(self):
        if (self.integer() == CONT): 
            return CONT
        elif (self.boolean() == CONT): 
            return CONT
        elif (self.Float() == CONT): 
            return CONT
        elif (self.char() == CONT): 
            return CONT
        else:
            return ERR

    #<integer> --> <Digit>    <Digit>
    #                       ^^^^Repeatable        
    def integer(self):
        #Checks to see if the token is a digit
        if (self.token[CATEGORY] == "integer" and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Integer")
            self.token = self.lex.next()
            return CONT
        else:
            return ERR
    
    #<boolean> --> true | false
    #           ^^^^One of the above
    def boolean(self):
        if ((self.token[VALUE] == "true" or self.token[VALUE] == "false") and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Boolean")
            self.token = self.lex.next()
            return CONT
        else:
            return ERR

    #<float> --> <Integer> . <Integer>
    def Float(self):
        #Looking for first integer of float
        if (self.token[CATEGORY] != "real"): 
            return BRK
        if (self.QUIT == True):
            return ERR
        print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Float")
        self.token = self.lex.next()
        return CONT

    #<Char> --> 'ASCICHAR'
    def char(self):
        if (self.token[CATEGORY] != "char"):
            return BRK
        if (self.QUIT == True):
            return ERR
        print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Char")
        self.token = self.lex.next()
        return CONT


    '''
    identifier is found by the lexer and therefore we just need to check the token category from the lexer.
    We also do not need <letter> or <Digit>
    '''
    #<identifier> --> <Letter>      <Letter> | <Digit>
    #                           ^^^^^^^^Repeatable
    def identifier(self):

        #Check token category if it has been determined to be an identifier
        if (self.token[CATEGORY] == "identifier" and self.QUIT == False):
            print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Identifier")
            self.token = self.lex.next()
            return CONT
        else:
            return ERR

    #<letter> --> a | b | ... | z | A | B | .... | Z
    #         ^^^^^one of the above
    def letter(self):
        print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Letter")
        self.token = self.lex.next()
        return CONT

    
    #<digit> --> 1 | 2 | 3 | ... | 9
    #         ^^^^^one of the above
    def digit(self):
        print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Digit")
        self.token = self.lex.next()
        return CONT