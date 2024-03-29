# print("LOLterpreter!")
from tkinter import * 
from tkinter import filedialog
from tkinter import ttk
import re

#* -- GUI INITIALIZATIONS --
window = Tk()
window.geometry("1200x750") #widthxheight
window.title("LOLTERPRETER")
    
#* -- CLASSES --
class SourceCode(): # * class for the source code
    # constructor
    def __init__(self):
        self.code = "" # initialize the holder for the entire code
        self.keywords = { # keywords for generating tokens
            "^HAI$": "Code Start Delimiter", 
            "^KTHXBYE$": "Code End Delimiter",
            "^BTW$":"Single Line Comment Delimiter",
            "^OBTW$":"Multiline Comment Delimiter",
            "^TLDR$":"Multi-Line Comment Delimiter", #Delimiters 
            "^I HAS A$":"Variable Declaration",
            "^ITZ$":"Variable Assignment",
            "^R$":"Assignment Operation Keyword", #IHAS A to R
            #^ "MAEK": "Explicit type-casting",
            "^AN$" : "Operand Separator",
            #^ "A": "Type cast helper",
            #^ "IS NOW A": "Type cast Specifier",
            "^VISIBLE$": "Output Keyword",
            "^GIMMEH$": "User input",  #MAEK to GIMMEH
            "^O RLY\?$": "IF-ELSE Statement Opening Delimiter",
            #!  "^OI$C": "Function Closing Delimiter", 
            "^YA RLY$": "IF TRUE delimiter",
            "^NO WAI$": "ELSE delimiter",
            "^MEBB$E" : "ELSE-IF delimeter", #O RLY to OIC,
            "^IT$" : "Implicit Variable",
            "^WTF\?$":"Switch Case Start Delimiter",
            "^OMG$": "Case Specifier",
            "^OMGWTF$": "Default Switch Case Specifier",
            "^GTFO$" : "Break Statement",
            "^OIC$" : "Switch Case/IF-ELSE End Delimiter",
            "^IM IN YR$": "Loop Opening Delimeter",
            "^UPPIN$": "Loop increment",
            "^NERFIN$":"Loop decrement",#WTF? to Nerfin
            "^YR$": "Loop Variable Specifier",
            "^TIL$":"FAIL Loop specifier",
            "^WILE$": "WIN Loop Specifier",
            "^IM OUTTA YR$": "Loop Closing Delimiter", #YR to IM OUTTA YR
            "^MKAY$" : "End of Boolean Statement"
        }
        self.literals = { # literals for tokens
            "\"": "String Delimiter",
            "^-?[0-9][0-9]*$" : "NUMBR Literal",
            "^-?[0-9]*\.[0-9]+$" : "NUMBAR Literal",
            "\".*\"": "YARN Literal",
            "^WIN$": "TROOF Literal",
            "^FAIL$":"TROOF Literal",
            "^NUMBR$":"TYPE Literal",
            "^NUMBAR$":"TYPE Literal",
            "^YARN$": "TYPE Literal",
            "^TROOF$": "TYPE Literal",
        }
        self.identifiers = { # since all regex's for identifiers are the same
            "[a-z]+[a-zA-Z0-9_]*": "Identifier", 
        }
        self.operations = {
            "^SUM OF$": "Addition Operator" , 
            "^DIFF OF$": "Subtraction Operator",  
            "^PRODUKT OF$": "Multiplication Operator", 
            "^QUOSHUNT OF$": "Division Operator", #Sum of to Quoshunt of
            "^MOD OF$": "Modulo Operator", 
            "^BIGGR OF$": "Maximum Operator", 
            "^SMALLR OF$": "Minimum Operator",  #MOD of to Smallr of
            "^BOTH OF$": "and operator", 
            "^EITHER OF$": "or operator",
            "^WON OF$": "XOR operator",
            "^NOT$": "Not operator",
            "^ANY OF$": "Infinite arity or operator", 
            "^ALL OF$": "Infinite arity and operator",  #! #Both of to ALL OF
            "^BOTH SAEM$": "Equal comparison",
            "^DIFFRINT$": "Not equal comparison",
            "^SMOOSH$": "Concatenation operator",  #BOTH SAEM to SMOOSH
        }

        self.lexemes=[] # token holder
        self.symbolTable = {}

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

    def printSymbolTable(self):
        table = self.symbolTable
        for keys, values in table.items():
            print("KEY-VALUE: ", keys, values)

class Lexeme(): # the token class
    def __init__(self,mismo):
        self.mismo=mismo
        self.type=None
        self.value= None

    def setType(self,type):
        self.type=type
    
    def export(self, lexAndSymbolTables): # display the lexeme to the lexemes table
        lexAndSymbolTables.populateLexTable(self.mismo, self.type)

    def getActual(self):
        return self.mismo

    def getType(self):
        return self.type
    
    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value
    
class Program(): # the root node for the entire program
    def __init__(self,lexemes,hai_lexeme,kthxbye_lexeme):
        self.HAI=hai_lexeme
        self.KTHXBYE=kthxbye_lexeme
        self.statement=list() # child node that will hold all the statements (statements = grouped lexemes)

    def lookAhead(self, lexemes): # method that groups the lexemes into statements since one line of code = one statement
        statementHolder = []
        multiline_comment_active = False
        for lexeme in lexemes:
            if lexeme.getType() == "Multiline Comment Delimiter" and not multiline_comment_active:
                multiline_comment_active = True
            elif lexeme.getType() == "Multi-Line Comment Delimiter" and multiline_comment_active:
                multiline_comment_active = False
                # continue
            elif lexeme.getType() != "Line Break" and not multiline_comment_active:
                statementHolder.append(lexeme)
            elif lexeme.getType() == "Line Break" and not multiline_comment_active:
                # statementHolder.append(lexeme)
                self.statement.append(statementHolder)
                statementHolder = []
            

    def getStatements(self):
        return self.statement

