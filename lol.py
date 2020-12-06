# print("LOLterpreter!")
from tkinter import * 
from tkinter import filedialog
from tkinter import ttk
import re

#* -- GUI INITIALIZATIONS --
window = Tk()
window.geometry("1200x750") #widthxheight
window.title("Ang ganda ni Maam Kat LOLTERPRETER")
    

#* -- CLASSES --
class SourceCode(): # * class for the source code
    # constructor
    def __init__(self):
        self.code = "" # initialize the holder for the entire code
        self.keywords = {
            "^HAI$": "Code Delimiter", 
            "^KTHXBYE$": "Code Delimiter",
            "^BTW$":"Single Line Comment Delimiter",
            "^OBTW$":"Multiline Comment Delimiter",
            "^TLDR$":"Comment Delimiter", #Delimiters 
            "^I HAS A$":"Variable Declaration",
            "^ITZ$":"Variable Assignment",
            "^R$":"Assignment Operation Keyword", #IHAS A to R
            #^ "MAEK": "Explicit type-casting",
            "^AN$" : "Operand Separator",
            #^ "A": "Type cast helper",
            #^ "IS NOW A": "Type cast Specifier",
            "^VISIBLE$": "Output Keyword",
            "^GIMMEH$": "User input",  #MAEK to GIMMEH
            "^O RLY$": "Function Opening Delimiter",
            "^OI$C": "Function Closing Delimeter",
            "^YA RLY$": "if delimiter",
            "^NO WAI$": "else delimiter",
            "^MEBB$E" : "else-if delimeter", #O RLY to OIC,
            "^IT$" : "For Comparison in a Switch Case",
            "^WTF\?$":"Switch Case Start Delimiter",
            "^OMG$": "Case Specifier",
            "^OMGWTF$": "Default Switch Case Specifiier",
            "^GTFO$" : "Break Statement",
            "^OIC$" : "Switch Case End Delimiter",
            "^IM IN YR$": "Loop Opening Delimeter",
            "^UPPIN$": "Loop increment",
            "^Loop decrement$":"",#WTF? to Nerfin
            "^YR$": "Loop Variable Specifier",
            "^TIL$":"FAIL Loop specifier",
            "^WILE$": "WIN Loop Specifier",
            "^IM OUTTA YR$": "Loop Closing Delimeter" #YR to IM OUTTA YR
        }
        self.literals = {
            "\"": "String Delimiter",
            "-?[0-9][0-9]*" : "NUMBR Literal",
            "-?[0-9]*\.[0-9]+" : "NUMBAR Literal",
            "\".*\"": "YARN Literal",
            "^WIN$": "TROOF LIteral",
            "^FAIL$":"TROOF Literal",
            "^NUMBR$":"TYPE Literal",
            "^NUMBAR$":"TYPE Literal",
            "^YARN$": "TYPE Literal",
            "^TROOF$": "TYPE Literal",  #Literals
        }
        self.identifiers = {
            "[a-z]+[a-zA-Z0-9_]+": "Identifier", 
            # [a-z]+[a-zA-Z0-9_]+": "Variable Identifier", 
            # "[a-z]+[a-zA-Z0-9_]+": "Function Identifier", 
            # "[a-z]+[a-zA-Z0-9_]+": "Loop Identifier", 
        }
        self.operations = {
            "^SUM OF$": "Addition Operator", 
            "^DIFF OF$": "Substraction Operator",
            "^PRODUKT OF$": "Multiplication Operator",
            "^QUOSHUNT OF$": "Division Operator", #Sum of to Quoshunt of
            "^MOD OF$": "Modulo Operator",
            "^BIGGR OF$": "Maximum Operator",
            "^SMALLR OF$": "Minimum Operator", #MOD of to Smallr of
            "^BOTH OF$": "and operator",
            "^EITHER OF$": "or operator",
            "^WON OF$": "XOR Operator",
            "^NOT$": "Not operator",
            "^ANY OF$": "Inifinite arity or operator",
            "^ALL OF$": "inifinite arity and operator", #Both of to ALL OF
            "^BOTH SAEM$": "Equal comparison Operator",
            "^DIFFRINT$": "Not equal comparison operator",
            "^SMOOSH$": "Concatenation operator",  #BOTH SAEM to SMOOSH
        }
        self.lexemes=[]
        self.ITZ = ""

    def addCode(self, code): # set the code for object
        self.code = code
    
    def getCode(self):
        return self.code

    def getKeyWords(self):
        return self.keywords

    def getLiterals(self):
        return self.literals

    def getIdentifiers(self):
        return self.identifiers

    def getOperations(self):
        return self.operations

    def showMe(self):
        print("=====SOURCE CODE=====")
        print("THE CODE: ")
        print(self.code)
        print("---------------------")
        print("KEYWORDS")
        print(self.keywords)
        print("=====================")

    def getLexemes(self):
        return self.lexemes

