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
            "^HAI$": "Code Start Delimiter", 
            "^KTHXBYE$": "Code End Delimiter",
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
            "^O RLY\?$": "IF-ELSE Statement Opening Delimiter",
            #!  "^OI$C": "Function Closing Delimiter", 
            "^YA RLY$": "IF TRUE delimiter",
            "^NO WAI$": "ELSE delimiter",
            "^MEBB$E" : "ELSE-IF delimeter", #O RLY to OIC,
            "^IT$" : "Implicit Variable",
            "^WTF\?$":"Switch Case Start Delimiter",
            "^OMG$": "Case Specifier",
            "^OMGWTF$": "Default Switch Case Specifiier",
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
        self.literals = {
            "\"": "String Delimiter",
            "^-?[0-9][0-9]*$" : "NUMBR Literal",
            "^-?[0-9]*\.[0-9]+$" : "NUMBAR Literal",
            "\".*\"": "YARN Literal",
            "^WIN$": "TROOF Literal",
            "^FAIL$":"TROOF Literal",
            "^NUMBR$":"TYPE Literal",
            "^NUMBAR$":"TYPE Literal",
            "^YARN$": "TYPE Literal",
            "^TROOF$": "TYPE Literal",  #Literals
        }
        self.identifiers = {
            "[a-z]+[a-zA-Z0-9_]*": "Identifier", 
            # [a-z]+[a-zA-Z0-9_]*": "Variable Identifier", 
            # "[a-z]+[a-zA-Z0-9_]*": "Function Identifier", 
            # "[a-z]+[a-zA-Z0-9_]*": "Loop Identifier", 
        }
        self.operations = {
            "^SUM OF$": "Addition Operator" , 
            "^DIFF OF$": "Substraction Operator",  
            "^PRODUKT OF$": "Multiplication Operator", 
            "^QUOSHUNT OF$": "Division Operator", #Sum of to Quoshunt of
            "^MOD OF$": "Modulo Operator", 
            "^BIGGR OF$": "Maximum Operator", 
            "^SMALLR OF$": "Minimum Operator",  #MOD of to Smallr of
            "^BOTH OF$": "and operator", #!
            "^EITHER OF$": "or operator",#!
            "^WON OF$": "XOR Operator",#!
            "^NOT$": "Not operator",
            "^ANY OF$": "Infiinite arity or operator", #!
            "^ALL OF$": "Infinite arity and operator",  #! #Both of to ALL OF
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

    def getActual(self):
        return self.mismo

    def getType(self):
        return self.type
    
    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value
    

class Program():
    def __init__(self,lexemes,hai_lexeme,kthxbye_lexeme):
        self.HAI=hai_lexeme
        self.KTHXBYE=kthxbye_lexeme
        # self.statement=[]
        self.statement=list()
        # self.linebreak=None

    def lookAhead(self, lexemes):
        statementHolder = []
        multiline_comment_active = False
        for lexeme in lexemes:
            if lexeme.getType() == "Single Line Delimiter" and multiline_comment_active == False:
                continue # if single line comment, proceed to next lexeme
            elif lexeme.getType() == "Multiline Comment Delimiter":
                multiline_comment_active = True
                continue
            elif multiline_comment_active:
                continue
            elif lexeme.getType() == "Comment Delimiter":
                multiline_comment_active = False
                continue
            elif lexeme.getType() != "Line Break":
                statementHolder.append(lexeme)
            elif lexeme.getType() == "Line Break":
                # statementHolder.append(lexeme)
                self.statement.append(statementHolder)
                statementHolder = []
            

    def getStatements(self):
        return self.statement

#lookahead method

        
    
class Statement():
    def __init__(self):
        #! take note of multiple instances of the same statement
        self.print= None
        self.vardec=None
        self.input=None
        self.assignment=None
        self.ifelse=None
        self.switchcase=None
        self.loop=None
        self.function=None
        self.functioncall=None
        # self.statement=None
        # self.linebreak = None

    def lookAhead(self, statements):
        # * holders
        # statementHolder = []
        ifCondObj = None
        ifElseObj = None
        caseObj= None
        defaultObj= None
        ifClauseObject = None
        elseClauseObject = None
        switchCaseObject=None
        clauseListOfStatements = []
        caseListofStatements= []

        #* flags
        multiline_comment_active = False
        printFlag = False
        ifElseFlag = False
        ifClauseActive = False
        elseClauseActive = False
        switchCaseActive= False
        caseObjActive=False
        defaultObjActive= False
        # TODO create if else flag for multiple lines kasi ung if else
        #! take note of comments
        #! take note of the order of the statements
        for statement in statements:
            # for lexeme in statement: # ! maybe we can replace this part --
            if statement == []:
                continue
            lexeme = statement[0] #! -- with this one
            if lexeme.getType() == "Output Keyword" and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False and printFlag ==False: #* PRINT
                printObj = Print()
                printObj.lookAhead(statement)
                self.print = printObj
                # self.print.append(statement)
            elif lexeme.getType() == "Variable Declaration" and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False: #* VAR DEC
                vardecObj = Vardec()
                vardecObj.lookAhead(statement)
                self.vardec = vardecObj
            elif lexeme.getType() == "User input" and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False: #* GIMMEH
                inputObj = Input()
                inputObj.lookAhead(statement)
                self.input = inputObj
            elif lexeme.getType() == "Variable Identifier" and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False: #* ASSIGNMENT
                assignObj = Assignment()
                assignObj.lookAhead(statement)
                self.assignment = assignObj
            elif lexeme.getType() in ["and operator", "or operator", "XOR operator", "Equal comparison Operator", "Not equal comparison"] and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False: #* IF CONDITION
                ifCondObj = Ifcond()
                ifCondObj.lookAhead(statement)
                ifElseFlag = True
            elif lexeme.getType() == "IF-ELSE Statement Opening Delimiter" and ifElseFlag and ifClauseActive == False and elseClauseActive == False: #* IF STATEMENT
                #IF-ELSE na obj
                ifElseObj = Ifelse(lexeme)
                #IF-ELSE na obj.setIfCond(ifCondObj)
                ifElseObj.setCond(ifCondObj)
                #TODO IF-ELSE na obj.lookAhead
            elif lexeme.getType() == "IF TRUE delimiter" and ifElseFlag and ifClauseActive == False and elseClauseActive == False: # the true branch for if-else statement
                ifClauseObject = IfClause(lexeme)
                ifClauseActive = True
            elif ifClauseActive and ifElseFlag: # codeblock inside true branch
                # collect all statements until a NO WAI is encountered
                if lexeme.getType() == "ELSE-IF delimiter":
                    # mebbe clause
                    pass
                elif lexeme.getType() == "ELSE delimiter":
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
            elif elseClauseActive and ifElseFlag: # codeblock inside F/else branch
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
                    ifElseObj.setElseClause(ifClauseObject)
                    # we create the elseClause object since a NO WAI is encountered
                    ifElseObj.setOIC(lexeme)
                    clauseListOfStatements = [] # clear the clauseListOfStatements holder
                else: 
                    clauseListOfStatements.append(statement)
            elif lexeme.getType() == "Switch Case Start Delimiter" and not switchCaseActive and not ifElseFlag and not ifClauseActive and not elseClauseActive:
                switchCaseActive= True
                switchCaseObject= SwitchCase(lexeme)

            elif switchCaseActive and lexeme.getType() in ["Case Specifier", "Default Switch Case Specifiier"] and not caseObjActive:
                if lexeme.getType() == "Case Specifier":
                    caseObjActive= True
                    caseObj = Case()
                    caseObj.lookAhead(statement)
                elif lexeme.getType() == "Default Switch Case Specifiier":
                    defaultObj=DefaultCase(lexeme)
                    defaultObjActive=True
                    
            elif switchCaseActive and defaultObjActive and not caseObjActive and not ifElseFlag and not ifClauseActive and not elseClauseActive:
                if lexeme.getType() == "Switch Case/IF-ELSE End Delimiter":
                    codeBlockObj = CodeBlock()
                    codeBlockObj.lookAhead(caseListofStatements)
                    defaultObj.setCodeBlock(codeBlockObj)
                    defaultObjActive = False
                    switchCaseObject.setDefaultCase(defaultObj)
                    switchCaseObject.setOIC(lexeme)
                    switchCaseActive=False
            
                    caseListofStatements = []
                else:
                    caseListofStatements.append(statement)                

            elif switchCaseActive and caseObjActive and not ifElseFlag and not ifClauseActive and not elseClauseActive:
                if lexeme.getType()=="Break Statement":
                    codeBlockObj= CodeBlock()
                    codeBlockObj.lookAhead(caseListofStatements)
                    caseObj.setCodeBlock(codeBlockObj)
                    caseObj.setGTFO(lexeme)
                    caseObjActive=False
                    switchCaseObject.setCase(caseObj)

                    caseListofStatements=[]

                else:
                    caseListofStatements.append(statement)


class Print():
    def __init__(self):
        self.left_operand=None
        self.right_operand=[]  #may branch
        self.linebreak = None

    #! take note of comments
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

class VisibleOperand():
    def __init__(self):
        # self.yarn=None
        self.expr=None
        self.literal=None
        self.varident= None
        self.linebreak=None

    # ! take note order of the operands
    def lookAhead(self, listOfLexemes):
        string_delimiter_flag = False
        literalObj = None
        exprObj = None
        expr_active = False
        expr_holder = []
        for lexeme in listOfLexemes:
            if lexeme.getType()=="String Delimiter" and string_delimiter_flag == False:
                string_delimiter_flag = True
                literalObj = Literal()
            elif string_delimiter_flag:
                literalObj.setValue(lexeme)
                self.literal=literalObj
            elif lexeme.getType()=="String Delimiter" and string_delimiter_flag:
                string_delimiter_flag = False
            elif lexeme.getType() in ["TROOF Literal", "NUMBR Literal", "NUMBAR Literal", "TYPE Literal"]:
                literalObj = Literal()
                literalObj.setValue(lexeme)
                self.literal=literalObj
            elif lexeme.getType() == "Variable Identifier":
                self.varident = lexeme
            elif expr_active:
                expr_holder.append(lexeme)
            else: 
                expr_active = True
                exprObj = Expr()
        if expr_active:
            exprObj.setExpr(expr_holder) # !


# TODO : expr
class Expr():
    def __init__(self):
        self.expr = None

    def setExpr(self, expr):
        self.expr = expr

class Literal():
    def __init__(self):
        self.literal=None

    def setValue(self, value):
        self.literal = value

class Vardec():
    def __init__(self):
        self.left_operand=None
        self.varident = None
        self.varinit = None

    #! take note of comments
    #! take note of variable identifier and identifier
    def lookAhead(self, statement):
        statementHolder = []
        varInitHolder = []
        for lexeme in statement:
            if lexeme.getType()=="Variable Declaration":
                self.left_operand = lexeme
            elif lexeme.getType() == "Variable Identifier":
                self.varident = lexeme 
            elif lexeme.getType() != "Identifier":
                varInitHolder.append(lexeme)

        varInitObj = Varinit()
        varInitObj.lookAhead(varInitHolder)
        self.varinit = varInitObj
        
class Varinit():
    def __init__(self):
        self.left_operand = None # ITZ
        self.literal=None
        self.expr=None
        self.typecast=None  #bonus
        self.varident=None

        # ! take note order of the operands
    def lookAhead(self, listOfLexemes): # ITZ operand
        literalObj = None
        exprObj = None
        expr_active = False
        expr_holder = []
        for lexeme in listOfLexemes:
            if lexeme.getType()=="Variable Assignment":
                self.left_operand = lexeme
            elif lexeme.getType() in ["TROOF Literal", "NUMBR Literal", "NUMBAR Literal", "TYPE Literal"]:
                literalObj = Literal()
                literalObj.setValue(lexeme)
                self.literal = literalObj
            elif lexeme.getType() == "Variable Identifier":
                self.varident = lexeme
            elif expr_active:
                expr_holder.append(lexeme)
            else: 
                expr_active = True
                exprObj = Expr()
        if expr_active:
            exprObj.setExpr(expr_holder) # !
    
class Input():  #* how to implement 
    def __init__(self):
        self.gimmeh = None
        self.varident = None
    
    def lookAhead(self, statement):
        for lexeme in statement:
            if lexeme.getType() == "User input":
                self.gimmeh = lexeme
            elif lexeme.getType() == "Variable Identifier":
                self.varident = lexeme

class Assignment():
    def __init__(self):
        self.left_operand= None
        self.middle_operand= None
        self.right_operand= None  #typecast,varident,lietral,expr,concatenation

    def lookAhead(self, statement):
        exprObj = None
        expr_active = False
        expr_holder = []

        for lexeme in statement:
            if lexeme.getType() == "Variable Identifier" and self.middle_operand == None:
                self.left_operand = lexeme
            elif lexeme.getType() == "Assignment Operation Keyword":
                self.middle_operand = lexeme    
            elif lexeme.getType() in ["TROOF Literal", "NUMBR Literal", "NUMBAR Literal", "TYPE Literal"]:
                self.right_operand = lexeme
            elif lexeme.getType() == "Variable Identifier" and self.middle_operand != None:
                self.right_operand = lexeme
            elif expr_active:
                expr_holder.append(lexeme)
            else: 
                expr_active = True
                exprObj = Expr()
        if expr_active:
            exprObj.setExpr(expr_holder) # !
            
#! class for concatenation
class Ifcond():
    def __init__(self):
        self.boolean=None
        self.comparison=None
    
    def lookAhead(self, statement):
        exprObj = None
        expr_active = False
        expr_holder = []

        for lexeme in statement:
            if lexeme.getType() in ["and operator", "or operator", "XOR operator"]:
                # TODO make boolean object, look ahead(statement)
                # TODO look ahead(statement)
                # TODO self.boolean = obj
                pass

            elif lexeme.getType() in ["Equal comparison Operator", "Not equal comparison"]:
                # TODO make comparison object, look ahead(statement)
                # TODO look ahead(statement)
                # TODO self.comparison = obj
                pass

class Ifelse():
    def __init__(self,orly_lexeme):
        self.ifcond=None
        self.orly = orly_lexeme # orly lexeme
        self.ifclause=None
        self.elseclause=None
        self.mebbeclause=None # !
        self.oic=None

    def setCond(self, ifCondObj):
        self.ifcond = ifCondObj

    def setIfClause(self, if_clause_object):
        self.ifclause = if_clause_object
    
    def setElseClause(self, else_clause_object):
        self.ifclause = else_clause_object

    def setOIC(self, oic_lexeme):
        self.oic = oic_lexeme

class IfClause():
    def __init__(self, ya_rly_lexeme):
        self.left_operand=ya_rly_lexeme
        self.right_operand=None  #Code Block

    def setRightOperand(self, codeBlock):
        self.right_operand = codeBlock


class ElseClause():
    def __init__(self,no_wai_lexeme):
        self.left_operand=no_wai_lexeme
        self.right_operand=None  #Code Block

    def setRightOperand(self, codeBlock):
        self.right_operand = codeBlock


#! make booleans
class Boolean():
    def __init__(self):
        pass

class Comparison():
    def __init__(self):
        self.compoperator=None
        self.left_operand=None   #<compoperator> <operand> AN <operand> 
                            #|<compoperator> <operand> AN <operation2> <operand> AN <operand> 
        self.right_operand=None

    def lookAhead(self, statement):
        operandHolder = []

        operation2Obj= None
        operandObj = None
        leftOperandActive=False
        operation2Active=False
        
        #!make flags for operand and arithmetic since operand needs statement and not lexeme
        for lexeme in statement:
            if lexeme.getType() in ["Equal comparison Operator", "Not equal comparison operator"]:
                self.compoperator = lexeme
            else:
                operandHolder.append(lexeme)
                if lexeme.getType()=="Operand Separator" and self.left_operand == None:
                    operandObj=Operand()
                    operandObj.lookAhead(statement)
                    self.left_operand = operandHolder  # <compoperator> <operand>
                    operandHolder=[]
                    leftOperandActive=True
                elif lexeme.getType() in ["Maximum Operator", "Minimum Operator"] and leftOperandActive:
                    operation2Obj=Operation2(lexeme)      # <compoperator> <operand> AN <operation2>
                    operation2Active=True
                elif operation2Active and lexeme.getType == "Operand Separator":
                    operation2Obj.setLeftOperand(operandHolder)  # <compoperator> <operand> AN <operation2> 
                    operandHolder=[]
                elif operation2Obj.left_operand != None and operation2Active:
                    operation2Obj.setRightOperand(operandHolder) # <compoperator> <operand> AN <operation2> <operand> AN <operand>
                    operandHolder = []
                    operation2Active=False
                    self.right_operand=operation2Obj
                elif not operation2Active and leftOperandActive:
                    self.right_operand=lexeme     # <compoperator> <operand> AN <operand>

class Compoperator():
    def __init__(self, lexemes):
        self.left_operand= None   #BOTH SAEM  | DIFFRNT

class Operand():
    def __init__(self):
        self.leaf_operand= None # varident, numbr, numbr, arithmetic 

    def lookAhead(self,statement):
        for lexeme in statement:
            if lexeme.getType in ["NUMBR Literal", "NUMBAR Literal","Variable Identifier"]:
                self.leaf_operand=lexeme
            elif lexeme.getType in ["SUM OF","DIFF OF","PRODCUKT OF","QUOSHUNT OF","MOD OF"]:
                #!make arithmetic object
                pass
     
class Arithmetic():
    def __init__(self, lexemes):
        self.operation1 = None
        self.an= None
        self.left_operand= None
        self.right_operand= None

class Operation1():
    def __init__(self,lexemes):
        self.leaf_operand=None #* SUM OFF | DIFF OF etc

class Operation2():
    def __init__(self,lexeme):
        self.leaf_operand=lexeme
        self.left_operand = None
        self.right_operand = None

    def setLeftOperand(self,lexeme):
        self.left_operand=lexeme

    def setRightOperand(self,lexeme):
        self.right_operand=lexeme    



#! class MebbeClause

class SwitchCase():
    def __init__(self,lexeme):
        self.left_operand=lexeme  #WTF
        self.right_operand=None #OIC
        self.case=[]        #case OMG
        self.default=None  # case OMGWTF
    
    def setCase(self,caseObj):
        self.case.append(caseObj)
    
    def setDefault(self,caseObj):
        self.default=caseObj

    def setOIC(self,lexeme):
        self.right_operand=lexeme


    

class DefaultCase():
    def __init__(self,lexeme):
        self.leaf_operand = lexeme
        self.codeblock = None
    
    


class Case():
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
    
        
             
    
    


class CodeBlock():
    def __init__(self):
        self.print = None
        self.vardec = None
        self.expr = None
        self.assignment = None
        self.ifelse = None
        self.switchcase = None
        self.loop = None
        self.functioncall = None
        self.codeblock = None
        self.linebreak = None

    def lookAhead(self, statements):
        # * holders
        # statementHolder = []
        ifCondObj = None
        ifElseObj = None
        ifClauseObject = None
        elseClauseObject = None
        clauseListOfStatements = []

        #* flags
        multiline_comment_active = False
        printFlag = False
        ifElseFlag = False
        ifClauseActive = False
        elseClauseActive = False
        # TODO create if else flag for multiple lines kasi ung if else
        #! take note of comments
        #! take note of the order of the statements
        for statement in statements:
            # for lexeme in statement: # ! maybe we can replace this part --
            if statement == []:
                continue
            lexeme = statement[0] #! -- with this one
            if lexeme.getType() == "Output Keyword" and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False: #* PRINT
                printObj = Print()
                printObj.lookAhead(statement)
                self.print = printObj
                # self.print.append(statement)
            elif lexeme.getType() == "Variable Declaration" and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False: #* VAR DEC
                vardecObj = Vardec()
                vardecObj.lookAhead(statement)
                self.vardec = vardecObj
            elif lexeme.getType() == "User input" and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False: #* GIMMEH
                inputObj = Input()
                inputObj.lookAhead(statement)
                self.input = inputObj
            elif lexeme.getType() == "Variable Identifier" and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False: #* ASSIGNMENT
                assignObj = Assignment()
                assignObj.lookAhead(statement)
                self.assignment = assignObj
            elif lexeme.getType() in ["and operator", "or operator", "XOR operator", "Equal comparison Operator", "Not equal comparison"] and ifElseFlag == False and ifClauseActive == False and elseClauseActive == False: #* IF CONDITION
                ifCondObj = Ifcond()
                ifCondObj.lookAhead(statement)
                ifElseFlag = True
            elif lexeme.getType() == "IF-ELSE Statement Opening Delimiter" and ifElseFlag and ifClauseActive == False and elseClauseActive == False: #* IF STATEMENT
                #IF-ELSE na obj
                ifElseObj = Ifelse(lexeme)
                #IF-ELSE na obj.setIfCond(ifCondObj)
                ifElseObj.setCond(ifCondObj)
                #TODO IF-ELSE na obj.lookAhead
            elif lexeme.getType() == "IF TRUE delimiter" and ifElseFlag and ifClauseActive == False and elseClauseActive == False: # the true branch for if-else statement
                ifClauseObject = IfClause(lexeme)
                ifClauseActive = True


            elif ifClauseActive and ifElseFlag:  # codeblock inside true branch
                # collect all statements until a NO WAI is encountered
                if lexeme.getType() == "ELSE-IF delimiter":
                    # mebbe clause
                    pass
                elif lexeme.getType() == "ELSE delimiter":
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
                    clauseListOfStatements = []  # clear the clauseListOfStatements holder
                else:
                    clauseListOfStatements.append(statement)
            elif elseClauseActive and ifElseFlag: # codeblock inside F/else branch
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
                    ifElseObj.setElseClause(ifClauseObject)
                    # we create the elseClause object since a NO WAI is encountered
                    ifElseObj.setOIC(lexeme)
                    clauseListOfStatements = [] # clear the clauseListOfStatements holder
                else: 
                    clauseListOfStatements.append(statement)


#!class functions, function call etc

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
# ! notes we should be updating the symbol table that we refer to everytime we encounter an identifier, baka andun na kasi pala siya

# * ---------------------------------------------------------------------------------------------------- LEXICAL ANALYSIS
def makeLexeme(mismo,lex_type,lexemes): #* function that constructs a lexeme object for a passed string
    tempLexeme = Lexeme(mismo) # mismong string
    tempLexeme.setType(lex_type) # type of lexeme
    lexemes.append(tempLexeme)
    tempLexeme.export(lexAndSymbolTables) # add the lexeme to the table in the GUI
    
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
    switch_case_active = False # ! not sure if this will be useful
 
    #* temporary holders
    multi_line_comment_actual = "" # temporary holder for a multi-line comment
    scanned_word = "" # temporary holder for a scanned word

    for character in code: # iterate through every character in the source code
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
            
            makeLexeme("\\n", "Line Break", lexemes)


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

# * ---------------------------------------------------------------------------------------------------------------------
# * ------------------------------------------------------------------------------------------------------SYNTAX ANALYSIS
def syntaxAnalysis(): # * function that executes syntax analysis
    print("SYNTAX ANALYSIS")
    lexemes = theCode.getLexemes()

    # statements = []
    # multiline_comment_active = False
    # statementHolder = [] # temporary holder for multiple lexemes that should form a statement
    # clearStatementHolder = False
    # printFlag = False

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
            break # ! not sure about this pero i think it is 
        index = index + 1

    # create program object and loop through statements between the code delimiters
    if startFlag and endFlag:
        hai_lexeme = lexemes.pop(indexOfStartCode)
        kthxbye_lexeme = lexemes.pop(indexOfEndCode)
        print("CODE DELIMITERS")
        print(hai_lexeme)
        print(kthxbye_lexeme)
        print("CODE DELIMITERS")

        programRoot = Program(lexemes, hai_lexeme, kthxbye_lexeme)
        programRoot.lookAhead(lexemes)

        statements = programRoot.getStatements()
        statementRoot = Statement()
        statementRoot.lookAhead(statements)

        # print("ASTTAETMENTS")
        # for statement in programRoot.getStatements():
        #     for lexeme in statement:
        #         print(lexeme.getActual())


def visibleOperand(lexeme): # * for visible operands only

    if isLiteral(lexeme):
        return True
    elif isExpr(lexeme):
        return True
    elif lexeme.getType() == "Variable Identifier":
        return True
    else:
        return False

def isExpr(lexeme):
    # check if arithmetic
    if isArithmetic(lexeme):
        return True
    # check if boolean
    elif isBoolean(lexeme):
        return True
    # check if comparison
    elif isComparison(lexeme):
        return True
    return False
    
def isArithmetic(lexeme):
    operation1 = theCode.getOperations().keys()

    # for index in range(7): # operation 1
    #     if lexeme.getActual() == operation1[index]:
    #         return True
    if lexeme.getActual() in operation1:
        return True

    if isOperand(lexeme): # operand
        return True
    elif lexeme.getType() == "Operand Separator":
        return True
    return False


def isBoolean(lexeme):

    #check if first type of boolean
    booloperation1 = theCode.getOperations()[7:10]

    for operation in booloperation1: # operation 1
        if lexeme.getActual() == operation:
            return True

    if isBoolOperand1(lexeme): # operand
        return True
    elif lexeme.getType() == "Operand Separator":
        return True

    #check if second type of boolean
    if isUnary(lexeme):
        return True

    # check if third type of boolean
    if isBoolean2(lexeme):
        return True
    return False

def isBoolean2(lexeme):
    booloperation2 = theCode.getOperations()[11:13]

    for operation in booloperation2: # operation 1
        if lexeme.getActual() == operation:
            return True

    if lexeme.getType() == "Variable Identifier":
        return True
    elif lexeme.getType() == "TROOF Literal":
        return True
    elif lexeme.getType() == "End of Boolean Statement":
        return True
    elif lexeme.getType() == "Operand Separator":
        return True
    return False

    # ! incomplete pa 
    # ! booleanf2only
    

def isBoolOperand1(lexeme):
    if lexeme.getType() == "Variable Identifier":
        return True
    elif lexeme.getType() == "TROOF Literal":
        return True
    elif isBoolean(lexeme):
        return True
    return False

def isOperand(lexeme):
    # * pwede ata ipagsama ? gamit ng or statement? 
    if lexeme.getType() == "Variable Identifier":
        return True
    elif lexeme.getType() == "NUMBR Literal":
        return True
    elif lexeme.getType() == "NUMBAR Literal":
        return True
    elif isArithmetic(lexeme):
        return True
    return False

def isLiteral(lexeme):
    literals = theCode.getLiterals()
    values = literals.values()

    for value in values:
        if lexeme.getType() == value:
            return True
    return False

def isUnary(lexeme):
    lexemeType = lexeme.getType()
    if lexemeType == "Loop increment" or lexemeType == "Loop decrement" or lexemeType == "Not operator":
        return True
    return False 


# * ---------------------------------------------------------------------------------------------------------------------

def executeCode(): #* function that executes the loaded code
    # print(codeSelectAndDisplay.getCodeDisplay().get("1.0","end"))
    terminal.setDisplay("Compiling...")
    lexicalAnalysis()
    syntaxAnalysis()

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