class Statement(): # the root node that will hold all the statements
    def __init__(self):
        #!
        self.boolObj = None
        self.compObj = None
        self.arithObj = None
        self.bool2Obj = None

        self.statements = [] # will hold the statement objects in proper order

    def lookAhead(self, statements): 
        # each element in statements is a list of lexemes/tokens (group)
        # method that checks the type of the first lexeme in each group
        # if it matches to a particular type, it will look ahead to the other lexemes in the same group to determine the syntax
        
        # * holders
        ifElseObj = None
        caseObj= None
        defaultObj= None
        ifClauseObject = None
        elseClauseObject = None
        switchCaseObject=None
        clauseListOfStatements = []
        caseListofStatements= []

        #! 
        boolObj = None
        compObj = None
        arithObj = None
        bool2Obj = None

        #* flags
        ifElseFlag = False
        ifClauseActive = False
        elseClauseActive = False
        switchCaseActive= False
        caseObjActive = False
        defaultObjActive= False
        for statement in statements:
            if statement == []:
                continue
            lexeme = statement[0] # get the first token in the "group"
            if lexeme.getType() == "Output Keyword" and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False and switchCaseActive == False and caseObjActive == False and defaultObjActive == False: #* PRINT
                printObj = Print()
                printObj.lookAhead(statement)
                self.statements.append(printObj)
            elif lexeme.getType() == "Variable Declaration" and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False and switchCaseActive == False and caseObjActive == False and defaultObjActive == False: #* VAR DEC
                vardecObj = Vardec()
                vardecObj.lookAhead(statement)
                self.statements.append(vardecObj)
            elif lexeme.getType() == "User input" and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False: #* GIMMEH
                inputObj = Input()
                inputObj.lookAhead(statement)
                self.statements.append(inputObj)
            elif lexeme.getType() in ["Variable Identifier", "Implicit Variable", "Identifier"] and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False: #* ASSIGNMENT
                assignObj = Assignment()
                assignObj.lookAhead(statement)
                self.statements.append(assignObj)
            elif lexeme.getType() == "Not operator" and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False and caseObjActive == False and defaultObjActive == False and switchCaseActive == False: #* UNARY OPERATOR
                unaryObj = Unary(lexeme)
                unaryObj.lookAhead(statement)
                self.statements.append(unaryObj)
            elif lexeme.getType() in ["and operator", "or operator", "XOR operator"] and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False and caseObjActive == False and defaultObjActive == False and switchCaseActive == False: #* BOOLEAN BOTH OF, EITHER OF, WON OF
                boolObj = Boolean(lexeme)
                boolObj.lookAhead(statement)
                self.statements.append(boolObj)
            elif lexeme.getType() in ["Equal comparison", "Not equal comparison"] and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False and caseObjActive == False and defaultObjActive == False and switchCaseActive == False: #* COMPARISON BOTH SAEM, DIFFRINT
                compObj = Comparison(lexeme)
                compObj.lookAhead(statement)
                self.statements.append(compObj)
            elif lexeme.getType() in ["Addition Operator", "Subtraction Operator", "Multiplication Operator", "Division Operator", "Modulo Operator", "Maximum Operator", "Minimum Operator"] and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False and caseObjActive == False and defaultObjActive == False and switchCaseActive == False: #* ARITHMETIC ADD, SUB, MULT, DIV, MOD, MAX, MIN
                arithObj = Arithmetic(lexeme)
                arithObj.lookAhead(statement)
                self.statements.append(arithObj)
            elif lexeme.getType() in ["Infinite arity or operator", "Infinite arity and operator"] and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False and caseObjActive == False and defaultObjActive == False and switchCaseActive == False: #* BOOLEAN 2 WITH INFINITE ARITY
                bool2Obj = Boolean2()
                bool2Obj.lookAhead(statement)
                self.statements.append(bool2Obj)
            elif lexeme.getType() == "IF-ELSE Statement Opening Delimiter" and ifClauseActive == False and elseClauseActive == False: #* IF STATEMENT
                ifElseObj = Ifelse(lexeme) # O RLY?
                ifElseFlag = True
            elif lexeme.getType() == "IF TRUE delimiter" and ifElseFlag and ifClauseActive == False and elseClauseActive == False: # * the true branch delimiter for if-else statement
                ifClauseObject = IfClause(lexeme) # YA RLY
                ifClauseActive = True
            elif ifClauseActive and ifElseFlag and elseClauseActive == False: # * codeblock inside true branch
                # collect all statements until a NO WAI is encountered
                if lexeme.getType() == "ELSE-IF delimiter":
                    # mebbe clause
                    pass
                elif lexeme.getType() == "ELSE delimiter": # NO WAI
                    # trigger some flags
                    ifClauseActive = False
                    elseClauseActive = True
                    # create a codeblock out of the collected statements inside the true branch of if
                    codeBlockObj = CodeBlock()
                    codeBlockObj.lookAhead(clauseListOfStatements)
                    # set the codeblock as the right operand of the ifClause object
                    ifClauseObject.setRightOperand(codeBlockObj)
                    # ifClause is complete so we set it as the attribute of the ifElseObj
                    ifElseObj.setIfClause(ifClauseObject)
                    # we create the elseClause object since a NO WAI is encountered
                    elseClauseObject = ElseClause(lexeme)
                    clauseListOfStatements = [] # clear the clauseListOfStatements holder
                else:
                    clauseListOfStatements.append(statement)
            elif elseClauseActive and ifElseFlag and ifClauseActive == False: # *  codeblock inside False/else branch
                if lexeme.getType() == "Switch Case/IF-ELSE End Delimiter": # end of the clause is encountered
                    # trigger some flags
                    ifElseFlag = False
                    elseClauseActive = False
                    # create a codeblock out of the collected statements inside the true branch of if
                    codeBlockObj = CodeBlock()
                    codeBlockObj.lookAhead(clauseListOfStatements)
                    # set the codeblock as the right operand of the ifClause object
                    elseClauseObject.setRightOperand(codeBlockObj)
                    # ifClause is complete so we set it as the attribute of the ifElseObj
                    ifElseObj.setElseClause(elseClauseObject)
                    ifElseObj.setOIC(lexeme)
                    self.statements.append(ifElseObj)
                    clauseListOfStatements = [] # clear the clauseListOfStatements holder
                else: 
                    clauseListOfStatements.append(statement)
            elif lexeme.getType() == "Switch Case Start Delimiter" and not switchCaseActive and not ifElseFlag and not ifClauseActive and not elseClauseActive: #* SWITCH CASE
                # encountered a switch case start so this triggers a flag
                switchCaseActive = True
                # create a switchCase Object
                switchCaseObject = SwitchCase(lexeme)

            elif switchCaseActive and lexeme.getType() in ["Case Specifier", "Default Switch Case Specifier"] and not caseObjActive and not defaultObjActive: #* CASES IN A SWITCH CASE
                if lexeme.getType() == "Case Specifier": # case
                    # a CASE is encountered, trigger some flags
                    caseObjActive = True
                    # create an object
                    caseObj = Case()
                    caseObj.lookAhead(statement) # assign the case keyword and the literal value for the case object
                elif lexeme.getType() == "Default Switch Case Specifier": # default case
                    # default case is encountered
                    defaultObj=DefaultCase(lexeme)
                    # trigger some flags
                    defaultObjActive = True
                    
            elif switchCaseActive and defaultObjActive and not caseObjActive and not ifElseFlag and not ifClauseActive and not elseClauseActive: #* end of a switch case
                if lexeme.getType() == "Switch Case/IF-ELSE End Delimiter":
                    # if the end delimiter of a switch case is encountered, 
                    # create a codeblock object that will contain the collected statements
                    codeBlockObj = CodeBlock()
                    codeBlockObj.lookAhead(caseListofStatements)
                    # connect the codeblock to the default case object
                    defaultObj.setCodeBlock(codeBlockObj)
                    # connect the default case to the switch case object
                    switchCaseObject.setDefaultCase(defaultObj)
                    switchCaseObject.setOIC(lexeme)
                    # trigger some flags
                    defaultObjActive = False
                    switchCaseActive = False
                    # clear the list of statements
                    caseListofStatements = []
                    # assign the completed switchCaseObject to the attribute of the statement
                    self.statements.append(switchCaseObject)
                else:
                    # collect the statements
                    caseListofStatements.append(statement)                

            elif switchCaseActive and caseObjActive and not ifElseFlag and not ifClauseActive and not elseClauseActive and not defaultObjActive: #* break statement in a case is encountered
                if lexeme.getType()=="Break Statement":
                    # if the delimiter for a case in a switch case is encountered
                    # we create a codeblock that will contain the statements
                    codeBlockObj = CodeBlock()
                    codeBlockObj.lookAhead(caseListofStatements)
                    # we connect the codeblock to the case object
                    caseObj.setCodeBlock(codeBlockObj) 
                    # we set the break statement to the case object as well
                    caseObj.setGTFO(lexeme)
                    caseObjActive = False
                    # we connect the case to the switch case object
                    switchCaseObject.setCase(caseObj) # we are appending the case codeblock to the list of case codeblocks attribute of the switchCaseObj
                    # clear the list of statements
                    caseListofStatements=[]
                else:
                    # collect the statements
                    caseListofStatements.append(statement)
            lexAndSymbolTables.symbolTable.delete(*lexAndSymbolTables.symbolTable.get_children())
            lexAndSymbolTables.populateSymbolTable(theCode.symbolTable)
            
    def getProcessedStatements(self):
        return self.statements

class Print(): #* VISIBLE
    def __init__(self):
        self.left_operand=None
        self.right_operand=[]  #may branch

    def lookAhead(self, statement):
        operandHolder = []
        for lexeme in statement:
            if lexeme.getType()=="Output Keyword":
                self.left_operand = lexeme
            else:
                operandHolder.append(lexeme)

        visibleOperandObj = VisibleOperand()
        visibleOperandObj.lookAhead(operandHolder)
        self.right_operand = visibleOperandObj

class VisibleOperand(): #* VISIBLE OPERAND
    def __init__(self):
        self.operand = []

    def lookAhead(self, listOfLexemes): 
        # * determine the type of operand
        string_delimiter_flag = False

        # flags
        arithmeticFlag = False
        booleanFlag = False
        boolean2Flag = False
        comparisonFlag = False

        #object holders
        arithObj = None
        boolObj = None
        bool2Obj = None
        compObj = None
        literalObj = None
        
        expr_holder = []
        for lexeme in listOfLexemes:
            if lexeme.getType()=="String Delimiter" and string_delimiter_flag == False and not arithmeticFlag and not booleanFlag and not comparisonFlag:
                string_delimiter_flag = True
                literalObj = Literal()
            elif lexeme.getType()=="String Delimiter" and string_delimiter_flag and not arithmeticFlag and not booleanFlag and not comparisonFlag:
                string_delimiter_flag = False
            elif string_delimiter_flag and not arithmeticFlag and not booleanFlag and not comparisonFlag: #* yarn encountered
                literalObj.setValue(lexeme)
                self.operand.append(literalObj)
            elif lexeme.getType() in ["TROOF Literal", "NUMBR Literal", "NUMBAR Literal", "TYPE Literal"] and not string_delimiter_flag and not arithmeticFlag and not booleanFlag and not comparisonFlag and not string_delimiter_flag: #* literal encountered
                literalObj = Literal()
                literalObj.setValue(lexeme)
                self.operand.append(literalObj)
            elif lexeme.getType() in ["Variable Identifier", "Identifier"] and not arithmeticFlag and not booleanFlag and not comparisonFlag and not string_delimiter_flag: #* varident encountered
                self.operand.append(lexeme)
            elif lexeme.getType() in ["Addition Operator", "Subtraction Operator", "Multiplication Operator", "Division Operator", "Modulo Operator", "Maximum Operator", "Minimum Operator"] and not arithmeticFlag and not booleanFlag and not comparisonFlag and not string_delimiter_flag: # * arithmetic
                arithmeticFlag = True
                arithObj = Arithmetic(lexeme)
                expr_holder.append(lexeme)
            elif lexeme.getType() in ["and operator", "or operator", "XOR operator"] and not arithmeticFlag and not booleanFlag and not comparisonFlag and not string_delimiter_flag: # * boolean
                booleanFlag = True
                boolObj = Boolean(lexeme)
                expr_holder.append(lexeme)
            elif lexeme.getType() in ["Equal comparison", "Not equal comparison"] and not arithmeticFlag and not booleanFlag and not comparisonFlag and not string_delimiter_flag: # * comparison
                comparisonFlag = True
                compObj = Comparison(lexeme)
                expr_holder.append(lexeme)
            elif lexeme.getType() == "Implicit Variable" and not arithmeticFlag and not booleanFlag and not comparisonFlag and not string_delimiter_flag: # * implicit variable
                # print("IT ENCOUNTERED")
                self.operand.append(lexeme)
            elif lexeme.getType() in ["Infinite arity or operator", "Infinite arity and operator"] and not arithmeticFlag and not booleanFlag and not comparisonFlag and not string_delimiter_flag: #* boolean with infinite arity 
                boolean2Flag = True
                bool2Obj = Boolean2(lexeme)
                expr_holder.append(lexeme)
            elif arithmeticFlag or booleanFlag or comparisonFlag or boolean2Flag and not string_delimiter_flag: 
                expr_holder.append(lexeme) #* collect the statements for an expr
            else:
                print("VISIBLE OPERAND ERROR!!!")
        
        #* create an object depending on the expr encountered
        if arithmeticFlag and not booleanFlag and not boolean2Flag and not comparisonFlag:
            arithObj.lookAhead(expr_holder)
            self.operand.append(arithObj)
            arithmeticFlag = False
        elif booleanFlag and not arithmeticFlag and not boolean2Flag and not comparisonFlag:
            boolObj.lookAhead(expr_holder)
            self.operand.append(boolObj)
            booleanFlag = False
        elif boolean2Flag and not arithmeticFlag and not booleanFlag and not comparisonFlag:
            bool2Obj.lookAhead(expr_holder)
            self.operand.append(bool2Obj)
            boolean2Flag = False
        elif comparisonFlag and not arithmeticFlag and not boolean2Flag and not booleanFlag:
            compObj.lookAhead(expr_holder)
            self.operand.append(compObj)
            comparisonFlag = False

