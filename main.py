import sys


class Token:
    def __init__(self, type, value):
        self.type = type  # tipo do token
        self.value = value  # valor do token


class Tokenizer:
    def __init__(self, origin, position, actual):
        self.origin = origin  # codigo fonte que sera tokenizado
        self.position = position  # posição atual que o tokenizador está separando
        self.actual = actual  # o ultimo token separando

    def selectNext():
        # le o proximo token e atualiza o atributo atual
        '''
        se origin[position] == '+' 
            position ++
            actual  = Token('','plus')
            return actual
        se origin[position] == '-'
            actual = Token('','minus')
            return actual
        se position >= len(origin)
            actual = token('','eof')
        se origin[position] is numeric
            candidato = origin[position]
            position ++
            enquanto origin [position] is numeric
                candidato = origin[position]
                position++
        else raise error

        [TRATAR ESPAÇOS]
        '''
        print("hello")


class Parser:
    tokens = None  # objeto da classe que era ler o codigo fonte e alimentar o analisador

    def parseExpression():
        # consome os tokens do tokenizer e analisa se a sintaze esta aderente
        # a gramatica proposta retorna o resultado da expressão analisada
        '''
        Se o token atual for número:
        Copiar número para o resultado
        Pegar próximo token
        Enquanto token for + ou -:
        Se o token atual é +:
        Pegar próximo token
        Se o token atual for número:
        Somar o número no resultado
        Senão ERRO
        Se o token atual é -:
        Pegar próximo token
        Se o token atual for número:
        Subtrair o número no resultado
        Senão ERRO
        Pegar próximo token
        Retornar resultado
        Senão ERRO
        '''

        print("hello")

    def run(code):
        # receve o codigo fonte como argumento, inicializa um objeto tokenizador e
        # retorna o resultado do parse expression(). Esse metodo serpa chamado pelo main()

        print("hello")