class Lexeme():
    def __init__(self,mismo):
        self.mismo=mismo
        self.type=None
        self.value= None

    def setType(self,type):
        self.type=type
    
    def export(self, lexAndSymbolTables):
        lexAndSymbolTables.populateLexTable(self.mismo, self.type)
    

class SelectGUI(): # * class for grouping the select button and displaying the code uploaded
    def __init__(self):
        # select button
        self.selectSourceCode = Button(window, text="Select LOLCode file", width = 19, command=selectSourceCode)
        self.selectSourceCode.place(x=10, y=20, width=325)
        # textbox where the code will be displayed
        self.codeDisplay = Text(window, width=40, height=20, background="white")
        self.codeDisplay.place(x=10, y=50)

    def setCodeDisplay(self, code):
        self.codeDisplay.delete('1.0', END)
        self.codeDisplay.insert(END, code)

    def getCodeDisplay(self):
        return self.codeDisplay

class TablesGUI(): # * class for accessing and displaying the lexemes and symbol table
    def __init__(self):
        Label(window, text="LOL CODE Interpreter", font="none 19 bold", bg="black", fg="white").place(x=350, y=20, width=830)
        # lexemes table
        Label(window, text="Lexemes", font="none 15").place(x=510, y=60)
        self.lexTable = ttk.Treeview(window, columns=("Lexemes", "Classification"), show="headings")
        self.lexTableScroll = ttk.Scrollbar(window, orient="vertical", command=self.lexTable.yview)
        self.lexTable.column("Lexemes", width=200)
        self.lexTable.column("Classification", width=200)
        self.lexTable.heading("Lexemes", text="Lexemes")
        self.lexTable.heading("Classification", text="Classification")
        self.lexTable.place(x=350, y=90, height="282")
        self.lexTableScroll.place(x=753, y=90, height=282)
        self.lexTable.configure(yscrollcommand=self.lexTableScroll.set)

        # symbol table
        Label(window, text="Symbol Table", font="none 15").place(x=910, y=60)
        self.symbolTable = ttk.Treeview(window, columns=("Identifier", "Value"), show="headings")
        self.symbolTableScroll = ttk.Scrollbar(window, orient="vertical", command=self.symbolTable.yview)
        self.symbolTable.column("Identifier", width=200)
        self.symbolTable.column("Value", width=200)
        self.symbolTable.heading("Identifier", text="Identifier")
        self.symbolTable.heading("Value", text="Value")
        self.symbolTable.place(x=775, y=90, height="282")
        self.symbolTableScroll.place(x=1180, y=90, height=282)
        self.symbolTable.configure(yscrollcommand=self.symbolTableScroll.set)


    def getLexTable(self):
        return self.lexTable
    
    def populateLexTable(self, word, classification):
        self.lexTable.insert("", "end", values=(str(word), str(classification)))

    def populateSymbolTable(self, word, value):
        self.lexTable.insert("", "end", values=(str(word), str(value)))

class TerminalGUI(): # * class for accessing and displaying the "terminal", where the output of the program will be displayed
    def __init__(self):
        IT = "" # this is the implicit IT variable

        #execute button
        self.executeButton = Button(window, text="EXECUTE", width = 19, command=executeCode)
        self.executeButton.place(x=10, y= 375, width=1185)
        #textbox
        self.codeOutput = Text(window, background="white") # make this uneditable
        self.codeOutput.place(x=10, y=405, width=1185, height=325)

    def setDisplay(self, code):
        self.codeOutput.config(state=NORMAL)
        self.codeOutput.delete('1.0', END)
        self.codeOutput.insert(END, code)
        self.codeOutput.config(state=DISABLED)
        
