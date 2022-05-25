from ast import Assign
import sys
import re
from unittest.mock import AsyncMock

header = '''; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment .data

segment .bss  ; variaveis
  res RESB 1

section .text
  global _start

print:  ; subrotina print

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer

  MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
  XOR ESI, ESI

print_dec: ; empilha todos os digitos
  MOV EDX, 0
  MOV EBX, 0x000A
  DIV EBX
  ADD EDX, '0'
  PUSH EDX
  INC ESI ; contador de digitos
  CMP EAX, 0
  JZ print_next ; quando acabar pula
  JMP print_dec

print_next:
  CMP ESI, 0
  JZ print_exit ; quando acabar de imprimir
  DEC ESI

  MOV EAX, SYS_WRITE
  MOV EBX, STDOUT

  POP ECX
  MOV [res], ECX
  MOV ECX, res

  MOV EDX, 1
  INT 0x80
  JMP print_next

print_exit:
  POP EBP
  RET

; subrotinas if/while
binop_je:
  JE binop_true
  JMP binop_false

binop_jg:
  JG binop_true
  JMP binop_false

binop_jl:
  JL binop_true
  JMP binop_false

binop_false:
  MOV EBX, False
  JMP binop_exit
binop_true:
  MOV EBX, True
binop_exit:
  RET

_start:
'''

footer = "POP EBP \n" + "MOV EAX, 1 \n" + "INT 0x80 \n"

class SymbolTable:
    symbolTableDict = {}
    pointer = 4

    @staticmethod
    def getIdentifier(identifierName):
        if(identifierName in SymbolTable.symbolTableDict.keys()):
            return SymbolTable.symbolTableDict.get(identifierName)
        else:
            raise ValueError(
                "Symbol Table ERROR - Identifier not in symbol table")

    @staticmethod
    def setIdentifier(identifierName, value):
        if(identifierName in SymbolTable.symbolTableDict.keys()):
            if(SymbolTable.symbolTableDict[identifierName][1] == "str" and type(value) == str
            or SymbolTable.symbolTableDict[identifierName][1] == "int" and str(value).isnumeric()):
                SymbolTable.symbolTableDict[identifierName] = (
                    value, SymbolTable.symbolTableDict[identifierName][1],SymbolTable.symbolTableDict[identifierName][2])
        else:
            raise ValueError(
                "Symbol Table ERROR - Identifier not in symbol table")

    @staticmethod
    def createIdentifier(identifierName, type):
        if(identifierName in SymbolTable.symbolTableDict.keys()):
            raise ValueError(
                "Symbol Table ERROR - Identifier already in symbol table")
        else:
            SymbolTable.symbolTableDict[identifierName] = (None, type, SymbolTable.pointer)
            SymbolTable.pointer += 4


class Token:
    def __init__(self, type, value):
        self.type = type  # tipo do token
        self.value = value  # valor do token


class PrePro:
    @staticmethod
    def filter(code):
        return re.sub("/\*.*?\*/", "", code)
    

class ASM:

    code = ""
    filename = sys.argv[1].replace('.c', '.asm')

    @staticmethod
    def Write(cmd):
        ASM.code += cmd + "\n"
    
    @staticmethod
    def Dump():
        with open(ASM.filename, 'w') as f:
            f.write(header + ASM.code + footer)
        f.close()

class Node:

    id = 0

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self):
        pass
    
    @staticmethod
    def newId():
        Node.id += 1
        return Node.id


