1. Dominic Ferrante, Brian Rexroth, Drew Battison


2. The Parser takes the lexer as an imput so that every word read from the lexer can be parsed. The Program will begin at <Program> and will call other EBNF rules. Every non-terminal
rule is converted into a function so that they can be called. The function will return the the testMain class if the parsing was performed successfully. If a parsing error was read within
the file being read, then an output will display where the error took place and the program will end using sys.exit(0). The error is fairly accurate but sometimes the error may be slighly
different than you might expect, such as if you are missing the closing expression for an assignmentand the next line begins with an identifier (which is an expression). This still gives
a general area for where to see the error.


3. Description of all classes and functions:

The lexer class holds 3 items: the file that is read, the current line number within the file, and the token information  which will be added to a list. This token information 
includes the token's line number, value, and category. The category of the token is determined by comparing the 'word' being tokenized with the regular expressions for integers, 
real numbers, and identifiers. The 'word' will also be compared against the list of existing keywords, operators, and punctuation.

The main function of testMain.py will ask the user to enter the name of a file to be read which will be sent to the lexer. A lexer object, lex is initalized by calling 
lexer.lexer(f) which creates a new lexer with the parameter as the file being read. The main function will then loop until every token is popped from the list of tokens, 
thereby printing the result of every token in the file.

The lexer class has a few dictionaries: Keywords, Operators, and Punctuations. These dictionaries hold the existing names and strings of the corresponding dictionary 
used for token categorization. The lexer also has regular expressions to match patterns for integers, real numbers, and identifiers also used for token categorization.

The lexer class also contains the following functions:

     __init__ takes the parameters of self (The Lexer) and the file being read. This function initializes the lexer and will allow the lexer to have the file: f, 
     the line number: lineNumber, and a list of tokens: tokenQueue. This will allow the lexer to access this information in the other functions of the lexer. The function
     generateTokens will then be called to traverse the file for tokens.

     generateTokens takes only the lexer as a parameter: self. This function will traverse every line of the file stored in lexer and will then tokenize every word in 
     each line. Each word will then be sent to lex() in order to complete the tokenization.

     lex takes the parameters of the lexer: self, and the word being tokenized: word. This function will compare the the word to the lexer's dictionaries and regular 
     expressions. The token will then be appended to the tokenQueue including the lineNumber, value, and category.
     
     next takes only the lexer as a parameter: self. This function is meant to be called from main to retrieve each token from the lexer. After the lexer finished, 
     next() is used to pop every token out of the list of tokens.


The parse class holds 2 items: an instantiation of the lexer being parsed and the current token read from self.lex.next(). The parse class is called from the main class
as par = parse.parse(lex) for instantiation. This will send the parser the lexed file to perform parsing on. The main will then perform the parse by running par.program() so 
that an effective parse will return to the main.