#* -------------
#* -- FUNCTIONS --
def isKeyWord(word):
    keywords = theCode.getKeyWords()

# def parser(code): #* function that generates the parse tree of the statements
    keywords = theCode.getKeyWords()
    # iterate thryoughj every element in code
    for lineOfCode in code:
        if re.match(keywords["^VISIBLE"], lineOfCode):
            checkGrammar(lineCode, "print")


# ! notes we should be updating the symbol table that we refer to everytime we encounter an identifier, baka andun na kasi pala siya

def isStatement(code,lexemes):
    
    for element in code:
        #! VARIABLE DECLARATION
        if isVardec(element):
            makeLexeme("I HAS A","Variable Declaration",lexemes)

            #Split by space
            element=element.split(" ")
            tempSubstring= element[3:len(element)]
            # print(tempSubstring)

            if isVarident(tempSubstring[0]):#Unintialized var
                makeLexeme(tempSubstring[0], "Variable Identifier", lexemes)

                if len(tempSubstring) > 1 and re.match("^ITZ$",tempSubstring[1]):  #initialized var
                    isVarinit(tempSubstring,lexemes)
        #! PRINT STATEMENT
        elif isPrint(element):
            makeLexeme("VISIBLE","Print Statement",lexemes)
            element = element[7:len(element)] # remove the "VISIBLE" keyword from the string
            

            operands = parseVisibleOperand(element, lexemes) # this will return the operands of the visible statement
            print("OPERANDS",operands)

            # TODO : add a function call here that checks if an operand from operands exists in the SYMBOL table. if it is, remove it from the operands list
            for operand in operands: # determine the type of each operand
                if isExpr(operand, lexemes): # loosely check if the syntax follows an expression: <operation> <operand> AN <operand>
                    # pass the operand to isExpr(operand, lexemes) and should return the value to be displayed whatever the expression is
                    value = arithmetic(operand, lexemes) #  can only evaluate numbar or numbr for now
                    print(value)

                    if value == None:
                        print("MUST BE BOOLEAN")
                        bool_value = boolean(operand, lexemes)
                        # ! consider mo rin ung ANY OF AT ALL OF WITH INFINITY ARGUMENTS!

                        if bool_value == None:
                            print("MUST BE COMPARISON")
                            comp_value = comparison(operand, lexemes)

                elif isLiteral(operand, lexemes):
                    terminal.setDisplay(element)

        # ! ASSIGNMENT OPERATOR
        # elif isAssignment(element):

    #return lexeme table    
    return lexemes

# * ---------------------------------------------------------------------------------------------------- IS STATEMENT FXNS

def parseVisibleOperand(substring, lexemes): # * function that counts and collects the operand of a visible statement
    operand = [] # store the operands read
    tempHolder = "" # temp holder for the substring to be generated
    start = True # to determine if it's the start of the string
    end = False # to determine if it's the end of the string
    # iterate through every character in the string

    for char in substring:
        if start==True and char == "\"": # it's a yarn literal delimiter
            makeLexeme(char, "String Delimiter", lexemes)
            start = False
            end = True
        elif end == True and char == "\"": # end of the yarn delimiter
            makeLexeme(char, "String Delimiter", lexemes)
            # tempHolder = tempHolder + char
            end = False
            operand.append(tempHolder) # add the constructed string as an operand of the visible statement
            tempHolder="" # reset the value of tempHolder
        else: # it must be something else other than a yarn
            tempHolder = tempHolder + char
            # tempHolder = tempHolder+char
    operand.append(tempHolder)
    return operand

#def isCodeBlock
def isPrint(code):
    if re.match("^VISIBLE", code):
        return True
    return False
#def isVisibleOperand
def isExpr(substring,lexemes): # * function that determines if a substring is an expression
    if re.match("([A-Z\s]*) (.*) AN (.*)", substring):
        return True
    return False

    # elif isBoolean():
        # pass
    # elif isComparison():

