import sys
import re


class SymbolTable:
    symbolTableDict = {}

    @staticmethod
    def getIdentifier(identifierName):
        return SymbolTable.symbolTableDict.get(identifierName)

    def setIdentifier(identifierName, value):
        SymbolTable.symbolTableDict[identifierName] = value
        pass


class Token:
    def __init__(self, type, value):
        self.type = type  # tipo do token
        self.value = value  # valor do token


class PrePro:
    @staticmethod
    def filter(code):
        return re.sub("/\*.*?\*/", "", code)


class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self):
        pass


class BinOp(Node):

    def Evaluate(self):
        if(self.value == "+"):
            return self.children[0].Evaluate() + self.children[1].Evaluate()
        elif (self.value == "-"):
            return self.children[0].Evaluate() - self.children[1].Evaluate()
        elif (self.value == "*"):
            return self.children[0].Evaluate() * self.children[1].Evaluate()
        elif (self.value == "/"):
            return self.children[0].Evaluate() // self.children[1].Evaluate()
        elif (self.value == "="):
            SymbolTable.setIdentifier(self.children[0].value, self.children[1].Evaluate())


class UnOp(Node):

    def Evaluate(self):
        if(self.value == "+"):
            return self.children[0].Evaluate()
        elif (self.value == "-"):
            return -self.children[0].Evaluate()


class IntVal(Node):

    def Evaluate(self):
        return self.value


class NoOp(Node):

    def Evaluate(self):
        pass


class Identifier(Node):

    def Evaluate(self):
        return SymbolTable.getIdentifier(self.value)


class Printf(Node):

    def Evaluate(self):
        print(self.children[0].Evaluate())

class Block(Node):

    def Evaluate(self):
        for child in self.children:
            child.Evaluate()



class Tokenizer:

    reservedWords = ["printf"]

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

        elif(self.origin[self.position] == '='):
            self.position += 1
            self.actual = Token("assign", 0)
            return self.actual

        elif(self.origin[self.position] == ';'):
            self.position += 1
            self.actual = Token("semicolon", 0)
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
                self.actual = Token(candidato, candidato)
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
            self.actual = Token("numeric", int(candidato))
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
            node = Block(0,children)
            Parser.tokens.selectNext()
        else:
            raise ValueError("ERROR")
        return node

    @staticmethod
    def parseStatement():
        if(Parser.tokens.actual.type == "identifier"):
            node = Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "assign"):
                Parser.tokens.selectNext()
                node = BinOp('=', [node, Parser.parseExpression()])
                if(Parser.tokens.actual.type == "semicolon"):
                    Parser.tokens.selectNext()
                else:
                    raise ValueError("ERROR")
            else:
                raise ValueError("ERROR")
        
        elif(Parser.tokens.actual.type == "printf"):

            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "openParentheses"):
                Parser.tokens.selectNext()
                node = Printf("printf", [Parser.parseExpression()])
                if(Parser.tokens.actual.type == "closeParentheses"):
                    Parser.tokens.selectNext()
                    if(Parser.tokens.actual.type == "semicolon"):
                        Parser.tokens.selectNext()
                    else:
                        raise ValueError("ERROR")
                else:
                    raise ValueError("ERROR")
            else:
                raise ValueError("ERROR")
        
        elif(Parser.tokens.actual.type == "semicolon"):
            node = NoOp(0,[])
            Parser.tokens.selectNext()
        
        else:
            raise ValueError("ERROR")

        return node
         

    @staticmethod
    def parseFactor():
        # consome os tokens do tokenizer e analisa se a sintaze esta aderente
        # a gramatica proposta retorna o resultado da expressão analisada
        if(Parser.tokens.actual.type == "numeric"):
            node = IntVal(Parser.tokens.actual.value, [])
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

        elif(Parser.tokens.actual.type == "openParentheses"):
            Parser.tokens.selectNext()
            node = Parser.parseExpression()
            if(Parser.tokens.actual.type == "closeParentheses"):
                Parser.tokens.selectNext()
            else:
                raise ValueError("ERROR")

        else:
            raise ValueError("ERROR")

        return node

    @staticmethod
    def parseTerm():
       # consome os tokens do tokenizer e analisa se a sintaze esta aderente
        # a gramatica proposta retorna o resultado da expressão analisada

        node = Parser.parseFactor()

        while((Parser.tokens.actual.type == "mult" or Parser.tokens.actual.type == "div")):

            if(Parser.tokens.actual.type == "mult"):
                Parser.tokens.selectNext()
                node = BinOp('*', [node, Parser.parseFactor()])

            elif(Parser.tokens.actual.type == "div"):
                Parser.tokens.selectNext()
                node = BinOp('/', [node, Parser.parseFactor()])

        return node

    @staticmethod
    def parseExpression():
        # consome os tokens do tokenizer e analisa se a sintaze esta aderente
        # a gramatica proposta retorna o resultado da expressão analisada

        node = Parser.parseTerm()

        while((Parser.tokens.actual.type == "minus" or Parser.tokens.actual.type == "plus")):

            if(Parser.tokens.actual.type == "minus"):
                Parser.tokens.selectNext()
                node = BinOp('-', [node, Parser.parseTerm()])

            elif(Parser.tokens.actual.type == "plus"):
                Parser.tokens.selectNext()
                node = BinOp('+', [node, Parser.parseTerm()])

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
            raise ValueError("ERROR")
        return result.Evaluate()


if(len(sys.argv) <= 1):
    raise ValueError("ERROR")


arg = str(sys.argv[1])
Parser.run(arg)
