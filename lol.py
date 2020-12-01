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
        self.keywords = {\
            "^HAI$": "Code Delimiter", 
            "^KTHXBYE$": "Code Delimiter",
            "^BTW$":"Comment",
            "^OBTW$":"Comment Delimiter",
            "^TLDR$":"Comment Delimiter", #Delimiters 
            "I HAS A":"Variable Declaration",
            "ITZ":"Variable Assignment",
            "R":"Assignment Operation Keyword", #IHAS A to R
            # "MAEK": "Explicit type-casting",
            # "A": "Type cast helper",
            # "IS NOW A": "Type cast Specifier",
            "VISIBLE": "Output Keyword",
            # "GIMMEH": "User input",  #MAEK to GIMMEH
            "O RLY": "Function Opening Delimiter",
            "OIC": "Function Closing Delimeter",
            "YA RLY": "if delimiter",
            "NO WAI": "else delimiter",
            "MEBBE" : "else-if delimeter", #O RLY to OIC
            "WTF?":"Case delimeter",
            "OMG": "Case Specifier",
            "OMGWTF": "Default Case Specifiier",
            "IM IN YR": "Loop Opening Delimeter",
            "UPPIN": "Loop increment",
            "Loop decrement":"",#WTF? to Nerfin
            "YR": "Loop Variable Specifier",
            "TIL":"FAIL Loop specifier",
            "WILE": "WIN Loop Specifier",
            "IM OUTTA YR": "Loop Closing Delimeter" #YR to IM OUTTA YR
        }
        self.literals = {
            "\"": "String Delimiter",
            "-?[0-9][0-9]+" : "NUMBR Literal",
            "-?[0-9]+\.[0-9]+" : "NUMBAR Literal",
            "\".*\"": "YARN Literal",
            "WIN": "TROOF LIteral",
            "FAIL":"TROOF Literal",
            "NUMBR":"TYPE Literal",
            "NUMBR": "TYPE Literal",
            "NUMBAR":"TYPE Literal",
            "YARN": "TYPE Literal",
            "TROOF": "TYPE Literal",  #Literals
        }
        self.identifiers = {
            "[^\"][a-z]+[a-zA-Z0-9_]+": "Variable Identifier", 
            "[^\"][a-z]+[a-zA-Z0-9]+": "Function Identifier",
             "[^\"][a-z]+[a-zA-Z0-9_]+": "Loop Identifier"
        }
        self.operations = {
            "SUM OF": "Addition Operator", 
            "DIFF OF": "Substraction Operator",
            "PRODUKT OF": "Multiplication Operator",
            "QUOSHUNT OF": "Division Operator", #Sum of to Quoshunt of
            "MOD OF": "Modulo Operator",
            "BIGGR OF": "Maximum Operator",
            "SMALLR OF": "Minimum Operator", #MOD of to Smallr of
            "BOTH OF": "and operator",
            "EITHER OF": "or operator",
            "WON OF": "XOR Operator",
            "NOT": "Not operator",
            "ANY OF": "Inifinite arity or operator",
            "ALL OF": "inifinite arity and operator", #Both of to ALL OF
            "BOTH SAEM": "Equal comparison Operator",
            "DIFFRNT": "Not equal comparison operator",
            "SMOOSH": "Concatenation operator",  #BOTH SAEM to SMOOSH
        }

    def addCode(self, code): # set the code for object
        self.code = code
    
    def getCode(self):
        return self.code

    def getKeyWords(self):
        return self.keywords

    def showMe(self):
        print("=====SOURCE CODE=====")
        print("THE CODE: ")
        print(self.code)
        print("---------------------")
        print("KEYWORDS")
        print(self.keywords)
        print("=====================")

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
        self.lexTable.insert("", "end", values=(str(word), classification))

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

def parser(code): #* function that generates the parse tree of the statements
    keywords = theCode.getKeyWords()
    # iterate thryoughj every element in code
    for lineOfCode in code:
        if re.match(keywords["^VISIBLE"], lineOfCode):
            checkGrammar(lineCode, "print")





def lexicalAnalysis(): #* function that generates the lexemes of the code in codeDisplay
    matchFlag = False
    code = codeSelectAndDisplay.getCodeDisplay().get("1.0", "end") # get the code in the display

    # print(code)
    code = code.replace("\t", "")
    code = code.split("\n")
    code.pop() # ! 
    print(code)

    lexTable = lexAndSymbolTables.getLexTable()

    if re.match("^HAI$", code[0]) and re.match("^KTHXBYE$", code[-1]):
        matchFlag = True
    
    if not matchFlag: 
        terminal.setDisplay("Error! Program not found!")
        return 0

    parser(code)
    # keywords = theCode.getKeyWords()

    

    # for word in code: # iterate through every word in the code 
    #     for keyword, classification in keywords.items(): # iterate through every keyword (and its classification) in the keywords dictionary
    #         pattern = re.compile(keyword) # compile the regex for the keyword/s
    #         for match in pattern.finditer(word): # find all matches in every line
                # lexAndSymbolTables.populateLexTable(match.group(), classification) # add the matches to the lexemes table




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