def arithmetic(substring, lexemes): # * function that determines if an expr is an arithmetic expr, will return the evaluated expression
    operations = ["SUM", "DIFF", "BIGGR", "SMALLR", "PRODUKT", "QUOSHUNT", "MOD"]
    toEval = ""
    
    for operation in operations:
        # * REGEX FOR NUMBR
        arithmetic_regex = operation + " OF (-?[0-9][0-9]*) AN (-?[0-9][0-9]*)"
        pattern = re.compile(arithmetic_regex)
        
        for match in pattern.finditer(substring):
            
            evaluated_val = evaluateExpr(operation, match.group(1), match.group(2), "numbr")
            makeLexeme(operation+"OF", "Arithmetic Operator", lexemes)
            makeLexeme(match.group(1), "NUMBR", lexemes)
            makeLexeme("AN", "Operator Separator", lexemes)
            makeLexeme(match.group(2), "NUMBR", lexemes)
            return evaluated_val

        # * REGEX FOR NUMBAR
        arithmetic_regex = operation + " OF (-?[0-9]+\.[0-9]+) AN (-?[0-9]+\.[0-9]+)"
        pattern = re.compile(arithmetic_regex)
        
        for match in pattern.finditer(substring):
            evaluated_val = evaluateExpr(operation, match.group(1), match.group(2), "numbar")
            makeLexeme(operation+"OF", "Arithmetic Operator", lexemes)
            makeLexeme(match.group(1), "NUMBAR", lexemes)
            makeLexeme("AN", "Operator Separator", lexemes)
            makeLexeme(match.group(2), "NUMBAR", lexemes)
            return evaluated_val

    return None

def larger(first, second): #* function that returns which of the two parameters is larger\
    if first > second:
        return first
    return second

def smaller(first, second): #* function that reutns which of the two parameters is smaller
    if first < second:
        return first
    return second

def evaluateExpr(operation, operand1, operand2, operandType): #* function that evaluates the expression
    
    if operandType == "numbr":
        operand1 = int(operand1)
        operand2 = int(operand2)
    elif operandType == "numbar":
        operand1 = float(operand1)
        operand2 = float(operand2)


    if operation == "SUM":
        return operand1 + operand2
    elif operation == "DIFF":
        return operand1 - operand2
    elif operation == "BIGGR":
        return larger(operand1, operand2)
    elif operation == "SMALLR":
        return smaller(operand1, operand2)
    elif operation == "PRODUKT":
        return operand1 * operand2
    elif operation == "QUOSHUNT":
        return operand1 / operand2
    elif operation == "MOD":
        return operand1 % operand2
    
    return [operand1, operation, operand2]

def boolean(substring, lexemes):
    operations = ["BOTH OF ", "EITHER OF ", "WON OF "] # AND, OR, XOR
    toEval = ""
    
    for operation in operations:
        boolean_regex = operation +  "(WIN|FAIL) AN (WIN|FAIL)"
        pattern = re.compile(boolean_regex)
        
        for match in pattern.finditer(substring):
            # evaluated_val = evaluateExpr(operation, match.group(1), match.group(2), "numbr")
            makeLexeme(operation, "Boolean Operator", lexemes)
            makeLexeme(match.group(1), "TROOF value", lexemes)
            makeLexeme("AN", "Operator Separator", lexemes)
            makeLexeme(match.group(2), "TROOF value", lexemes)
            # return evaluated_val
            return True

    return None

def comparison(substring, lexemes):
    operations = ["BOTH SAEM ", "DIFFRINT "]
    toEval = ""
    
    for operation in operations:
        boolean_regex = operation +  "(.*) AN (.*)" #! for now it takes anything as operands but should only be varident, numbr, numbar, or arithmetic
        pattern = re.compile(boolean_regex)
        
        for match in pattern.finditer(substring):
            # evaluated_val = evaluateExpr(operation, match.group(1), match.group(2), "numbr")
            makeLexeme(operation, "Comparison Operator", lexemes)
            makeLexeme(match.group(1), "Operand", lexemes)
            makeLexeme("AN", "Operator Separator", lexemes)
            makeLexeme(match.group(2), "Operand", lexemes)
            # return evaluated_val
            return True

    return None