class Literal(): #* LITERAL
    def __init__(self):
        self.literal=None

    def setValue(self, value):
        self.literal = value

class Vardec(): #* VARIABLE DECLARATION
    def __init__(self):
        self.left_operand=None # I HAS A
        self.varident = None
        self.varinit = None # Varinit object

    def lookAhead(self, statement):
        statementHolder = []
        varInitHolder = []

        varInitActive = False
        for lexeme in statement:
            if lexeme.getType()=="Variable Declaration": # I HAS A
                self.left_operand = lexeme
            # elif lexeme.getType() == "Variable Identifier":
            elif lexeme.getType() in ["Variable Identifier", "Identifier"] and varInitActive == False:
                self.varident = lexeme
                # add the declared varident to the symbol table
                theCode.symbolTable[lexeme.getActual()] = None 
            elif self.varident != None and self.left_operand != False and not varInitActive: # start of a var init
                varInitActive = True
                varInitHolder.append(lexeme)
            elif varInitActive:
                varInitHolder.append(lexeme)

        varInitObj = Varinit()
        varInitObj.lookAhead(varInitHolder) # if varInitHolder is empty, then the right operand of the varinit object will be None
        self.varinit = varInitObj
        varInitActive = False
        #update the symbol table again
        theCode.symbolTable[self.varident.getActual()] = getObjectValue(varInitObj.right_operand)
        # print("Var Declared: ", self.varident.getActual(), " : ", theCode.symbolTable[self.varident.getActual()])
        # theCode.printSymbolTable()
        
class Varinit(): #* VARIABLE INITIALIZATION
    def __init__(self):
        self.left_operand = None # ITZ
        self.right_operand = None

    def lookAhead(self, listOfLexemes): # ITZ operand
        literalObj = None
        exprObj = None
        expr_active = False
        expr_holder = []

        # flags
        stringFlag = False
        arithmeticFlag = False
        booleanFlag = False
        boolean2Flag = False
        comparisonFlag = False
        unaryFlag = False

        #object holders
        arithObj = None
        boolObj = None
        bool2Obj = None
        compObj = None
        unaryObj = None

        for lexeme in listOfLexemes:
            if lexeme.getType()=="Variable Assignment" and not stringFlag and not arithmeticFlag and not booleanFlag and not comparisonFlag and not boolean2Flag and not unaryFlag: # * ITZ
                self.left_operand = lexeme
            elif lexeme.getType() in ["TROOF Literal", "NUMBR Literal", "NUMBAR Literal", "TYPE Literal"] and not stringFlag and not arithmeticFlag and not booleanFlag and not comparisonFlag and not boolean2Flag and not unaryFlag: # * literal
                literalObj = Literal()
                literalObj.setValue(lexeme)
                self.right_operand = literalObj
            elif lexeme.getType() in ["Variable Identifier", "Identifier"] and not stringFlag and not arithmeticFlag and not booleanFlag and not comparisonFlag and not boolean2Flag and not unaryFlag: # * varident
                self.right_operand = lexeme
            elif lexeme.getType() == "String Delimiter" and not stringFlag and not arithmeticFlag and not booleanFlag and not comparisonFlag and not boolean2Flag and not unaryFlag: # * start of a string
                stringFlag = True # trigger flag
            elif stringFlag and lexeme.getType() != "String Delimiter" and not arithmeticFlag and not booleanFlag and not comparisonFlag and not boolean2Flag and not unaryFlag:
                # create a literal object for the string
                literalObj = Literal()
                literalObj.setValue(lexeme)
                self.right_operand = literalObj
            elif lexeme.getType() == "String Delimiter" and stringFlag and not arithmeticFlag and not booleanFlag and not comparisonFlag and not boolean2Flag and not unaryFlag:
                stringFlag = False # trigger a flag when the end delimiter of a string is encountered
            elif lexeme.getType() in ["Addition Operator", "Subtraction Operator", "Multiplication Operator", "Division Operator", "Modulo Operator", "Maximum Operator", "Minimum Operator"] and not arithmeticFlag and not booleanFlag and not comparisonFlag and not stringFlag and not boolean2Flag and not unaryFlag: # * arithmetic
                arithmeticFlag = True
                arithObj = Arithmetic(lexeme)
                expr_holder.append(lexeme)
            elif lexeme.getType() in ["and operator", "or operator", "XOR operator"] and not arithmeticFlag and not booleanFlag and not comparisonFlag and not stringFlag and not boolean2Flag and not unaryFlag: # * boolean
                booleanFlag = True
                boolObj = Boolean(lexeme)
                expr_holder.append(lexeme)
            elif lexeme.getType() in ["Equal comparison", "Not equal comparison"] and not arithmeticFlag and not booleanFlag and not comparisonFlag and not stringFlag and not boolean2Flag and not unaryFlag: # * comparison
                comparisonFlag = True
                compObj = Comparison(lexeme)
                expr_holder.append(lexeme)
            elif lexeme.getType() in ["Infinite arity or operator", "Infinite arity and operator"] and not arithmeticFlag and not booleanFlag and not comparisonFlag and not stringFlag and not boolean2Flag and not unaryFlag: # * boolean with infinite arity
                boolean2Flag = True
                bool2Obj = Boolean2(lexeme)
                expr_holder.append(lexeme)
            elif lexeme.getType() == "Not operator" and not arithmeticFlag and not booleanFlag and not comparisonFlag and not stringFlag and not boolean2Flag and not unaryFlag:
                #* unary operator
                unaryFlag = True
                unaryObj = Unary(lexeme)
                expr_holder.append(lexeme)
            elif arithmeticFlag or booleanFlag or comparisonFlag or boolean2Flag or unaryFlag and not stringFlag: 
                expr_holder.append(lexeme)

        # create the appropriate object depending on the expression encountered and then set it to the right operand
        if arithmeticFlag and not booleanFlag and not boolean2Flag and not comparisonFlag and not unaryFlag:
            arithObj.lookAhead(expr_holder)
            self.right_operand = arithObj
            arithmeticFlag = False
        elif booleanFlag and not arithmeticFlag and not boolean2Flag and not comparisonFlag and not unaryFlag:
            boolObj.lookAhead(expr_holder)
            self.right_operand = boolObj
            booleanFlag = False
        elif boolean2Flag and not arithmeticFlag and not booleanFlag and not comparisonFlag and not unaryFlag:
            bool2Obj.lookAhead(expr_holder)
            self.right_operand = bool2Obj
            boolean2Flag = False
        elif comparisonFlag and not arithmeticFlag and not boolean2Flag and not booleanFlag and not unaryFlag:
            compObj.lookAhead(expr_holder)
            self.right_operand = compObj
            comparisonFlag = False
        elif unaryFlag and not comparisonFlag and not arithmeticFlag and not boolean2Flag and not booleanFlag:
            unaryObj.lookAhead(expr_holder)
            self.right_operand = unaryObj
    
class Input(): #* INPUT/GIMMEH
    def __init__(self):
        self.gimmeh = None
        self.varident = None
    
    def lookAhead(self, statement):
        for lexeme in statement:
            if lexeme.getType() == "User input":
                self.gimmeh = lexeme
            elif lexeme.getType() in ["Variable Identifier", "Identifier"]:
                self.varident = lexeme

