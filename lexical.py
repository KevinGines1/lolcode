import re

def lexicalAnalysis(codeSelectAndDisplay, theCode):
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