class BinOp(Node):

    def Evaluate(self):

        left = self.children[0].Evaluate()
        ASM.Write(f'PUSH EBX')
        right = self.children[1].Evaluate()
        ASM.Write(f'POP EAX')

        if (left[1] == "str" and right[1] == "str"):

            if (self.value == "=="):
                if(left[0] == right[0]):
                    return(1,"str")
                else:
                    return(0,"str")

            elif (self.value == "."):
                return (left[0] + right[0], "str")
            
            elif (self.value == "<"):
                if(left[0] < right[0]):
                    return(1,"str")
                else:
                    return(0,"str")

            elif (self.value == ">"):
                if(left[0] > right[0]):
                    return(1,"str")
                else:
                    return(0,"str")
        
        elif (left[1] == "str" and right[1] != "str"):
            if (self.value == "."):
                return (left[0] + str(right[0]), "str")

        elif (left[1] != "str" and right[1] == "str"):
            if (self.value == "."):
                return (str(left[0]) + right[0], "str")

        elif (left[1] != "str" and right[1] != "str"):

            if(self.value == "+"):
                ASM.Write(f"ADD EAX, EBX")
                ASM.Write(f"MOV EBX, EAX")
                return (left[0] + right[0], "int")

            elif (self.value == "-"):
                ASM.Write(f'SUB EAX, EBX')
                ASM.Write(f'MOV EBX, EAX')
                return (left[0] - right[0], "int")

            elif (self.value == "*"):
                ASM.Write(f'IMUL EAX, EBX')
                ASM.Write(f'MOV EBX, EAX')
                return (left[0] * right[0], "int")

            elif (self.value == "/"):
                ASM.Write(f'IDIV EAX, EBX')
                ASM.Write(f'MOV EBX, EAX')
                return (left[0] // right[0], "int")

            elif (self.value == "<"):
                ASM.Write('CMP EAX, EBX')
                ASM.Write('CALL binop_jl')
                if(left[0] < right[0]):
                    return(1,"int")
                else:
                    return(0,"int")

            elif (self.value == ">"):
                ASM.Write('CMP EAX, EBX')
                ASM.Write('CALL binop_jg')
                if(left[0] > right[0]):
                    return(1,"int")
                else:
                    return(0,"int")

            elif (self.value == "=="):
                ASM.Write('CMP EAX, EBX')
                ASM.Write('CALL binop_je')
                if(left[0] == right[0]):
                    return(1,"int")
                else:
                    return(0,"int")

            elif (self.value == "&&"):
                ASM.Write(f'AND EAX, EBX')
                ASM.Write(f'MOV EBX, EAX')
                if(left[0] and right[0]):
                    return(1,"int")
                else:
                    return(0,"int")

            elif (self.value == "||"):
                ASM.Write(f'OR EAX, EBX')
                ASM.Write(f'MOV EBX, EAX')
                if(left[0] or right[0]):
                    return(1,"int")
                else:
                    return(0,"int")

            elif (self.value == "."):
                return (str(left[0]) + str(right[0]), "str")


class UnOp(Node):

    def Evaluate(self):
        if(self.value == "+"):
            return (self.children[0].Evaluate()[0], "int")
        elif (self.value == "-"):
            return (-self.children[0].Evaluate()[0], "int")
        elif (self.value == "!"):
            return (not(self.children[0].Evaluate()[0]), "int")


class AssignOp(Node):

    def Evaluate(self):
        for child in self.children:
            SymbolTable.createIdentifier(child.value, self.value)
            ASM.Write('PUSH DWORD 0')


class SetOp(Node):

    def Evaluate(self):
        temp_set = self.children[1].Evaluate()[0]
        ASM.Write(f'MOV [EBP-{SymbolTable.getIdentifier(self.children[0].value)[2]}], EBX')

        SymbolTable.setIdentifier(self.children[0].value, temp_set )



class IntVal(Node):

    def Evaluate(self):
        ASM.Write(f'MOV EBX, {self.value}')
        return (self.value, "int")


class StrVal(Node):

    def Evaluate(self):
        return (self.value, "str")


class NoOp(Node):

    def Evaluate(self):
        pass


class Identifier(Node):

    def Evaluate(self):
        ASM.Write(f"MOV EBX, [EBP-{str(SymbolTable.getIdentifier(self.value)[2])}]")
        return SymbolTable.getIdentifier(self.value)


class Printf(Node):

    def Evaluate(self):
        temp_print = self.children[0].Evaluate()[0]
        ASM.Write('PUSH EBX')
        ASM.Write('CALL print')
        ASM.Write('POP EBX')
        print(temp_print)


class Scanf(Node):

    def Evaluate(self):
        input_ = int(input())
        return (input_, "int")


class Block(Node):

    def Evaluate(self):
        for child in self.children:
            child.Evaluate()


class While(Node):

    def Evaluate(self):
        temp_while = Node.newId()
        ASM.Write(f'LOOP_{temp_while}:')
        self.children[0].Evaluate()
        ASM.Write('CMP EBX, False')
        ASM.Write(f'JE EXIT_{temp_while}')
        self.children[1].Evaluate()
        ASM.Write(f'JMP LOOP_{temp_while}')
        ASM.Write(f'EXIT_{temp_while}:')


class If(Node):

    def Evaluate(self):
         
        tmp_if = Node.newId()
        ASM.write(f"IF_{tmp_if}:")
        self.children[0].Evaluate()
        ASM.write("CMP EBX, False")
        ASM.write(f"JE ELSE_{tmp_if}") 
        self.children[1].Evaluate()
        ASM.write(f"JMP IF_END_{tmp_if}")
        ASM.write(f"ELSE_{tmp_if}:")
        if (len(self.children) > 2):
            self.children[2].Evaluate()
        ASM.write(f"IF_END_{tmp_if}:")


class Tokenizer:

    reservedWords = ["printf", "if", "else", "while", "scanf", "int", "str"]

    def __init__(self, origin):
        self.origin = origin  # codigo fonte que sera tokenizado
        self.position = 0  # posição atual que o tokenizador está separando
        self.actual = None  # o ultimo token separando

    def selectNext(self):
        # le o proximo token e atualiza o atributo atual
        if(self.position >= len(self.origin)):
            self.actual = Token("EOF", 0)
            return self.actual

        while(self.origin[self.position] == " " or self.origin[self.position] == "\n"):
            self.position += 1
            if(self.position >= len(self.origin)):
                self.actual = Token("EOF", 0)
                return self.actual

        if(self.origin[self.position] == '+'):
            self.position += 1
            self.actual = Token("plus", 0)
            return self.actual

        elif(self.origin[self.position] == '-'):
            self.position += 1
            self.actual = Token("minus", 0)
            return self.actual

        elif(self.origin[self.position] == '*'):
            self.position += 1
            self.actual = Token("mult", 0)
            return self.actual

        elif(self.origin[self.position] == '/'):
            self.position += 1
            self.actual = Token("div", 0)
            return self.actual

        elif(self.origin[self.position] == '('):
            self.position += 1
            self.actual = Token("openParentheses", 0)
            return self.actual

        elif(self.origin[self.position] == ')'):
            self.position += 1
            self.actual = Token("closeParentheses", 0)
            return self.actual

        elif(self.origin[self.position] == '{'):
            self.position += 1
            self.actual = Token("openCurlyBrackets", 0)
            return self.actual

        elif(self.origin[self.position] == '}'):
            self.position += 1
            self.actual = Token("closeCurlyBrackets", 0)
            return self.actual

        elif(self.origin[self.position] == ';'):
            self.position += 1
            self.actual = Token("semicolon", 0)
            return self.actual

        elif(self.origin[self.position] == '<'):
            self.position += 1
            self.actual = Token("lesser", 0)
            return self.actual

        elif(self.origin[self.position] == '>'):
            self.position += 1
            self.actual = Token("greater", 0)
            return self.actual

        elif(self.origin[self.position] == '!'):
            self.position += 1
            self.actual = Token("not", 0)
            return self.actual

        elif(self.origin[self.position] == '=' and self.origin[self.position + 1] == '='):
            self.position += 2
            self.actual = Token("compare", 0)
            return self.actual

        elif(self.origin[self.position] == '='):
            self.position += 1
            self.actual = Token("assign", 0)
            return self.actual

        elif(self.origin[self.position] == '.'):
            self.position += 1
            self.actual = Token("concat", 0)
            return self.actual

        elif(self.origin[self.position] == ','):
            self.position += 1
            self.actual = Token("comma", 0)
            return self.actual

        elif(self.origin[self.position] == '&' and self.origin[self.position + 1] == '&'):
            self.position += 2
            self.actual = Token("and", 0)
            return self.actual

        elif(self.origin[self.position] == '|' and self.origin[self.position + 1] == '|'):
            self.position += 2
            self.actual = Token("or", 0)
            return self.actual

        elif self.origin[self.position] == '"':
            self.position += 1
            candidato = self.origin[self.position]
            self.position += 1
            while self.position < len(self.origin) and (self.origin[self.position] != '"'):
                candidato += self.origin[self.position]
                self.position += 1
            self.position += 1
            self.actual = Token("str", candidato)
            return self.actual

        elif(self.origin[self.position].isalpha()):
            candidato = self.origin[self.position]
            self.position += 1
            if(self.position < len(self.origin)):
                while(self.origin[self.position].isalpha() or self.origin[self.position] == '_' or self.origin[self.position].isnumeric()):
                    candidato += self.origin[self.position]
                    self.position += 1
                    if(self.position >= len(self.origin)):
                        break
            if(candidato in Tokenizer.reservedWords):
                self.actual = Token(candidato, 0)
            else:
                self.actual = Token("identifier", candidato)

            return self.actual

        elif(self.origin[self.position].isnumeric()):
            candidato = self.origin[self.position]
            self.position += 1
            if(self.position < len(self.origin)):
                while(self.origin[self.position].isnumeric()):
                    candidato += self.origin[self.position]
                    self.position += 1
                    if(self.position >= len(self.origin)):
                        break
            self.actual = Token("int", int(candidato))
            return self.actual

        else:
            raise ValueError("ERROR")


class Parser:
    tokens = None  # objeto da classe que era ler o codigo fonte e alimentar o analisador

    @staticmethod
    def parseBlock():
        children = []
        if(Parser.tokens.actual.type == "openCurlyBrackets"):
            Parser.tokens.selectNext()
            while (Parser.tokens.actual.type != "closeCurlyBrackets"):
                children.append(Parser.parseStatement())
            node = Block(0, children)
            Parser.tokens.selectNext()
        else:
            raise ValueError(
                "parseBlock ERROR - opened Curly Brackets token not found ")
        return node

    @staticmethod
    def parseStatement():

        if(Parser.tokens.actual.type == "identifier"):

            node = Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()

            if(Parser.tokens.actual.type == "assign"):

                Parser.tokens.selectNext()
                node = SetOp('=', [node, Parser.parseRelExpression()])

                if(Parser.tokens.actual.type == "semicolon"):
                    Parser.tokens.selectNext()
                else:
                    raise ValueError(
                        "parseStatement ERROR - semicolon token not found")
            else:
                raise ValueError(
                    "parseStatement ERROR - assign token not found")

        elif(Parser.tokens.actual.type == "printf"):

            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "openParentheses"):

                Parser.tokens.selectNext()
                node = Printf("printf", [Parser.parseRelExpression()])

                if(Parser.tokens.actual.type == "closeParentheses"):
                    Parser.tokens.selectNext()

                    if(Parser.tokens.actual.type == "semicolon"):
                        Parser.tokens.selectNext()
                    else:
                        raise ValueError(
                            "parseStatement ERROR - semicolon token not found")
                else:
                    raise ValueError(
                        "parseStatement ERROR - closed Parentheses token not found")
            else:
                raise ValueError(
                    "parseStatement ERROR - opened Parentheses token not found")

        elif(Parser.tokens.actual.type == "openCurlyBrackets"):
            node = Parser.parseBlock()

        elif(Parser.tokens.actual.type == "str" or Parser.tokens.actual.type == "int"):

            nodes = []
            actualType = Parser.tokens.actual.type
            Parser.tokens.selectNext()

            if(Parser.tokens.actual.type == "identifier"):

                nodes.append(Parser.tokens.actual)
                Parser.tokens.selectNext()

                while(Parser.tokens.actual.type == "comma"):
                    Parser.tokens.selectNext()

                    if(Parser.tokens.actual.type == "identifier"):
                        nodes.append(Parser.tokens.actual)
                        Parser.tokens.selectNext()
                    else:
                        raise ValueError(
                            "parseStatement ERROR - identifier token not found")
                if(Parser.tokens.actual.type == "semicolon"):
                    Parser.tokens.selectNext()
                    return AssignOp(actualType, nodes)
                else:
                    raise ValueError(
                        "parseStatement ERROR - semicolon token not found")

            else:
                raise ValueError(
                    "parseStatement ERROR - identifier token not found")

        elif Parser.tokens.actual.type == "while":
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "openParentheses":
                Parser.tokens.selectNext()
                expression = Parser.parseRelExpression()
                if Parser.tokens.actual.type == "closeParentheses":
                    Parser.tokens.selectNext()
                    block = Parser.parseStatement()
                else:
                    raise ValueError(
                        "parseStatement ERROR - closed Parentheses token not found")
            else:
                raise ValueError(
                    "parseStatement ERROR - opened Parentheses token not found")

            node = While("while", [expression, block])

        elif Parser.tokens.actual.type == "if":

            children = []
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "openParentheses":
                Parser.tokens.selectNext()
                expression = Parser.parseRelExpression()
                children.append(expression)

                if Parser.tokens.actual.type == "closeParentheses":
                    Parser.tokens.selectNext()
                    block = Parser.parseStatement()
                    children.append(block)

                else:
                    raise ValueError(
                        "parseStatement ERROR - closed Parentheses token not found")

                if Parser.tokens.actual.type == "else":
                    Parser.tokens.selectNext()
                    elseExpression = Parser.parseStatement()
                    children.append(elseExpression)

            else:
                raise ValueError(
                    "parseStatement ERROR - opened Parentheses token not found")

            node = If("if", children)

        elif(Parser.tokens.actual.type == "semicolon"):
            node = NoOp(0, [])
            Parser.tokens.selectNext()

        else:
            raise ValueError("parseStatement ERROR - token not found")

        return node

    @staticmethod
    def parseFactor():
        # consome os tokens do tokenizer e analisa se a sintaze esta aderente
        # a gramatica proposta retorna o resultado da expressão analisada

        if(Parser.tokens.actual.type == "int"):
            node = IntVal(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()

        elif(Parser.tokens.actual.type == "str"):
            node = StrVal(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()

        elif(Parser.tokens.actual.type == "identifier"):
            node = Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()

        elif(Parser.tokens.actual.type == "minus"):
            Parser.tokens.selectNext()
            node = UnOp('-', [Parser.parseFactor()])

        elif(Parser.tokens.actual.type == "plus"):
            Parser.tokens.selectNext()
            node = UnOp('+', [Parser.parseFactor()])

        elif(Parser.tokens.actual.type == "not"):
            Parser.tokens.selectNext()
            node = UnOp('!', [Parser.parseFactor()])

        elif(Parser.tokens.actual.type == "openParentheses"):
            Parser.tokens.selectNext()
            node = Parser.parseRelExpression()
            if(Parser.tokens.actual.type == "closeParentheses"):
                Parser.tokens.selectNext()
            else:
                raise ValueError(
                    "parseFactor ERROR - closed Parentheses token not found")

        elif(Parser.tokens.actual.type == "scanf"):

            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "openParentheses":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == "closeParentheses":
                    Parser.tokens.selectNext()
                else:
                    raise ValueError(
                        "parseFactor ERROR - closed Parentheses token not found")
            else:
                raise ValueError(
                    "parseFactor ERROR - opened Parentheses token not found")

            node = Scanf('scanf', [])

        else:
            raise ValueError("parseFactor ERROR - token not found")

        return node

    @staticmethod
    def parseTerm():
        # a gramatica proposta retorna o resultado da expressão analisada

        node = Parser.parseFactor()

        while((Parser.tokens.actual.type == "mult" or Parser.tokens.actual.type == "div" or Parser.tokens.actual.type == "and")):

            if(Parser.tokens.actual.type == "mult"):
                Parser.tokens.selectNext()
                node = BinOp('*', [node, Parser.parseFactor()])

            elif(Parser.tokens.actual.type == "div"):
                Parser.tokens.selectNext()
                node = BinOp('/', [node, Parser.parseFactor()])

            elif(Parser.tokens.actual.type == "and"):
                Parser.tokens.selectNext()
                node = BinOp('&&', [node, Parser.parseFactor()])

        return node

    @staticmethod
    def parseExpression():

        node = Parser.parseTerm()

        while((Parser.tokens.actual.type == "minus" or Parser.tokens.actual.type == "plus" or Parser.tokens.actual.type == "or" or Parser.tokens.actual.type == "concat")):

            if(Parser.tokens.actual.type == "minus"):
                Parser.tokens.selectNext()
                node = BinOp('-', [node, Parser.parseTerm()])

            elif(Parser.tokens.actual.type == "plus"):
                Parser.tokens.selectNext()
                node = BinOp('+', [node, Parser.parseTerm()])

            elif(Parser.tokens.actual.type == "or"):
                Parser.tokens.selectNext()
                node = BinOp('||', [node, Parser.parseTerm()])

            elif(Parser.tokens.actual.type == "concat"):
                Parser.tokens.selectNext()
                node = BinOp('.', [node, Parser.parseTerm()])

        return node

    @staticmethod
    def parseRelExpression():

        node = Parser.parseExpression()

        while((Parser.tokens.actual.type == "lesser" or Parser.tokens.actual.type == "greater" or Parser.tokens.actual.type == "compare")):

            if(Parser.tokens.actual.type == "lesser"):
                Parser.tokens.selectNext()
                node = BinOp('<', [node, Parser.parseExpression()])

            elif(Parser.tokens.actual.type == "greater"):
                Parser.tokens.selectNext()
                node = BinOp('>', [node, Parser.parseExpression()])

            elif(Parser.tokens.actual.type == "compare"):
                Parser.tokens.selectNext()
                node = BinOp('==', [node, Parser.parseExpression()])

        return node

    def run(code):
        # receve o codigo fonte como argumento, inicializa um objeto tokenizador e
        # retorna o resultado do parse expression(). Esse metodo sera chamado pelo main()

        f = open(code, "r")
        code = f.read()
        f.close()
        postProCode = PrePro.filter(code)
        Parser.tokens = Tokenizer(postProCode)
        Parser.tokens.selectNext()

        result = Parser.parseBlock()
        if(Parser.tokens.actual.type != "EOF"):
            raise ValueError("run ERROR - EOF token not found")
        
        symbolTable = SymbolTable()
        asm = ASM()
        result.Evaluate()
        asm.Dump()


if(len(sys.argv) <= 1):
    raise ValueError("ERROR - missing input")


arg = str(sys.argv[1])
Parser.run(arg)