class Assignment(): # * ASSIGNMENT (VARIDENT R <VALUE>)
    def __init__(self):
        self.left_operand= None # VARIDENT or IT
        self.middle_operand= None # R
        self.right_operand= None  #typecast,varident,literal,expr,concatenation

    def lookAhead(self, statement):
        string_delimiter_flag = False

        # flags
        arithmeticFlag = False
        booleanFlag = False
        boolean2Flag = False
        comparisonFlag = False
        unaryFlag = False

        #object holders
        arithObj = None
        boolObj = None
        bool2Obj = None
        compObj = None
        literalObj = None
        unaryObj = None
        
        expr_holder = []

        for lexeme in statement:
            # print("LEXEME: ", lexeme.getActual(), lexeme.getType())
            if lexeme.getType()=="String Delimiter" and string_delimiter_flag == False and not arithmeticFlag and not booleanFlag and not comparisonFlag:
                string_delimiter_flag = True
                literalObj = Literal()
            elif lexeme.getType()=="String Delimiter" and string_delimiter_flag and not arithmeticFlag and not booleanFlag and not comparisonFlag:
                string_delimiter_flag = False
            elif string_delimiter_flag and not arithmeticFlag and not booleanFlag and not comparisonFlag: #* the yarn is found
                literalObj.setValue(lexeme)
                self.right_operand = literalObj
            elif lexeme.getType() in ["TROOF Literal", "NUMBR Literal", "NUMBAR Literal", "TYPE Literal"] and not string_delimiter_flag and not arithmeticFlag and not booleanFlag and not comparisonFlag: #* literal
                literalObj = Literal()
                literalObj.setValue(lexeme)
                self.right_operand = literalObj
            elif lexeme.getType() in ["Variable Identifier", "Identifier", "Implicit Variable"] and not arithmeticFlag and not booleanFlag and not comparisonFlag and self.left_operand == None: #* a varident is found and the left operand is not yet set
                self.left_operand = lexeme
            elif lexeme.getType() in ["Variable Identifier", "Identifier", "Implicit Variable"] and not arithmeticFlag and not booleanFlag and not comparisonFlag and self.left_operand != None: # * a varident is found and the left operand is set, so the right operand will be set this time
                self.right_operand = lexeme
            elif lexeme.getType() in ["Addition Operator", "Subtraction Operator", "Multiplication Operator", "Division Operator", "Modulo Operator", "Maximum Operator", "Minimum Operator"] and not arithmeticFlag and not booleanFlag and not comparisonFlag: # * arithmetic
                arithmeticFlag = True
                arithObj = Arithmetic(lexeme)
                expr_holder.append(lexeme)
            elif lexeme.getType() in ["and operator", "or operator", "XOR operator"] and not arithmeticFlag and not booleanFlag and not comparisonFlag: # * boolean
                booleanFlag = True
                boolObj = Boolean(lexeme)
                expr_holder.append(lexeme)
            elif lexeme.getType() in ["Equal comparison", "Not equal comparison"] and not arithmeticFlag and not booleanFlag and not comparisonFlag: # * comparison
                comparisonFlag = True
                compObj = Comparison(lexeme)
                expr_holder.append(lexeme)
            elif lexeme.getType() in ["Infinite arity or operator", "Infinite arity and operator"] and not arithmeticFlag and not booleanFlag and not comparisonFlag: # * boolean with infinite arity
                boolean2Flag = True
                bool2Obj = Boolean2(lexeme)
                expr_holder.append(lexeme)
            elif lexeme.getType() == "Not operator" and not arithmeticFlag and not booleanFlag and not comparisonFlag and not unaryFlag: #* unary operator
                unaryFlag = True
                unaryObj = Unary(lexeme)
                expr_holder.append(lexeme)
            elif arithmeticFlag or booleanFlag or comparisonFlag or boolean2Flag or unaryFlag and not string_delimiter_flag: 
                expr_holder.append(lexeme) #* collect the lexemes when one of the expr flag is activated
        
        #* process the collected tokens based on the expression that was encountered
        if arithmeticFlag and not booleanFlag and not boolean2Flag and not comparisonFlag:
            arithObj.lookAhead(expr_holder)
            self.right_operand = arithObj
            arithmeticFlag = False
        elif booleanFlag and not arithmeticFlag and not boolean2Flag and not comparisonFlag:
            boolObj.lookAhead(expr_holder)
            self.right_operand = boolObj
            booleanFlag = False
        elif boolean2Flag and not arithmeticFlag and not booleanFlag and not comparisonFlag:
            bool2Obj.lookAhead(expr_holder)
            self.right_operand = bool2Obj
            boolean2Flag = False
        elif comparisonFlag and not arithmeticFlag and not boolean2Flag and not booleanFlag:
            compObj.lookAhead(expr_holder)
            self.right_operand = compObj
            comparisonFlag = False
        elif unaryFlag and not comparisonFlag and not arithmeticFlag and not boolean2Flag and not booleanFlag:
            unaryObj.lookAhead(expr_holder)
            self.right_operand = unaryObj
            unaryFlag = False

        #* update the symbol table by setting the value of the left_operand with the value of the object at its right_operand
        theCode.symbolTable[self.left_operand.getActual()] = getObjectValue(self.right_operand)
        # theCode.printSymbolTable()
        # print("IN THE END: ", self.left_operand.getActual(), theCode.symbolTable[self.left_operand.getActual()])
            
class Ifelse(): #* IF ELSE 
    def __init__(self,orly_lexeme):
        self.ifcond=None
        self.orly = orly_lexeme # orly lexeme
        self.ifclause=None
        self.elseclause=None
        self.mebbeclause=None # ! coming soon
        self.oic=None

    def setIfClause(self, if_clause_object):
        self.ifclause = if_clause_object
    
    def setElseClause(self, else_clause_object):
        self.elseclause = else_clause_object

    def setOIC(self, oic_lexeme):
        self.oic = oic_lexeme

class IfClause(): #* IF CLAUSE (THE TRUE BRANCH)
    def __init__(self, ya_rly_lexeme):
        self.left_operand=ya_rly_lexeme
        self.right_operand=None  #Code Block

    def setRightOperand(self, codeBlock):
        self.right_operand = codeBlock

class ElseClause(): #* ELSE CLAUSE (THE FALSE BRANCH)
    def __init__(self,no_wai_lexeme):
        self.left_operand=no_wai_lexeme
        self.right_operand=None  #Code Block

    def setRightOperand(self, codeBlock):
        self.right_operand = codeBlock

class Boolean(): # * BOOLEAN WITH 2 OPERANDS
    def __init__(self, lexeme):
        self.booloperation1 = lexeme
        self.left_operand = None
        self.right_operand = None
        self.value = None

    def setLeftOperand(self, left_operand):
        # ! check if operand is valid
        self.left_operand = left_operand
    
    def setRightOperand(self, right_operand):
        # ! check if operand is valid
        self.right_operand = right_operand

    def setValue(self, value):
        self.value = value

    def lookAhead(self, statement):

        # * utilize a stack for constructing the expression and its operands
        # * and for easier evaluation
        stack = []

        # * iterate by starting from the end of the statement 
        for index in range(len(statement)-1, -1, -1):
            lexeme = statement[index]

            if lexeme.getType() in ["TROOF Literal", "Variable Identifier", "Identifier", "Implicit Variable"]: # * WIN/FAIL , VARIDENT
                stack.append(lexeme)
            elif lexeme.getType() in ["and operator", "or operator", "XOR operator"]: # AND OR XOR
                right_operand = stack.pop()
                left_operand = stack.pop()
                if len(stack) == 0 and index == 0: 
                    # * reached the end of statement
                    # * when an operation keyword is encountered, pop two values from the stack as it will become its operands
                    self.left_operand = left_operand
                    self.right_operand = right_operand
                    #* evalue the constructed expression
                    self.value = getBoolValue(lexeme, right_operand, left_operand)
                else: 
                    # * nested boolean
                    boolObj = Boolean(lexeme)
                    boolObj.setLeftOperand(left_operand)
                    boolObj.setRightOperand(right_operand)
                    #* evalue the constructed expression
                    boolObj.setValue(getBoolValue(lexeme, right_operand, left_operand))
                    stack.append(boolObj)
            elif lexeme.getType() == "Not operator": 
                # * when a unary is encountered
                operand = stack.pop()
                unaryObj = Unary(lexeme)
                unaryObj.setOperand(operand)
                unaryObj.setValue(getUnaryValue(lexeme, operand))
                stack.append(unaryObj)

class Boolean2(): #* BOOLEAN WITH INFINITE ARITY
    def __init__(self):
        self.boolop2 = None
        self.operands = None
        self.value = None

    def setOperand(self, operands):
        self.operands = operands

    def setValue(self, value):
        self.value = value

    def lookAhead(self, statement):

        # * stack will be used for evaluation and expr construction
        stack = []

        # * iteration starts from the end of the statement moving backwards
        for index in range(len(statement)-1, -1, -1):
            lexeme = statement[index]
            if lexeme.getType() in ["TROOF Literal", "Variable Identifier", "Identifier", "Implicit Variable"]: # * basic operand
                stack.append(lexeme)
            elif lexeme.getType() in ["Infinite arity or operator", "Infinite arity and operator"]: # * infinite arity operators is encountered
                self.boolop2 = lexeme # set the name of the operation
                if index == 0: # we reached the end of the statement
                    # * the oeprands will be the entire stack
                    self.operands = stack
                    # * evaluate
                    self.value = getBool2Value(lexeme, stack)
                else:
                    # * if nested infinite arity is encountered
                    bool2 = Boolean2()
                    bool2.setOperand(stack)
                    bool2.setValue(getBool2Value(lexeme, stack))
                    # * clear the stack
                    stack.clear()
                    stack.append(bool2)
            elif lexeme.getType() in ["and operator", "or operator", "XOR operator"]: 
                #*  AND OR XOR is encountered
                booleanObj = Boolean(lexeme)
                booleanObj.setRightOperand(stack.pop())
                booleanObj.setLeftOperand(stack.pop())
                stack.append(booleanObj)
            elif lexeme.getType() == "Not operator": 
                # * unary is encountered
                unaryObj = Unary(lexeme)
                unaryObj.setOperand(stack.pop())
                stack.append(unaryObj)
                