The parse class contains the following functions (All functions other than __init__ have only self as a parameter:

     __init__ takes the parameters of self (the parser) and the lexer being read. This function initialized the parser so that the parser has access to information from the lexer.

     Program is meant to perform the following EBNF rule: 		<Program> --> int main() {<Declarations> <Statements>}

     Declarations is meant to perform the following EBNF rule:		<Declarations> --> <Declaration>
										<Declaration> is repeatable 

     Declaration is meant to perform the following EBNF rule:		<declaration> --> <Type> <Identifier> [<Integer>] , <Identifier> [<integer>] ;
										[<integer>] is optional and , <Identifier> [<integer>] is repeatable

     Type is meant to perform the following EBNF rule:			<Type> --> int | bool | float | char

     Statements is meant to perform the following EBNF rule:		<statements> --> <statement>
										<Statement> is repeatable

     Statement is meant to perform the following EBNF rule:		<statement> --> ; | <block> | <assignment> | <iftstatement> | <whilestatement>

     Block is meant to perform the following EBNF rule:			<block> --> { <Statements> }

     Assignment is meant to perform the following EBNF rule:		<Assignment> --> <Identifier>[<expression>] = <expression>
										[expression>] is optional

     IfStatement is meant to perform the following EBNF rule:		<ifStatement> --> if( <expression> ) <statement>    else <statement>
										else <statement> is optional<whileStatement> --> while( <expression> ) <Statement>

     WhileStatement is meant to perform the following EBNF rule:	<whileStatement> --> while( <expression> ) <Statement>

     Expression is meant to perform the following EBNF rule:		<expression> --> <Conjunction> || <Conjunction>
										|| <Conjunction> is repeatable

     Conjunction is meant to perform the following EBNF rule:		<Conjuncion> --> <Equality> && <Equality>
										&& <Equality> is repeatable

     Equality is meant to perform the following EBNF rule:		<equality> --> <Relation> <EquOp> <Relation>
										<EquOp> <Relation> is optional

     EquOp is meant to perform the following EBNF rule:			<equOp> --> == | !=

     Relation is meant to perform the following EBNF rule:		<relation> --> <Addition> <relOp> <Addition>
										<relOp> <Addition> is optional

     RelOp is meant to perform the following EBNF rule:			<relOp> --> < | <= | > | >=

     Addition is meant to perform the following EBNF rule:		<addition> --> <term> <addOp> <Term>
										<addOp> <Term> is repeatable

     AddOp is meant to perform the following EBNF rule:			<addOp> --> + | -

     Term is meant to perform the following EBNF rule:			<term> --> <Factor> <MulOp> <Factor>
										<MulOP> <Factor> is repeatable

     MulOp is meant to perform the following EBNF rule:			<mulOp> --> * | / | %

     Factor is meant to perform the following EBNF rule:		<factor> --> <UnaryOp>    <Primary>
										<unaryOp> is optional

     UnaryOp is meant to perform the following EBNF rule:		<unaryOp> --> - | !

     Primary is meant to perform the following EBNF rule:		<primary> --> <Identifier> [<Expression>] | <Literal> | (<Expression>) | <Type> (<Expression>)
										[<Expression>] is optional

     Identifier is meant to perform the following EBNF rule:		#<identifier> --> <Letter> <Letter> | <Digit>
										<letter> | <digit> is repeatable
										Identifier is found by the lexer. Just need to check self.token[CATEGORY]!!!

     Letter is meant to perform the following EBNF rule:		<letter> --> a | b | ... | z | A | B | .... | Z
										Never called. Lexer already seperates tokens by "words"

     Digit is meant to perform the following EBNF rule:			<digit> --> 1 | 2 | 3 | ... | 9
										Never called. Lexer already seperates tokens by "words"

     Literal is meant to perform the following EBNF rule:		<literal> --> <Integer> | <Boolean> | <Float> | <Char>

     Integer is meant to perform the following EBNF rule:		<integer> --> <Digit> <Digit>
										<Digit> is repeatable
										Integer is found by the lexer. Just need to check self.token[CATEGORY]!!!

     Boolean is meant to perform the following EBNF rule:		<boolean> --> true | false

     Float is meant to perform the following EBNF rule:			#<float> --> <Integer> . <Integer>
										Float is found by the lexer. Just need to check self.token[CATEGORY]!!!

     Char is meant to perform the following EBNF rule:			<Char> --> 'ASCICHAR'
										Char is found by the lexer. Just need to check self.token[CATEGORY]!!!


4. (This is written as with the expectation of using windows cmd)
First you need to have python3 installed.
Then cd <directory> where <directory is the folder containing the following: testMain.py   lexer.py   parse.py   sample.txt   sample2.txt   sample3.txt
After you reached the desired folder, type: python3 testMain.py
Then you will be asked for the file and you should type: sample.txt

Example from my PC (After cmd is opened):
cd C:\Users\drewb\Documents\College\2020_2021_Sem_1\Programming Languages\Parser and Lexer Project\Parser Portion\ProgrammingLanguage-master
C:\Users\drewb\Documents\College\2020_2021_Sem_1\Programming Languages\Parser and Lexer Project\Parser Portion\ProgrammingLanguage-master>python3 testMain.py
Please enter testing file: sample.txt


5. The 3 files to be run to test the parser are sample.txt, sample2.txt, sample3.txt

sample.txt - Sample.txt runs every CLite rule correctly in order to show that the parser is working correctly.

sample2.txt - The same code as sample.txt but with an error in declaration. In line 5, the file is missing an identifier after readin a comma causing a parsing error.

sample3.txt - The same code as sample.txt but with an error in assignment. In line 23, the file is missing an expression after "=" and therefore the parser will display an
error that it read "}" in line 24 instead of the expected expression. 