def isLiteral(substring, lexemes):
    if re.match("^-?[0-9][0-9]*$", substring):
        tempLexeme = Lexeme(substring)
        tempLexeme.setType("NUMBR")
        tempLexeme.export(lexAndSymbolTables)
        lexemes.append(tempLexeme)

    elif re.match("^-?[0-9]+\.[0-9]+$", substring):
        tempLexeme = Lexeme(substring)
        tempLexeme.setType("NUMBAR")
        lexemes.append(tempLexeme)
    elif re.match('([^\\"]|\\")', substring): 
        #still wrong
        # tempLexeme = Lexeme(substring)
        # tempLexeme.setType("YARN")
        # lexemes.append(tempLexeme)

        makeLexeme(substring,"YARN",lexemes)
    elif re.match("^WIN$|^FAIL$", substring):
        tempLexeme = Lexeme(substring)
        tempLexeme.setType("TROOF")
        lexemes.append(tempLexeme)
    elif re.match("^NUMBR$|^NUMBAR$| ^YARN$|^TROOF$", substring):
        tempLexeme = Lexeme(substring)
        tempLexeme.setType("TYPE LITERAL")
        lexemes.append(tempLexeme)
    else:
        return False
    return True

def isVardec(code):
    if re.match("^I HAS A", code):
        return True
    return False

def isVarident(substring):
    if re.match("^[a-z][a-zA-Z0-9_]*", substring):
        return True
    return False

def isVarinit(substring, lexemes):
    #Substring[0] is varident
    #Substring[1] is ITZ
    #Substring[2] nested if
    makeLexeme(substring[1],"Variable Assignment",lexemes)
    if isLiteral(substring[2], lexemes):
        return True
    elif isExpr(substring[2]):
        return True
    elif isVarident(substring[2]):
        return True
    else:
        return False




# * ---------------------------------------------------------------------------------------------------- GENERAL FXNS
def makeLexeme(mismo,type,lexemes): #* function that constructs a lexeme object for a passed string
    tempLexeme = Lexeme(mismo)
    tempLexeme.setType(type)
    lexemes.append(tempLexeme)
    tempLexeme.export(lexAndSymbolTables)
    
def analyzeKeyword(word, keywords, literals, identifiers, operations, lexemes):
    print("CHECKING:", word)

    if word == "":
        return True

    for keyword in keywords.keys():
        if re.match(keyword, word):
            if word == "WTF?":
                raw_string = r"{}".format(word)
                print(raw_string)
            makeLexeme(word, keywords[keyword], lexemes)
            return True
    
    for literal in literals.keys():
        if re.match(literal, word):
            makeLexeme(word, literals[literal], lexemes)
            return True
    
    for identifier in identifiers.keys():
        if re.match(identifier, word):
            # ! print("IDENTIFIER FOUND! WE SHOULD CHECK SYMBOL TABLE!")
            makeLexeme(word, identifiers[identifier], lexemes)
            return True

    for operation in operations.keys():
        if re.match(operation, word):
            makeLexeme(word, operations[operation], lexemes)
            return True

    return False

def willBeExpectingIdentifier(word, keywords, literals, identifiers, operations, lexemes):
    if word == "I HAS A":
        return True, False, False
    elif word == "IM IN YR":
        return False, True, False
    elif word == "HOW IZ I":
        return False, False, True
    return False, False, False
    

