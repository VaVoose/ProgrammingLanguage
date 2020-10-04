1. Dominic Ferrante, Brian Rexroth, Drew Battison


2. This code will read in a file that is inputted into the command line after running main. This txt file will then be sent to the lexer class in order to seperate tokens 
and give the token's line number, value, and category. The lexer will ignore any comments and spaces so no empty lines or characters after "//" will be tokenized. 
The file will be read line by line and each 'word' in the line will be tokenized.


3. This lexer is the only class of the program. The lexer class holds 3 items: the file that is read, the current line number within the file, and the token information 
which will be added to a list. This token information includes the token's line number, value, and category. The category of the token is determined by comparing the 
'word' being tokenized with the regular expressions for integers, real numbers, and identifiers. The 'word' will also be compared against the list of existing keywords, 
operators, and punctuation.

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
     
     
4. (This is written as with the expectation of using windows cmd)
First you need to have python3 installed.
Then cd <directory> where <directory is the folder containing the following: testMain.py   lexer.py   test_input.txt
After you reached the desired folder, type: python3 testMain.py
Then you will be asked for the file and you should type: test_input.txt

Example from my PC (After cmd is opened):
C:\Users\drewb>cd C:\Users\drewb\Documents\College\2020_2021_Sem_1\Programming Languages\Parser and Lexer Project\ProgrammingLanguages(Lexer)
C:\Users\drewb\Documents\College\2020_2021_Sem_1\Programming Languages\Parser and Lexer Project\ProgrammingLanguages(Lexer)>python3 testMain.py
Please enter testing file: test_input.txt
