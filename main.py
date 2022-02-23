import sys


class Token:
    def __init__(self, type, value):
        self.type = type  # tipo do token
        self.value = value  # valor do token


class Tokenizer:
    def __init__(self, origin):
        self.origin = origin  # codigo fonte que sera tokenizado
        self.position = 0  # posição atual que o tokenizador está separando
        self.actual = None  # o ultimo token separando

    def selectNext(self):
        # le o proximo token e atualiza o atributo atual
        # TIRAR OS ESPAÇOS AQUI

        if(self.origin[self.position] == '+'):
            self.position += 1
            actual = Token('plus', 0)
            return actual
        elif(self.origin[self.position] == '-'):
            actual = Token('minus', 0)
            return actual
        elif(self.position >= len(self.origin)):
            actual = Token('EOF', 0)
            return actual
        elif(self.origin[self.position].isnumeric()):
            cadidato = self.origin[self.position]
            self.position += 1
            while(self.origin[self.position.isnumeric()]):
                cadidato += self.origin[self.position]
                self.position += 1
            actual = Token('numeric', cadidato)
            return actual
        else:
            raise ValueError("ERROR")


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
                        Pegar próximo token(selectNext())
                        Se o token atual for número:
                            Somar o número no resultado
                        Senão ERRO
                    Se o token atual é -:
                        Pegar próximo token(selectNext())
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


if(len(sys.argv) <= 1):
    raise ValueError("ERROR")

arg = str(sys.argv[1])