def lexicalAnalysis():
    code = codeSelectAndDisplay.getCodeDisplay().get("1.0", "end") # get the code in the display
    
    keywords = theCode.getKeyWords()
    literals = theCode.getLiterals()
    identifiers = theCode.getIdentifiers()
    operations = theCode.getOperations()
    
    lexemes = theCode.getLexemes()
    
    #* flags
    stringDelimiterActive = False # when true, all characters are part of a string comment
    varInitActive = False # when true, all characters read will become a variable identifer
    loopInitActive = False # for loop identifier
    fxnInitActive = False # for function identifier
    single_line_comment = False # when true, all characters are part of a single line comment
    multi_line_comment = False # when true, all characters are part of a multi-line comment
    switch_case_active = False # ! if this is true, will collect all the cases in a switch case
 
    #* temporary holders
    multi_line_comment_actual = "" # temporary holder for a multi-line comment
    scanned_word = "" # temporary holder for a scanned word

    for character in code:
        if character == " " and not stringDelimiterActive and not single_line_comment and not multi_line_comment:
            print("<SPACE>")
            print(scanned_word)

            if re.match("^BTW$", scanned_word):
                single_line_comment = True

            if varInitActive or loopInitActive or fxnInitActive:
                if re.match("[a-z]+[a-zA-Z0-9_]+", scanned_word):
                    if varInitActive:
                        makeLexeme(scanned_word, "Variable Identifier", lexemes)
                        varInitActive = False
                    elif loopInitActive:
                        makeLexeme(scanned_word, "Loop Identifier", lexemes)
                        loopInitActive = False
                    elif fxnInitActive:
                        makeLexem(scanned_word, "Function Identifier", lexemes)
                        fxnInitActive = False
                    clear = True
            
            varInitActive, loopInitActive, fxnInitActive = willBeExpectingIdentifier(scanned_word, keywords, literals, identifiers, operations, lexemes)

            clear = analyzeKeyword(scanned_word, keywords, literals, identifiers, operations, lexemes)

            if clear:
                scanned_word = ""
            else:
                scanned_word = scanned_word + " "
                
        elif character == "\n" and not stringDelimiterActive and not multi_line_comment:
            print("<NEW LINE>")
            print(scanned_word)

            if re.match("^OBTW$", scanned_word): # because OBTW should be in a line of its own
                multi_line_comment = True


            if single_line_comment:
                makeLexeme(scanned_word, "Single Line Comment", lexemes)
                single_line_comment = False
                clear = True
            else:
                clear = analyzeKeyword(scanned_word, keywords, literals, identifiers, operations, lexemes)


            if clear:
                scanned_word = ""
            else:
                scanned_word = scanned_word + " "
        elif character == "\t" and not stringDelimiterActive and not single_line_comment and not multi_line_comment:
            print("<TAB>")
            print(scanned_word)
            clear = analyzeKeyword(scanned_word, keywords, literals, identifiers, operations, lexemes)
            if clear:
                scanned_word = ""
            else:
                scanned_word = scanned_word + " "
        elif character == "\"" and not stringDelimiterActive and not single_line_comment and not multi_line_comment: # opening of a string delimiter
            stringDelimiterActive = True
            makeLexeme(character, "String Delimiter", lexemes)
            scanned_word = ""
        elif character == "\"" and stringDelimiterActive and not single_line_comment and not multi_line_comment: # closing of a string delimiter
            makeLexeme(scanned_word, "YARN", lexemes)
            stringDelimiterActive = False
            makeLexeme(character,"String Delimiter", lexemes)
            scanned_word = ""
        elif (character == "\n" or character == " " or character == "\t") and multi_line_comment:
            if re.match("^TLDR$", scanned_word):
                makeLexeme(multi_line_comment_actual, "Multiline Comment", lexemes)
                makeLexeme(scanned_word, "Multi-Line Comment Delimiter", lexemes)
                multi_line_comment_actual = ""
                multi_line_comment = False
            else:
                multi_line_comment_actual = multi_line_comment_actual + character + scanned_word
            scanned_word = ""
        else:
            scanned_word = scanned_word + character


def executeCode(): #* function that executes the loaded code
    # print(codeSelectAndDisplay.getCodeDisplay().get("1.0","end"))
    terminal.setDisplay("Compiling...")
    lexicalAnalysis()

def readCode(filename): # * function that reads the code in the passed filename
    f = open(filename)
    # code = f.readlines() # read the code inside the text file
    code = f.read() # read the code inside the text file
    theCode.addCode(code) # add the code to the initialized object
    # theCode.showMe()
    codeSelectAndDisplay.setCodeDisplay(theCode.getCode())

def selectSourceCode(): 
    # make the dialog be strict in selecting files by only allowing .lol code to be selected
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.lol*"),("all files","*.*")))
    readCode(filename)

#* ---------------

# * initialize the objects for the program
codeSelectAndDisplay = SelectGUI() # create a GUI
theCode = SourceCode() # create an object for the input Source LOLCode
lexAndSymbolTables = TablesGUI() # create an object for the tables to be generated
terminal = TerminalGUI() # create an object for the "terminal"




window.mainloop()
