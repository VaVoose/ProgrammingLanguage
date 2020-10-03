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
        if (self.token[VALUE] == "int"):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Program")
            self.token = self.lex.next()

            if (self.token[VALUE] == "main"):
                #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Program")
                self.token = self.lex.next()

                if (self.token[VALUE] == "("):
                    #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Program")
                    self.token = self.lex.next()
                    
                    if (self.token[VALUE] == ")"):
                        #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Program")
                        self.token = self.lex.next()
                        
                        if (self.token[VALUE] == "{"):
                            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Program")
                            self.token = self.lex.next()
                            
                            #Get delarations
                            self.declarations()

                            #Get statements
                            self.statements()

                            #Program Ends successfully
                            if (self.token[VALUE] == "}"):
                                self.token = self.lex.next()
                                if (self.token != "EOF"):
                                    print("Parsing Failed - Ending '}' was found before the end of the file!! -- Read", self.token[VALUE], "at line", self.token[LINENUMBER], "\n")
                                    exit(0)
                                #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Program")
                                return SUCCESS
                            else:
                                if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected '}' to end program at line", "EOF\n")
                                else: print("Parsing failed - read:", self.token[VALUE], "but expected '}' to end program at line", self.token[LINENUMBER], "\n")
                                sys.exit(0)
                        else:
                            if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected '{' in program at line", "EOF\n")
                            else: print("Parsing failed - read:", self.token[VALUE], "but expected '{' in program at line", self.token[LINENUMBER], "\n")
                            sys.exit(0)
                    else:
                        if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected ')' in program at line", "EOF\n")
                        else: print("Parsing failed - read:", self.token[VALUE], "but expected ')' in program at line", self.token[LINENUMBER], "\n")
                        sys.exit(0)
                else:
                    if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected '(' in program at line", "EOF\n")
                    else: print("Parsing failed - read:", self.token[VALUE], "but expected '(' in program at line", self.token[LINENUMBER], "\n")
                    sys.exit(0)
            else:
                if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected 'main' in program at line", "EOF\n")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected 'main' in program at line", self.token[LINENUMBER], "\n")
                sys.exit(0)
        else:
            if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected 'int' in program at line", "EOF\n")
            else: print("Parsing failed - read:", self.token[VALUE], "but expected 'int' in program at line", self.token[LINENUMBER], "\n")
            sys.exit(0)

        #<declarations> --> <declaration>
    #                   ^^^^ Repeatable
    def declarations(self):
        while(True):      
            if (self.declaration() == BRK):
                self.declaration()
                break
        return CONT

    #<declaration> --> <Type> <Identifier>   [<Integer>]     , <Identifier>    [<integer>]     ;
    #                                        ^^^Optional    ^^^^^^Repeatable  ^^Optional       ^^^needed
    def declaration(self):

        #A declaration must begin with a type 
        #If a type does not exist, then the statement is not a declaration!
        if (self.Type() == BRK): 
            return BRK

        #A declaration must also have an identifier
        if (self.identifier() == BRK): 
            if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected an identifier for declaration at line ", "EOF\n")
            else: print("Parsing failed - read:", self.token[VALUE], "but expected an identifer for delcaration at line", self.token[LINENUMBER], "\n")
            sys.exit(0)

        #The identifer can also have an optional array location
        if (self.token[VALUE] == "["):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Declaration")
            self.token = self.lex.next()

            #After [ was read, there must be an integer for the array location
            if (self.integer() == BRK): 
                if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected an an integer for the array location of identifier during declaration at line ", "EOF\n")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected an integer for the array location of identifier during declaration at line", self.token[LINENUMBER], "\n")
                sys.exit(0)

            #The array must have ] as a closing bracket
            if (self.token[VALUE] == "]"):
                #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Declaration")
                self.token = self.lex.next()
            else:
                if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected ']' to close identifier's array location during declaration at line ", "EOF\n")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected ']' to close identifier's array location during declaration at line ", self.token[LINENUMBER], "\n")
                sys.exit(0)

        #Possibly adding more identifiers
        while(True):

            #Look for optional comma for additional identifiers
            if (self.token[VALUE] == ","):
                #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Declaration")
                self.token = self.lex.next()

                #Adding additional identifier if a comma was read
                if (self.identifier() == BRK): 
                    if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected an additional identifier during declaration after comma at line ", "EOF\n")
                    else: print("Parsing failed - read:", self.token[VALUE], "but expected an additonal identifier during declaration after comma at line", self.token[LINENUMBER], "\n")
                    sys.exit(0)   

                #Checking to see if the identifier has an array location     
                if (self.token[VALUE] == "["):
                    #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Declaration")
                    self.token = self.lex.next()

                    #After [ was read, there must be an integer for the array location
                    if (self.integer() == BRK): 
                        if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected an integer for the array location of additional identifier during declaration at line ", "EOF\n")
                        else: print("Parsing failed - read:", self.token[VALUE], "but expected an integer for the array location of additonal identifier during declaration at line", self.token[LINENUMBER], "\n")
                        sys.exit(0)
                    #The array must have ] as a closing bracket
                    if (self.token[VALUE] == "]"):
                        #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Declaration")
                        self.token = self.lex.next()
                    else:
                        if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected ']' to close additional identifier's array location during declaration at line ", "EOF\n")
                        else: print("Parsing failed - read:", self.token[VALUE], "but expected ']' to close additional identifier's array location during declaration at line ", self.token[LINENUMBER], "\n")
                        sys.exit(0) 
                else:
                    #Look for more identifiers
                    continue
            else:
                #Stop looking for identifers and look for declaration end
                break

        #Look for semicolon to end declaration
        if (self.token[VALUE] == ";"):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Declaration")
            self.token = self.lex.next()
            return CONT
        else:
            if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected ';' to end declaration at line ", "EOF\n")
            else: print("Parsing failed - read:", self.token[VALUE], "but expected ';'' to end declaration at line ", self.token[LINENUMBER], "\n")
            sys.exit(0)

    #<Type> --> int | bool | float | char
    #           ^^^^^^^^^^ one of the above
    def Type(self):
        result = self.token[VALUE]
        if (result == "bool" or result == "int" or result == "float" or result == "char"):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Type")
            self.token = self.lex.next()
            return CONT
        else:
            return BRK

    #<statements> --> <statement>
    #                ^^^^Repeatable
    def statements(self):
        while(True):
            if (self.statement() == BRK):
                self.statement()
                break
        return CONT
    
    #<statement> --> ; | <block> | <assignment> | <iftstatement> | <whilestatement>
    #               ^^^^One of the above
    def statement(self):
        #Go through the possible options for statement
        if (self.token[VALUE] == ";"):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Statement")
            self.token = self.lex.next()
            return CONT

        elif (self.block() == CONT):
            return CONT

        elif (self.assignment() == CONT):
            return CONT

        elif (self.ifStatement() == CONT):
            return CONT

        elif (self.whileStatement() == CONT):
            return CONT

        return BRK

    #<block> --> { <Statements> }
    def block(self):
        #Check to see if the statement is a block. A block begins with {
        if (self.token[VALUE] == "{"):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Block")
            self.token = self.lex.next()

            #Get statements to place within block
            self.statements()

            #Get closing bracket of block
            if (self.token[VALUE] == "}"):
                #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Block")
                self.token = self.lex.next()
                return CONT
            else:
                if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected '}' to close the block at line ", "EOF\n")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected '}' to close the block at line ", self.token[LINENUMBER], "\n")
                sys.exit(0)
        return BRK

    #<Assignment> --> <Identifier>[<expression>] = <expression>
    #                               ^^^ optional [expression]
    def assignment(self):
        #reading an identifier, if no identifier is found then this is not an assignment
        if (self.identifier() == BRK):
            return BRK

        #Look for possible [ for expression
        if (self.token[VALUE] == "["):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Assignment")
            self.token = self.lex.next()

            #Finding expression
            if (self.expression() == BRK): 
                if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected an expression in assignment at line ", "EOF\n")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected an expression in assignment at line", self.token[LINENUMBER], "\n")
                sys.exit(0)

            #Closing ] to end 
            if (self.token[VALUE] == "]"):
                #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Assignment")
                self.token = self.lex.next()
            else:
                if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected ']' for assignment in line ", "EOF\n")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected ']' for assignment in line ", self.token[LINENUMBER], "\n")
                sys.exit(0)

        #Need to continue assignment with "="
        if (self.token[VALUE] == "="):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Assignment")
            self.token = self.lex.next()

            if (self.expression() == BRK): 
                if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected an expression in assignment at line ", "EOF\n")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected an expression in assignment at line", self.token[LINENUMBER], "\n")
                sys.exit(0)
        else:
            if (self.token == "EOF"):
                print("Parsing failed - read:", "NULL", "but expected '=' for assignmnet in line ", "EOF\n")
            else: print("Parsing failed - read:", self.token[VALUE], "but expected '=' from assignment in line ", self.token[LINENUMBER], "\n")
            sys.exit(0)

        return CONT

    #<ifStatement> --> if( <expression> ) <statement>    else <statement>
    #                                                  ^^^^^^^ Optional additions    
    def ifStatement(self):

        #If the statement does not begin with 'if', it is not an ifstatement
        if (self.token[VALUE] == "if"):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- ifStatement")
            self.token = self.lex.next()
        else:
            return BRK

        #If an if statement, there needs to be '(' to look for expressions
        if (self.token[VALUE] == "("):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- ifStatement")
            self.token = self.lex.next()
        else: 
            if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected '(' in ifstatement at line ", "EOF\n")
            else: print("Parsing failed - read:", self.token[VALUE], "but expected '(' in ifstatement at line ", self.token[LINENUMBER], "\n")
            sys.exit(0)

        #Look for expressions within parenthesis
        if (self.expression() == BRK): 
            if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected an expression in ifstatement at line ", "EOF\n")
            else: print("Parsing failed - read:", self.token[VALUE], "but expected an expression in ifstatement at line", self.token[LINENUMBER], "\n")
            sys.exit(0)

        #Looking for closing parenthesis
        if (self.token[VALUE] == ")"):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- ifStatement")
            self.token = self.lex.next()
        else:
            if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected ')' in ifstatemen at line ", "EOF\n")
            else: print("Parsing failed - read:", self.token[VALUE], "but expected ')' in ifstatement at line ", self.token[LINENUMBER], "\n")
            sys.exit(0)

        #Looking for closing statement to end ifstatement
        if (self.statement() == BRK): 
            if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected a statement in ifstatement at line ", "EOF\n")
            else: print("Parsing failed - read:", self.token[VALUE], "but expected a statement in ifstatement at line", self.token[LINENUMBER], "\n")
            sys.exit(0)
                    
        #Look for possible else statement for additional ifstatements
        if (self.token[VALUE] == "else"):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- ifStatement")
            self.token = self.lex.next()
            
            #Look for statement
            if (self.statement() == BRK): 
                if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected a statement in ifstatement at line ", "EOF\n")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected a statement in ifstatement at line", self.token[LINENUMBER], "\n")
                sys.exit(0)
       
        return CONT

    #<whileStatement> --> while( <expression> ) <Statement>
    def whileStatement(self):

        #If the statement does not begin with 'while', it is not a whilestatement
        if (self.token[VALUE] == "while"):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- whileStatement")
            self.token = self.lex.next()
        else:
            return BRK

        #If while statement, you need to begin with '('
        if (self.token[VALUE] == "("):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- whileStatement")
            self.token = self.lex.next()
        else:
            if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected '(' tin whilestatement at line ", "EOF\n")
            else: print("Parsing failed - read:", self.token[VALUE], "but expected'(' in whilestatement at line ", self.token[LINENUMBER], "\n")
            sys.exit(0)

        #Looking for expression between parenthesis for whilestatement
        if (self.expression() == BRK): 
            if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected an expression in whilestatement at line ", "EOF\n")
            else: print("Parsing failed - read:", self.token[VALUE], "but expected an expression in whilestatement at line", self.token[LINENUMBER], "\n")
            sys.exit(0)

        if (self.token[VALUE] == ")"):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- whileStatement")
            self.token = self.lex.next()
        else:
            if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected ')' in whilestatement at line ", "EOF\n")
            else: print("Parsing failed - read:", self.token[VALUE], "but expected ')' in whilestatement at line ", self.token[LINENUMBER], "\n")
            sys.exit(0)

        #Look for statement
        if (self.statement() == BRK): 
            if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected a statement in whilestatement at line ", "EOF\n")
            else: print("Parsing failed - read:", self.token[VALUE], "but expected a statement in whilestatement at line", self.token[LINENUMBER], "\n")
            sys.exit(0)

        return CONT

    #<expression> --> <Conjunction>    || <Conjunction>
    #                                ^^^^^Repeatable
    def expression(self):
        #Looking for conjunction. If not found, not an expression
        if (self.conjunction() == BRK): 
            return BRK

        #Looking for additional conjunctions if '||' is read
        while (True):
            #Looking for optional or statement
            if (self.token[VALUE] == "||"):
                #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Expression")
                self.token = self.lex.next()

                #Looking for additional conjunction
                if (self.conjunction() == BRK): 
                    if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected a conjunction in expression at line ", "EOF\n")
                    else: print("Parsing failed - read:", self.token[VALUE], "but expected a conjunction in expression at line", self.token[LINENUMBER], "\n")
                    sys.exit(0)      
            else:
                break
        return CONT   

    # <Conjuncion> --> <Equality>     && <Equality>
    #                              ^^^^Repeatable
    def conjunction(self):

        #Looking for equality. If not found then there is no conjunction
        if (self.equality() == BRK): 
            return BRK

        #Looking for additional equalities if '%+&&' is read
        while (True):

            #Looking for optional and statement with '&&'
            if (self.token[VALUE] == "&&"):
                #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Conjunction")
                self.token = self.lex.next()

                #Looking for equality        
                if (self.equality() == BRK): 
                    if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected an eqaulity in conjunction at line ", "EOF\n")
                    else: print("Parsing failed - read:", self.token[VALUE], "but expected an equality at conjunction at line", self.token[LINENUMBER], "\n")
                    sys.exit(0)
            else:
                break

        return CONT

    #<equality> --> <Relation>     <EquOp> <Relation>
    #                            ^^^^^^^Optional
    def equality(self):
        #Looking for relation. if relation is not found then this is not an equality
        if (self.relation() == BRK): 
            return BRK

        #Looking for option equOp and second relation
        if (self.equOp() == CONT):

            #Looking for second relation
            if (self.relation() == BRK): 
                if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected a relation in equality at line ", "EOF\n")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected a relation in equality at line", self.token[LINENUMBER], "\n")
                sys.exit(0)
        return CONT

    #<equOp> --> == | !=
    #           ^^^^^^^^^ one of the above
    def equOp(self):
        if (self.token[VALUE] == "==" or self.token[VALUE] == "!="):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- equOp")
            self.token = self.lex.next()
            return CONT
        return BRK   

    #<relation> --> <Addition>      <relOp> <Addition>
    #                           ^^^^^^^Optional
    def relation(self):
        #Looking for addition. If not found, this is not a relation
        if (self.addition() == BRK): 
            return BRK
        #Looking for optional relative operator
        if (self.relOp() == CONT):

            #If optional relop is found, find addition
            if (self.addition() == BRK): 
                if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected an addition in relation at line ", "EOF\n")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected an addition in relation at line", self.token[LINENUMBER], "\n")
                sys.exit(0)
        return CONT

    #<relOp> --> < | <= | > | >=
    #            ^^^^^^^^^^^^^ one of the above
    def relOp(self):
        if (self.token[VALUE] == "<" or self.token[VALUE] == "<=" or self.token[VALUE] == ">" or self.token[VALUE] == ">="):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- relOp")
            self.token = self.lex.next()
            return CONT
        return BRK

    #<addition> --> <term>    <addOp> <Term>
    #                       ^^^^repeatable
    def addition(self):
        #Looking for term, if not found then this is not addition
        if (self.term() == BRK): 
            return BRK

        #Looking for additional terms to add
        while (True):
            
            #Looking for addOp
            if (self.addOp() == CONT):

                #Looking for term to add if addOp was found
                if (self.term() == BRK): 
                    if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected a term in addition at line ", "EOF\n")
                    else: print("Parsing failed - read:", self.token[VALUE], "but expected a term in addition at line", self.token[LINENUMBER], "\n")
                    sys.exit(0)

            else:
                break
        return CONT

    #<addOp> --> + | -
    #            ^^^^^ One of the above
    def addOp(self):
        if (self.token[VALUE] == "+" or self.token[VALUE] == "-"):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- addOp")
            self.token = self.lex.next()
            return CONT
        return BRK

    #<term> --> <Factor>     <MulOp> <Factor>
    #                      ^^^^^Repeatable
    def term(self):
        #Looking for factor. If not found, this is not a term
        if (self.factor() == BRK): 
            return BRK
        #Looking for additional factors to multiply
        while (True):
            
            #Looking for possible multiply operator
            if (self.mulOp() == CONT):

                #If a multiply operator is found, we need a factor to go with it
                if (self.factor() == BRK): 
                    if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected a factor in term at line ", "EOF\n")
                    else: print("Parsing failed - read:", self.token[VALUE], "but expected a factor in term at line", self.token[LINENUMBER], "\n")
                    sys.exit(0)
            else:
                break
        return CONT

    #<mulOp> --> * | / | %
    #            ^^^^^^ one of the above
    def mulOp(self):
        if (self.token[VALUE] == "*" or self.token[VALUE] == "/" or self.token[VALUE] == "%"):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- mulOp")
            self.token = self.lex.next()
            return CONT
        return BRK

    #<factor> --> <UnaryOp>    <Primary>
    #            ^^^Optional   ^^^^Needed
    def factor(self):
        #Looking for Optional unaryOp
        self.unaryOp()

        #Looking for primary
        if (self.primary() == BRK): 
            return BRK  

        return CONT

    #<unaryOp> --> - | !
    #              ^^^^One of the above
    def unaryOp(self):
        if (self.token[VALUE] == "-" or self.token[VALUE] == "!"):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- unaryOp")
            self.token = self.lex.next()
            return CONT
        return BRK

    #<primary> --> <Identifier>    [<Expression>]    |     <Literal>      |     (<Expression>)      |   <Type> (<Expression>)
    #Choose one of the above       ^^^^^Optional
    def primary(self):
        #Option 1 - Looking for identifier. If not found then not a primary
        if (self.identifier() == CONT):

            #Looking for optional '[' to begin array
            if (self.token[VALUE] == "["):
                #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Primary")
                self.token = self.lex.next()

                #Looking for expression
                if (self.expression() == BRK):
                    if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected an expression in primary at line ", "EOF\n")
                    else: print("Parsing failed - read:", self.token[VALUE], "but expected an expression in primary at line", self.token[LINENUMBER], "\n")
                    sys.exit(0)


                #Looking for array closing bracket, ']'
                if (self.token[VALUE] == "]"):
                    #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Primary")
                    self.token = self.lex.next()
                    return CONT
                else:
                    if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected ']' to close expression array in primary at line ", "EOF\n")
                    else: print("Parsing failed - read:", self.token[VALUE], "but expected ']' to close expression array in primary at line ", self.token[LINENUMBER], "\n")
                    sys.exit(0)

            return CONT

        #Option 2 - If not identifier, look for Literal
        elif(self.literal() == CONT): 
            return CONT

        #Option 3 - Looking for (<expression>)
        elif(self.token[VALUE] == "("):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Primary")
            self.token = self.lex.next()

            #Looking for expression
            if (self.expression() == BRK):
                if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected an expression in primary at line ", "EOF\n")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected an expression in primary at line", self.token[LINENUMBER], "\n")
                sys.exit(0)

            #Looking for closing parenthesis
            if (self.token[VALUE] == ")"):
                #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Primary")
                self.token = self.lex.next()
                return CONT
            else:
                if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected ')' in primary at line ", "EOF\n")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected ')' in primary at line", self.token[LINENUMBER], "\n")
                sys.exit(0)

        #Option 4 -Looking for <Type> (<Expression>)
        elif(self.Type() == CONT):

            #if type is found, look for opening parenthesis
            if(self.token[VALUE] == "("):
                #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Primary")
                self.token = self.lex.next()
            else:
                if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected '(' in primary at line ", "EOF\n")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected '(' in primary at line ", self.token[LINENUMBER], "\n")
                sys.exit(0)
            
            #Look for expression
            if (self.expression() == BRK): 
                if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected an expression in primary at line ", "EOF\n")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected an expression in primary at line  ", self.token[LINENUMBER], "\n")
                sys.exit(0)

            #Look for closing parenthesis
            if (self.token[VALUE] == ")"):
                #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Primary")
                self.token = self.lex.next()
                return CONT
            else:
                if (self.token == "EOF"): print("Parsing failed - read:", "NULL", "but expected ')' in primary at line ", "EOF\n")
                else: print("Parsing failed - read:", self.token[VALUE], "but expected ')' in primary at line  ", self.token[LINENUMBER], "\n")
                sys.exit(0)

        #no option in primary was found
        return BRK
    
    '''
    identifier is found by the lexer and therefore we just need to check the token category from the lexer.
    We also do not need <letter> or <Digit> as the lexer already seperates by "words"
    '''
    #<identifier> --> <Letter>      <Letter> | <Digit>
    #                           ^^^^^^^^Repeatable
    def identifier(self):

        #Check token category if it has been determined to be an identifier
        if (self.token[CATEGORY] == "identifier"):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Identifier")
            self.token = self.lex.next()
            return CONT
        else:
            return BRK

    #<letter> --> a | b | ... | z | A | B | .... | Z
    #         ^^^^^one of the above
    def letter(self):
        #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Letter")
        self.token = self.lex.next()
        return CONT

    
    #<digit> --> 1 | 2 | 3 | ... | 9
    #         ^^^^^one of the above
    def digit(self):
        #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Digit")
        self.token = self.lex.next()
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
        return BRK

    #<integer> --> <Digit>    <Digit>
    #                       ^^^^Repeatable        
    def integer(self):
        #Checks to see if the token is a digit
        if (self.token[CATEGORY] == "integer"):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Integer")
            self.token = self.lex.next()
            return CONT
        return BRK
    
    #<boolean> --> true | false
    #           ^^^^One of the above
    def boolean(self):
        if (self.token[VALUE] == "true" or self.token[VALUE] == "false"):
            #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Boolean")
            self.token = self.lex.next()
            return CONT
        return BRK

    #<float> --> <Integer> . <Integer>
    def Float(self):
        #Looking for first integer of float
        if (self.token[CATEGORY] != "real"): 
            return BRK
        #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Float")
        self.token = self.lex.next()
        return CONT

    #<Char> --> 'ASCICHAR'
    def char(self):
        if (self.token[CATEGORY] != "char"):
            return BRK
        #print("read", self.token[VALUE], "at line number", self.token[LINENUMBER], "--- Char")
        self.token = self.lex.next()
        return CONT