class Comparison(): #* COMPARISON
    def __init__(self, lexeme):
        #<compoperator> <operand> AN <operand> 
        #<compoperator> <operand> AN <operation2> <operand> AN <operand> 
        #<compoperator> <comparison> AN <comparison>
        
        self.compoperator=lexeme
        self.left_operand=None   
        self.right_operand=None
        self.value = None

    def setLeftOperand(self, left_operand):
        # ! check if operand is valid
        self.left_operand = left_operand
    
    def setRightOperand(self, right_operand):
        # ! check if operand is valid
        self.right_operand = right_operand

    def setValue(self, value):
        self.value = value

    def lookAhead(self, statement):
        
        #* utilize a stack for constructing the expr and evaluating the expr
        stack = []

        #* iterate starting from the end of the statement moving backwards
        for index in range(len(statement)-1, -1, -1):
            lexeme = statement[index]
            # print("LEXEME: ", lexeme.getActual(), lexeme.getType())
            if lexeme.getType() in ["NUMBR Literal", "NUMBAR Literal", "Variable Identifier", "Identifier", "Implicit Variable"]: #* literal
                stack.append(lexeme)
            elif lexeme.getType() in ["Addition Operator", "Subtraction Operator", "Multiplication Operator", "Division Operator"]: #* literal
                # * when an arithmetic operator is encountered, pop two from the stack and it will become its operands
                left_operand = stack.pop()
                right_operand = stack.pop()
                arithObj = Arithmetic(lexeme)
                arithObj.setLeftOperand(left_operand)
                arithObj.setRightOperand(right_operand)
                arithObj.setValue(getValue(lexeme, right_operand, left_operand))
                # * append the object to the stack
                stack.append(arithObj)
            elif lexeme.getType() in ["Maximum Operator", "Minimum Operator"]:
                # * when a min/max operator is encountered
                left_operand = stack.pop()
                right_operand = stack.pop()
                operation2Obj = Operation2(lexeme)
                operation2Obj.setLeftOperand(left_operand)
                operation2Obj.setRightOperand(right_operand)
                operation2Obj.setValue(getValue(lexeme, right_operand, left_operand))
                stack.append(operation2Obj)
            elif lexeme.getType() in ["Equal comparison", "Not equal comparison"]:
                #* when a comparison is found 
                left_operand = stack.pop()
                right_operand = stack.pop()
                if len(stack) == 0 and index == 0: # reached the end of statement
                    # print("empty stack detected")
                    self.left_operand = left_operand
                    self.right_operand = right_operand
                    self.value = getValue(lexeme, right_operand, left_operand)
                else: # nested comparison 
                    comparisonObj = Comparison(lexeme)
                    comparisonObj.setLeftOperand(left_operand)
                    comparisonObj.setRightOperand(right_operand)
                    comparisonObj.setValue(getValue(lexeme, left_operand, right_operand))
                    stack.append(comparisonObj)
     
class Arithmetic(): #* ARITHMETIC
    def __init__(self, operation):
        self.operation1 = operation
        self.left_operand= None
        self.right_operand= None
        self.value = None
    
    def setLeftOperand(self, left_operand):
        # ! check if operand is valid
        self.left_operand = left_operand
    
    def setRightOperand(self, right_operand):
        # ! check if operand is valid
        self.right_operand = right_operand
    
    def setValue(self, value):
        self.value = value

    def lookAhead(self, statement):
        stack = [] # * use a stack for constructing the expr and evaluating the expr
        value = None

        # * iterate starting from the end moving backwards
        for index in range(len(statement)-1, -1, -1):
            lexeme = statement[index]
            # print("LEXEME: ", lexeme.getActual(), lexeme.getType())
            if lexeme.getType() in ["NUMBR Literal", "NUMBAR Literal", "Variable Identifier", "Identifier", "Implicit Variable"]: #* literal/varident is encountered
                stack.append(lexeme)
            elif lexeme.getType() in ["Addition Operator", "Subtraction Operator", "Multiplication Operator", "Division Operator", "Maximum Operator", "Minimum Operator", "Modulo Operator"]: #* an arithmetic operation is encountered or a min/max operation
                left_operand = stack.pop()
                right_operand = stack.pop()

                if len(stack) == 0 and index == 0: # reached the end of statement
                    self.left_operand = left_operand
                    self.right_operand = right_operand
                    #* evaluate
                    self.value = getValue(lexeme, right_operand, left_operand)
                else: # nested arithmetic
                    arithObj = Arithmetic(lexeme)
                    arithObj.setLeftOperand(left_operand)
                    arithObj.setRightOperand(right_operand)
                    #* evaluate
                    arithObj.setValue(getValue(lexeme, right_operand, left_operand))
                    #* add to the stack since not yet the end
                    stack.append(arithObj)

class Operation2(): #* MIN/MAX OPERATION
    def __init__(self,lexeme):
        self.leaf_operand=lexeme
        self.left_operand = None
        self.right_operand = None

    def setValue(self, value):
        self.value = value

    def setLeftOperand(self,lexeme):
        #! check if operand is valid
        self.left_operand=lexeme

    def setRightOperand(self,lexeme):
        #! check if operand is valid
        self.right_operand=lexeme    

#! class MebbeClause

class SwitchCase(): #* SWITCH CASE
    def __init__(self,lexeme):
        self.left_operand=lexeme  #WTF
        self.right_operand=None #OIC
        self.case=[]        #list of cases OMG
        self.default=None  # default case OMGWTF
    
    def setCase(self,caseObj):
        self.case.append(caseObj)
    
    def setDefaultCase(self,caseObj):
        self.default=caseObj

    def setOIC(self,lexeme):
        self.right_operand=lexeme

class DefaultCase(): #* DEFAULT CASE IN A SWITCH CASE
    def __init__(self,lexeme):
        self.leaf_operand = lexeme
        self.codeblock = None

    def setCodeBlock(self,codeblock):
        self.codeblock=codeblock
    
class Case(): #* CASE IN A SWITCH CASE
    def __init__(self):
        self.leaf_operand=None
        self.literal=None
        self.codeblock=None
        self.middle_operand=None     #GTFO
        self.right_operand=None     #case

    def lookAhead(self,statement):
        for lexeme in statement:
            if lexeme.getType()== "Case Specifier":
                self.leaf_operand=lexeme
            elif lexeme.getType() in ["TROOF Literal", "NUMBR Literal", "NUMBAR Literal", "TYPE Literal"]:
                self.literal=lexeme
    def setGTFO(self,lexeme):
        self.middle_operand=lexeme

    def setCodeBlock(self,codeblock):
        self.codeblock=codeblock
    
