import sys


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Tokenizer:
    def __init__(self, origin, position, actual):
        self.origin = origin
        self.position = position
        self.actual = actual

    def selectNext():
        print("le o proximo token e atualiza o atributo atual")


class Parser:
    token = None

    def parseExpression():
        print("consome os tokens do tokenizer e analisa se a sintaze esta aderente a gramatica proposta retorna o resultado da expressão analisada")

    def run(code):
        print("receve o codigo fonte como argumento, inicializa im objeto tokenizador e retorna o resultado do parse expression(). Esse metodo serpa chamado pelo main()")
