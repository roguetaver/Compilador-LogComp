import sys
import re


class Token:
    def __init__(self, type, value):
        self.type = type  # tipo do token
        self.value = value  # valor do token


class PrePro:
    @staticmethod
    def filter(code):
        return re.sub("/\*.*?\*/", "", code)


class Tokenizer:
    def __init__(self, origin):
        self.origin = origin  # codigo fonte que sera tokenizado
        self.position = 0  # posição atual que o tokenizador está separando
        self.actual = None  # o ultimo token separando

    def selectNext(self):
        # le o proximo token e atualiza o atributo atual
        if(self.position >= len(self.origin)):
            self.actual = Token("EOF", 0)
            return self.actual

        while(self.origin[self.position] == " "):
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

        elif(self.origin[self.position].isnumeric()):
            cadidato = self.origin[self.position]
            self.position += 1
            if(self.position < len(self.origin)):
                while(self.origin[self.position].isnumeric()):
                    cadidato += self.origin[self.position]
                    self.position += 1
                    if(self.position >= len(self.origin)):
                        break
            self.actual = Token("numeric", int(cadidato))
            return self.actual

        else:
            raise ValueError("ERROR")


class Parser:
    tokens = None  # objeto da classe que era ler o codigo fonte e alimentar o analisador

    @staticmethod
    def parseFactor():
        # consome os tokens do tokenizer e analisa se a sintaze esta aderente
        # a gramatica proposta retorna o resultado da expressão analisada

        if(Parser.tokens.actual.type == "numeric"):
            resultado = Parser.tokens.actual.value
            Parser.tokens.selectNext()

        elif(Parser.tokens.actual.type == "minus"):
            Parser.tokens.selectNext()
            resultado = -Parser.parseFactor()

        elif(Parser.tokens.actual.type == "plus"):
            Parser.tokens.selectNext()
            resultado = Parser.parseFactor()

        elif(Parser.tokens.actual.type == "openParentheses"):
            Parser.tokens.selectNext()
            resultado = Parser.parseExpression()
            if(Parser.tokens.actual.type == "closeParentheses"):
                Parser.tokens.selectNext()
            else:
                raise ValueError("ERROR")

        else:
            raise ValueError("ERROR")

        return resultado

    @staticmethod
    def parseTerm():
       # consome os tokens do tokenizer e analisa se a sintaze esta aderente
        # a gramatica proposta retorna o resultado da expressão analisada
        resultado = Parser.parseFactor()

        while((Parser.tokens.actual.type == "mult" or Parser.tokens.actual.type == "div")):

            if(Parser.tokens.actual.type == "mult"):
                Parser.tokens.selectNext()
                resultado *= Parser.parseFactor()

            elif(Parser.tokens.actual.type == "div"):
                Parser.tokens.selectNext()
                resultado //= Parser.parseFactor()

        return resultado

    @staticmethod
    def parseExpression():
        # consome os tokens do tokenizer e analisa se a sintaze esta aderente
        # a gramatica proposta retorna o resultado da expressão analisada
        resultado = Parser.parseTerm()

        while((Parser.tokens.actual.type == "minus" or Parser.tokens.actual.type == "plus")):

            if(Parser.tokens.actual.type == "minus"):
                Parser.tokens.selectNext()
                resultado -= Parser.parseTerm()

            elif(Parser.tokens.actual.type == "plus"):
                Parser.tokens.selectNext()
                resultado += Parser.parseTerm()

        return resultado

    def run(code):
        # receve o codigo fonte como argumento, inicializa um objeto tokenizador e
        # retorna o resultado do parse expression(). Esse metodo sera chamado pelo main()
        postProCode = PrePro.filter(code)
        Parser.tokens = Tokenizer(postProCode)
        Parser.tokens.selectNext()

        result = Parser.parseExpression()
        if(Parser.tokens.actual.type != "EOF"):
            raise ValueError("ERROR")
        return result


if(len(sys.argv) <= 1):
    raise ValueError("ERROR")

arg = str(sys.argv[1])
print(Parser.run(arg))