class CodeBlock(): #* CODEBLOCK
    def __init__(self):
        self.statements = []
        #!
        self.boolObj = None
        self.compObj = None
        self.arithObj = None
        self.bool2Obj = None

    def lookAhead(self, statements): 
        # each element in statements is a list of lexemes/tokens (group)
        # method that checks the type of the first lexeme in each group
        # if it matches to a particular type, it will look ahead to the other lexemes in the same group to determine the syntax
        
        # * holders
        ifElseObj = None
        caseObj= None
        defaultObj= None
        ifClauseObject = None
        elseClauseObject = None
        switchCaseObject=None
        clauseListOfStatements = []
        caseListofStatements= []

        #! 
        boolObj = None
        compObj = None
        arithObj = None
        bool2Obj = None

        #* flags
        ifElseFlag = False
        ifClauseActive = False
        elseClauseActive = False
        switchCaseActive= False
        caseObjActive = False
        defaultObjActive= False
        for statement in statements:
            if statement == []:
                continue
            lexeme = statement[0] # get the first token in the "group"
            if lexeme.getType() == "Output Keyword" and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False and switchCaseActive == False and caseObjActive == False and defaultObjActive == False: #* PRINT
                printObj = Print()
                printObj.lookAhead(statement)
                # self.print = printObj #!
                self.statements.append(printObj)
                # self.print.append(statement)
            elif lexeme.getType() == "Variable Declaration" and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False and switchCaseActive == False and caseObjActive == False and defaultObjActive == False: #* VAR DEC
                vardecObj = Vardec()
                vardecObj.lookAhead(statement)
                # self.vardec = vardecObj #!
                self.statements.append(vardecObj)
            elif lexeme.getType() == "User input" and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False: #* GIMMEH
                inputObj = Input()
                inputObj.lookAhead(statement)
                # self.input = inputObj #!
                self.statements.append(inputObj)
            # elif lexeme.getType() == "Variable Identifier" and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False: #* ASSIGNMENT
            elif lexeme.getType() in ["Variable Identifier", "Implicit Variable", "Identifier"] and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False: #* ASSIGNMENT
                assignObj = Assignment()
                assignObj.lookAhead(statement)
                # self.assignment = assignObj #! INCLUDED THE IT R <LITERAL> ASSIGNMENT
                self.statements.append(assignObj)
            elif lexeme.getType() == "Not operator" and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False and caseObjActive == False and defaultObjActive == False and switchCaseActive == False: #* UNARY OPERATOR
                # print("FOUND UNARY")
                unaryObj = Unary(lexeme)
                unaryObj.lookAhead(statement)
                self.statements.append(unaryObj)
            elif lexeme.getType() in ["and operator", "or operator", "XOR operator"] and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False and caseObjActive == False and defaultObjActive == False and switchCaseActive == False: #* BOOLEAN BOTH OF, EITHER OF, WON OF
                boolObj = Boolean(lexeme)
                boolObj.lookAhead(statement)
                self.statements.append(boolObj)
            elif lexeme.getType() in ["Equal comparison", "Not equal comparison"] and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False and caseObjActive == False and defaultObjActive == False and switchCaseActive == False: #* COMPARISON BOTH SAEM, DIFFRINT
                compObj = Comparison(lexeme)
                compObj.lookAhead(statement)
                self.statements.append(compObj)
            elif lexeme.getType() in ["Addition Operator", "Subtraction Operator", "Multiplication Operator", "Division Operator", "Modulo Operator", "Maximum Operator", "Minimum Operator"] and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False and caseObjActive == False and defaultObjActive == False and switchCaseActive == False: #* ARITHMETIC ADD, SUB, MULT, DIV, MOD, MAX, MIN
                arithObj = Arithmetic(lexeme)
                arithObj.lookAhead(statement)
                self.statements.append(arithObj)
            elif lexeme.getType() in ["Infinite arity or operator", "Infinite arity and operator"] and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False and caseObjActive == False and defaultObjActive == False and switchCaseActive == False: #* BOOLEAN 2 WITH INFINITE ARITY
                bool2Obj = Boolean2()
                bool2Obj.lookAhead(statement)
                self.statements.append(bool2Obj)
            elif lexeme.getType() == "IF-ELSE Statement Opening Delimiter" and ifClauseActive == False and elseClauseActive == False: #* IF STATEMENT
                ifElseObj = Ifelse(lexeme) # O RLY?
                ifElseFlag = True
            elif lexeme.getType() == "IF TRUE delimiter" and ifElseFlag and ifClauseActive == False and elseClauseActive == False: # * the true branch delimiter for if-else statement
                ifClauseObject = IfClause(lexeme) # YA RLY
                ifClauseActive = True
            elif ifClauseActive and ifElseFlag and elseClauseActive == False: # * codeblock inside true branch
                # collect all statements until a NO WAI is encountered
                if lexeme.getType() == "ELSE-IF delimiter":
                    # mebbe clause
                    pass
                elif lexeme.getType() == "ELSE delimiter": # NO WAI
                    # trigger some flags
                    ifClauseActive = False
                    elseClauseActive = True
                    # create a codeblock out of the collected statements inside the true branch of if
                    codeBlockObj = CodeBlock()
                    codeBlockObj.lookAhead(clauseListOfStatements)
                    # set the codeblock as the right operand of the ifClause object
                    ifClauseObject.setRightOperand(codeBlockObj)
                    # ifClause is complete so we set it as the attribute of the ifElseObj
                    ifElseObj.setIfClause(ifClauseObject)
                    # we create the elseClause object since a NO WAI is encountered
                    elseClauseObject = ElseClause(lexeme)
                    clauseListOfStatements = [] # clear the clauseListOfStatements holder
                else:
                    clauseListOfStatements.append(statement)
            elif elseClauseActive and ifElseFlag and ifClauseActive == False: # *  codeblock inside False/else branch
                if lexeme.getType() == "Switch Case/IF-ELSE End Delimiter": # end of the clause is encountered
                    # trigger some flags
                    ifElseFlag = False
                    elseClauseActive = False
                    # create a codeblock out of the collected statements inside the true branch of if
                    codeBlockObj = CodeBlock()
                    codeBlockObj.lookAhead(clauseListOfStatements)
                    # set the codeblock as the right operand of the ifClause object
                    elseClauseObject.setRightOperand(codeBlockObj)
                    # ifClause is complete so we set it as the attribute of the ifElseObj
                    ifElseObj.setElseClause(elseClauseObject)
                    ifElseObj.setOIC(lexeme)
                    # self.ifelse = ifElseObj #!
                    self.statements.append(ifElseObj)
                    clauseListOfStatements = [] # clear the clauseListOfStatements holder
                else: 
                    clauseListOfStatements.append(statement)
            elif lexeme.getType() == "Switch Case Start Delimiter" and not switchCaseActive and not ifElseFlag and not ifClauseActive and not elseClauseActive: #* SWITCH CASE
                # encountered a switch case start so this triggers a flag
                switchCaseActive = True
                # create a switchCase Object
                switchCaseObject = SwitchCase(lexeme)

            elif switchCaseActive and lexeme.getType() in ["Case Specifier", "Default Switch Case Specifier"] and not caseObjActive and not defaultObjActive: #* CASES IN A SWITCH CASE
                if lexeme.getType() == "Case Specifier": # case
                    # a CASE is encountered, trigger some flags
                    caseObjActive = True
                    # create an object
                    caseObj = Case()
                    caseObj.lookAhead(statement) # assign the case keyword and the literal value for the case object
                elif lexeme.getType() == "Default Switch Case Specifier": # default case
                    # default case is encountered
                    defaultObj=DefaultCase(lexeme)
                    # trigger some flags
                    defaultObjActive = True
                    
            elif switchCaseActive and defaultObjActive and not caseObjActive and not ifElseFlag and not ifClauseActive and not elseClauseActive: #* end of a switch case
                if lexeme.getType() == "Switch Case/IF-ELSE End Delimiter":
                    # if the end delimiter of a switch case is encountered, 
                    # create a codeblock object that will contain the collected statements
                    codeBlockObj = CodeBlock()
                    codeBlockObj.lookAhead(caseListofStatements)
                    # connect the codeblock to the default case object
                    defaultObj.setCodeBlock(codeBlockObj)
                    # connect the default case to the switch case object
                    switchCaseObject.setDefaultCase(defaultObj)
                    switchCaseObject.setOIC(lexeme)
                    # trigger some flags
                    defaultObjActive = False
                    switchCaseActive = False
                    # clear the list of statements
                    caseListofStatements = []
                    # assign the completed switchCaseObject to the attribute of the statement
                    # self.switchcase = switchCaseObject #!
                    self.statements.append(switchCaseObject)
                else:
                    # collect the statements
                    caseListofStatements.append(statement)                

            elif switchCaseActive and caseObjActive and not ifElseFlag and not ifClauseActive and not elseClauseActive and not defaultObjActive: #* break statement in a case is encountered
                if lexeme.getType()=="Break Statement":
                    # if the delimiter for a case in a switch case is encountered
                    # we create a codeblock that will contain the statements
                    codeBlockObj = CodeBlock()
                    codeBlockObj.lookAhead(caseListofStatements)
                    # we connect the codeblock to the case object
                    caseObj.setCodeBlock(codeBlockObj) 
                    # we set the break statement to the case object as well
                    caseObj.setGTFO(lexeme)
                    caseObjActive = False
                    # we connect the case to the switch case object
                    switchCaseObject.setCase(caseObj) # we are appending the case codeblock to the list of case codeblocks attribute of the switchCaseObj
                    # clear the list of statements
                    caseListofStatements=[]
                else:
                    # collect the statements
                    caseListofStatements.append(statement)
            
    def getProcessedStatements(self):
        return self.statements

class Unary(): # * UNARY
    def __init__(self, lexeme):
        self.unary_opt = lexeme
        self.operand = None
        self.value = None

    def setOperand(self, operand):
        self.operand = operand

    def setValue(self, value):
        self.value = value

    def lookAhead(self, statement):

        stack = [] #*  for constructing and evaluating expr

        for index in range(len(statement)-1, -1, -1):
            lexeme = statement[index]

            if lexeme.getType() in ["TROOF Literal", "Variable Identifier", "Identifier"]: # *WIN/FAIL , VARIDENT
                stack.append(lexeme)
            elif lexeme.getType() in ["and operator", "or operator", "XOR operator"]: # * AND OR XOR
                right_operand = stack.pop()
                left_operand = stack.pop()
                boolObj = Boolean(lexeme)
                boolObj.setLeftOperand(left_operand)
                boolObj.setRightOperand(right_operand)
                # * evaluate
                boolObj.setValue(getBoolValue(lexeme, right_operand, left_operand))
                stack.append(boolObj)
            elif lexeme.getType() == "Not operator": # * NOT
                operand = stack.pop()
                if len(stack) == 0 and index == 0: # * reached the end of statement
                    self.operand = operand
                    # * evaluate
                    self.value = getUnaryValue(lexeme, self.operand)
                else: # * nested unary 
                    unaryObj = Unary(lexeme)
                    unaryObj.setOperand(operand)
                    # * evaluate
                    unaryObj.setValue(getUnaryValue(lexeme, operand))
                    # * add to stack
                    stack.append(unaryObj)

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

    # def populateSymbolTable(self, word, value):
        # self.lexTable.insert("", "end", values=(str(word), str(value)))

    def populateSymbolTable(self, symbolTableDictionary):

        for key,value in symbolTableDictionary.items():
            # print(key, " : ", value)
            self.symbolTable.insert("", "end", value=(key, value))

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

    def addToDisplay(self, code):
        self.codeOutput.config(state=NORMAL)
        self.codeOutput.insert(END, code)
        self.codeOutput.insert(END, " ")
        self.codeOutput.config(state=DISABLED)

    def clear(self):
        self.codeOutput.config(state=NORMAL)
        self.codeOutput.delete("1.0", "end")
        self.codeOutput.config(state=DISABLED)
        
#* -------------

#* -- FUNCTIONS --
# * ---------------------------------------------------------------------------------------------------- LEXICAL ANALYSIS
def makeLexeme(mismo,lex_type,lexemes): #* function that constructs a lexeme object for a passed string

    if lex_type == "Variable Identifier": # update the symbol table
        theCode.symbolTable[mismo] = None

    tempLexeme = Lexeme(mismo) # mismong string
    tempLexeme.setType(lex_type) # type of lexeme
    lexemes.append(tempLexeme)
    tempLexeme.export(lexAndSymbolTables) # add the lexeme to the table in the GUI
    
def analyzeKeyword(word, keywords, literals, identifiers, operations, lexemes): #* function that analyzes the word passed to it by comparing it with the regex's in theCode
    # print("CHECKING:", word)

    if word == "":
        return True

    for keyword in keywords.keys():
        if re.match(keyword, word):
            if word == "WTF?":
                raw_string = r"{}".format(word)
            makeLexeme(word, keywords[keyword], lexemes)
            return True
    
    for literal in literals.keys():
        if re.match(literal, word):
            makeLexeme(word, literals[literal], lexemes)
            return True
    
    for identifier in identifiers.keys():
        if re.match(identifier, word):
            makeLexeme(word, identifiers[identifier], lexemes)
            return True

    for operation in operations.keys():
        if re.match(operation, word):
            makeLexeme(word, operations[operation], lexemes)
            return True

    return False

def willBeExpectingIdentifier(word, keywords, literals, identifiers, operations, lexemes): # * when a keyword is found that expects an identifer to follow
    # if word == "I HAS A":
    if re.match("^I HAS A$", word):
        return True, False, False
    # elif word == "IM IN YR":
    elif re.match("^IM IN YR$", word):
        return False, True, False
    # elif word == "HOW IZ I":
    elif re.match("^HOW IZ I?$", word):
        return False, False, True
    return False, False, False
    
def lexicalAnalysis(): #* LEXICAL ANALYSIS 
    print("LEXICAL ANALYSIS")
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
 
    #* temporary holders
    multi_line_comment_actual = "" # temporary holder for a multi-line comment
    scanned_word = "" # temporary holder for a scanned word

    for character in code: # iterate through every character in the source code
        if character == " " and not stringDelimiterActive and not single_line_comment and not multi_line_comment:
            # print("<SPACE>")
            # print(scanned_word)

            if re.match("^BTW$", scanned_word):
                single_line_comment = True

            if varInitActive or loopInitActive or fxnInitActive:
                if re.match("[a-z]+[a-zA-Z0-9_]*", scanned_word):
                # if re.match("[a-z]+[a-zA-Z0-9_]+", scanned_word):
                    if varInitActive:
                        makeLexeme(scanned_word, "Variable Identifier", lexemes)
                        varInitActive = False
                    elif loopInitActive:
                        makeLexeme(scanned_word, "Loop Identifier", lexemes)
                        loopInitActive = False
                    elif fxnInitActive:
                        makeLexeme(scanned_word, "Function Identifier", lexemes)
                        fxnInitActive = False
                    clear = True
            
            varInitActive, loopInitActive, fxnInitActive = willBeExpectingIdentifier(scanned_word, keywords, literals, identifiers, operations, lexemes)

            clear = analyzeKeyword(scanned_word, keywords, literals, identifiers, operations, lexemes)

            if clear:
                scanned_word = ""
            else:
                scanned_word = scanned_word + " "
                
        elif character == "\n" and not stringDelimiterActive and not multi_line_comment:
            # print("<NEW LINE>")
            # print(scanned_word)

            if varInitActive or loopInitActive or fxnInitActive: # in cases of declared but not initialized
                if re.match("[a-z]+[a-zA-Z0-9_]*", scanned_word):
                # if re.match("[a-z]+[a-zA-Z0-9_]+", scanned_word):
                    if varInitActive:
                        makeLexeme(scanned_word, "Variable Identifier", lexemes)
                        varInitActive = False
                    elif loopInitActive:
                        makeLexeme(scanned_word, "Loop Identifier", lexemes)
                        loopInitActive = False
                    elif fxnInitActive:
                        makeLexeme(scanned_word, "Function Identifier", lexemes)
                        fxnInitActive = False
                    clear = True

            if re.match("^OBTW$", scanned_word): # because OBTW should be in a line of its own
                multi_line_comment = True


            if single_line_comment:
                makeLexeme(scanned_word, "Single Line Comment", lexemes)
                single_line_comment = False
                clear = True
            else:
                clear = analyzeKeyword(scanned_word, keywords, literals, identifiers, operations, lexemes)
            
            makeLexeme("\\n", "Line Break", lexemes)


            if clear:
                scanned_word = ""
            else:
                scanned_word = scanned_word + " "
        elif character == "\t" and not stringDelimiterActive and not single_line_comment and not multi_line_comment:
            # print("<TAB>")
            # print(scanned_word)
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
    
    lexAndSymbolTables.populateSymbolTable(theCode.symbolTable)

# * ---------------------------------------------------------------------------------------------------------------------
# * ------------------------------------------------------------------------------------------------------SYNTAX ANALYSIS
def syntaxAnalysis(): # * SYNTAX ANALYSIS
    print("SYNTAX ANALYSIS")
    lexemes = theCode.getLexemes()

    startFlag = False
    endFlag = False
    indexOfStartCode = 0
    indexOfEndCode = 0
    index = 0 

    # look for code delimiters first
    for lexeme in lexemes:
        # print("LEXEME: ", lexeme.mismo, "->", lexeme.type)
        if lexeme.getType() == "Code Start Delimiter":
            indexOfStartCode = index
            startFlag = True
            print("START OF PROGRAM FOUND!")
        elif lexeme.getType() == "Code End Delimiter":
            endFlag = True
            indexOfEndCode = index
            print("END OF PROGRAM FOUND!")
            break 
        index = index + 1

    # create program object and loop through statements between the code delimiters
    if startFlag and endFlag:
        hai_lexeme = lexemes.pop(indexOfStartCode)
        kthxbye_lexeme = lexemes.pop(indexOfEndCode)
        # print("CODE DELIMITERS")
        # print(hai_lexeme)
        # print(kthxbye_lexeme)
        # print("CODE DELIMITERS")

        #* create the root for the program
        programRoot = Program(lexemes, hai_lexeme, kthxbye_lexeme)
        programRoot.lookAhead(lexemes)

        #* get the statements child of the program root and set it as the root of all the other statements
        statements = programRoot.getStatements()
        statementRoot = Statement()
        statementRoot.lookAhead(statements)
        # print(statementRoot.switchcase)

        return programRoot, statementRoot

# * ---------------------------------------------------------------------------------------------------------------------
# * ------------------------------------------------------------------------------------------------------SEMANTIC ANALYSIS
def semanticAnalysis(statements): #* SEMANTIC ANALYSIS
    print("Semantic Analysis", len(statements))

    #* print the statements 
    for statement in statements:
        print(statement)

    for statement in statements:
        if isinstance(statement, Print): # * encountered a print object
            # check if right_operand is valid
            if isinstance(statement.right_operand, VisibleOperand):
                visible_operand = statement.right_operand
                # print("PRINT DAPAT: ",visible_operand.operand)
                for operand in visible_operand.operand: # iterate through every operand in the visible operand
                # determine what type the operand is
                    if isinstance(operand, Literal):
                        terminal.addToDisplay(operand.literal.getActual())
                    elif isinstance(operand, Arithmetic) or isinstance(operand, Boolean) or isinstance(operand, Comparison):
                        # print(operand)
                        # print(operand.value)
                        terminal.addToDisplay(operand.value)
                    elif operand.getType() in ["Identifier", "Implicit Variable"]:
                        # REFER TO ITS VALUE IN THE SYMBOL TABLE
                        # print(operand.getType())
                        displayMe = theCode.symbolTable[operand.getActual()]
                        # print(displayMe)
                        terminal.addToDisplay(displayMe)
                terminal.addToDisplay("\n")
            else: 
                print("INVALID VISIBLE OPERAND!!")
                # TODO : throw an error, invalid visible operand
        elif isinstance(statement, Vardec): # *  encountered a variable declaration object
            if statement.varident != None:
                # print(statement.varident, " -> ", statement.varinit.right_operand)
                if statement.varinit.left_operand != None:
                    # check if a var init was encountered during var dec synax analysis
                    value = getObjectValue(statement.varinit.right_operand)
                    print("VARDEC ITZ: ", value)
                    theCode.symbolTable[statement.varident.getActual()] = value
            else:
                # TODO : throw an error, invalid varident
                print("No varident! Error!")
        elif isinstance(statement, Arithmetic) or isinstance(statement, Boolean) or isinstance(statement, Comparison) or isinstance(statement, Unary) or isinstance(statement, Boolean2): #* encountered an arithmetic, boolean, comparison object

            value = getObjectValue(statement)
            if value == None:
                print("Error in evaluating the expr")
            else:
                print("RANJIT", value)
                theCode.symbolTable["IT"] = value
        elif isinstance(statement, Assignment): #* encountered an assignment statement
            # print("assignment encountered")
            # simply assign the value at the right operand of the object with the left operand as the key
            theCode.symbolTable[statement.left_operand.getActual()] = getObjectValue(statement.right_operand)
            # theCode.printSymbolTable()
        elif isinstance(statement, Ifelse): #* encountered an if else statement
            # print("encountered if else statement")
            # print(theCode.symbolTable["IT"])
            # determine which path to take
            if theCode.symbolTable["IT"] == "WIN":
                # print("TRUE BRANCH", statement.ifclause)
                semanticAnalysis(statement.ifclause.right_operand.getProcessedStatements())
            elif theCode.symbolTable["IT"] == "FAIL":
                # print("FALSE BRANCH", statement.elseclause)
                semanticAnalysis(statement.elseclause.right_operand.getProcessedStatements())
        elif isinstance(statement, SwitchCase): #* encountered a switch case
            # print("encountered switch statement")
            itVar = theCode.symbolTable["IT"]
            cases = statement.case
            foundCaseFlag = False
            # determine the right path to take
            # compare the value of the implicit variable to every case in switchcase object
            # if found a case/ reached default case, semanticAnalysis(codeBlock)
            for case in cases:
                # print("CASE: ",case.literal.getActual())
                if case.literal.getActual() == itVar:
                    # print("MATCHED WITH", case.literal.getActual(), case.codeblock.getProcessedStatements())
                    foundCaseFlag = True
                    semanticAnalysis(case.codeblock.getProcessedStatements())
                    break
            
            if not foundCaseFlag:
                # print("NO MATCH FOUND", statement.default.codeblock.getProcessedStatements())
                semanticAnalysis(statement.default.codeblock.getProcessedStatements())
                # semanticAnalysis(case.)
        elif isinstance(statement, Input): #* encountered a GIMMEH
            input = getInput()
            # update the symbol table with the input of the user
            theCode.symbolTable[statement.varident.getActual()] = input
            # print(theCode.symbolTable["IT"], statement)
        lexAndSymbolTables.symbolTable.delete(*lexAndSymbolTables.symbolTable.get_children())
        lexAndSymbolTables.populateSymbolTable(theCode.symbolTable)
        
# * -----------------------------------------------------------------------------------------------------------------------
def parse(operand): # * function that converts the value of a lexeme according to the type of that lexeme
    try: 
        if operand.getType() == "NUMBR Literal":
            return int(operand.getActual())
        elif operand.getType() == "NUMBAR Literal":
            return float(operand.getActual())
        elif operand.getType() in ["Variable Identifier", "Identifier", "Implicit Variable"]:
            # print("FR SYMBOL TABLE: ", theCode.symbolTable[operand.getActual()])
            # print("FR SYMBOL TABLE: ", operand.getActual())
            if re.match("^-?[0-9][0-9]*$", theCode.symbolTable[operand.getActual()]): # matched with a numbr literal
                return int(theCode.symbolTable[operand.getActual()])
            elif re.match("^-?[0-9]*\.[0-9]+$", theCode.symbolTable[operand.getActual()]): # matched with a numbar literal
                return float(theCode.symbolTable[operand.getActual()])
            elif theCode.symbolTable[operand.getActual()] == "WIN":
                return True
            elif theCode.symbolTable[operand.getActual()] == "FAIL":
                return False
            else:
                print("NOT A VALID IDENTIFIER VALUE!")
        else: 
            print("INVALID LITERAL IN PARSE", operand.getActual(), operand.getType())
    except: # an error will be thrown when instance is an object
    
        try: 

            return operand.value # in cases when the operand is an object and not a literal
        except: # in cases when it's neither a numbr/numbar literal or an object
            print("NOT AN OBJECT AND NOT A NUMBR, NUMBAR LITERAL")

def parseBool(operand): # * function that converts the value of a boolean lexeme according to the type of the lexeme
    try:
        if operand.getType() == "TROOF Literal":
            return True if operand.getActual() == "WIN" else False
        elif operand.getType() in ["Variable Identifier", "Identifier", "Implicit Variable"]:
            if theCode.symbolTable[operand.getActual()] == "WIN":
                return True
            elif theCode.symbolTable[operand.getActual()] == "FAIL":
                return False
            else:
                print("NOT A VALID IDENTIFIER VALUE!")
        else:
            print("INVALID LITERAL IN PARSE BOOL", operand.getActual(), operand.getType())
    except:
        try:
            if operand.value == "WIN":
                return True
            elif operand.value == "FAIL":
                return False
            else:
                return operand.value
        except:
            print("NOT AN OBJECT AND NOT A TROOF LITERAL")

def getBoolValue(lexeme, right, left): #* function that executes the boolean operation (2 operands)
    calc_right = parseBool(right)
    calc_left = parseBool(left)

    if lexeme.getType() == "and operator":
        value = calc_right and calc_left
        returnMe = "WIN" if value == True else "FAIL"
        return returnMe
    elif lexeme.getType() == "or operator":
        value = calc_right or calc_left
        returnMe = "WIN" if value == True else "FAIL"
        return returnMe
    elif lexeme.getType() == "XOR operator":
        value = calc_right ^ calc_left
        returnMe = "WIN" if value == True else "FAIL"
        return returnMe

def getBool2Value(lexeme, stack): #* function that executes the boolean operation with infinite arity
    # print(lexeme.getActual(), stack)
    andFlag = None
    orFlag = None
    if lexeme.getType() == "Infinite arity and operator":
        andFlag = True
    elif lexeme.getType() == "Infinite arity or operator":
        orFlag = True
    else:
        print("INVALID LEXEME VALUE IN BOOL 2")

    if andFlag:
        for operand in stack:
            #* if a FAIL is encounteted in infinite arity operation, then no need to continue, it will be FAIL anyway
            if getObjectValue(operand) == False or getObjectValue(operand) == "FAIL":
                return "FAIL"
        return "WIN"
    elif orFlag:
            #* if a WIN is encounteted in infinite arity operation, then no need to continue, it will be WIN anyway
        for operand in stack:
            if getObjectValue(operand) == True or getObjectValue(operand) == "WIN":
                return "WIN"
        return "FAIL"

def getValue(lexeme, right, left): # * function that executes the arithmetic, min/max, and comparison operation
    #* check if both operands have the same type
    calc_right = parse(right)
    calc_left = parse(left)

    if lexeme.getType() == "Addition Operator":
        return calc_right + calc_left
    elif lexeme.getType() == "Subtraction Operator":
        return calc_left - calc_right
    elif lexeme.getType() == "Multiplication Operator":
        return calc_right * calc_left
    elif lexeme.getType() == "Division Operator":
        try:
            return calc_left / calc_right
        except:
            return 0
    elif lexeme.getType() == "Modulo Operator":
        try:
            return calc_left % calc_right
        except:
            return 0
    elif lexeme.getType() == "Maximum Operator":
        returnMe = calc_left if calc_left > calc_right else calc_right
        return returnMe
    elif lexeme.getType() == "Minimum Operator":
        returnMe = calc_left if calc_left < calc_right else calc_right
        return returnMe
    elif lexeme.getType() == "Equal comparison":
        print(calc_left, " equal with ", calc_right)
        # print(type(calc_left), type(calc_right))
        if (type(calc_left) == type(calc_right)) and (calc_left == calc_right): 
            return "WIN"
        else:
            return "FAIL"
    elif lexeme.getType() == "Not equal comparison":
        print(calc_left, " diffrint with ", calc_right)
        if (type(calc_left) != type(calc_right)) or (calc_left != calc_right): 
            return "WIN"
        else:
            return "FAIL"

def getUnaryValue(lexeme, operand): #* function that executes the not operation
    calc_operand = parseBool(operand)

    if lexeme.getType() == "Not operator":
        # print("GET UNARY VALUE: ", calc_operand)
        return "WIN" if calc_operand == False else "FAIL"

def getObjectValue(obj_find): #* function that returns the value of an object

    if isinstance(obj_find, Literal):
        return obj_find.literal.getActual()
    elif isinstance(obj_find, Arithmetic) or isinstance(obj_find, Boolean) or isinstance(obj_find, Comparison) or isinstance(obj_find, Unary) or isinstance(obj_find, Boolean2):
        return obj_find.value
    elif isinstance(obj_find, Lexeme):

        if obj_find.getType() == "Identifier":
            # print("WAZZZAT ", theCode.symbolTable[obj_find.getActual()])
            return theCode.symbolTable[obj_find.getActual()]
        else:
            return obj_find.getActual() #!
    else:
        print("OBHECTN VALUE: ", obj_find)

def getInput(): #* function invoked when a GIMMEH is encountered
    
    userInput = StringVar()
    okBtnClicked = IntVar()
    
    # * create a pop up window to ask for the input from the user
    inputWindow = Toplevel()
    label = Label(inputWindow, text="INPUT: ", height = 2, width = 50)
    label.pack()
    inputGUI = Entry(inputWindow, textvariable=userInput)
    inputGUI.pack()
    okBtn = Button(inputWindow, text="OK", command=lambda: okBtnClicked.set(1))
    okBtn.pack()

    #* wait for the OK btn to be clicked... "pauses" the tkinter main loop
    okBtn.wait_variable(okBtnClicked)
    returnMe = inputGUI.get()

    if okBtnClicked.get() == 1:
        inputWindow.destroy()

    # return the value input of the user
    return returnMe

def executeCode(): #* function that executes the loaded code
    # print(codeSelectAndDisplay.getCodeDisplay().get("1.0","end"))
    # terminal.setDisplay("Compiling...")
    lexAndSymbolTables.lexTable.delete(*lexAndSymbolTables.lexTable.get_children())
    lexAndSymbolTables.symbolTable.delete(*lexAndSymbolTables.symbolTable.get_children())
    theCode.lexemes = []
    theCode.symbolTable = {}
    terminal.clear()
    lexicalAnalysis()
    programObj, statementsObj = syntaxAnalysis()
    semanticAnalysis(statementsObj.getProcessedStatements())

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
