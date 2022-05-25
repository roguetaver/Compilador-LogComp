# Compilador-LogComp

Compilador da disciplina Logica Computacional
Feito por André Tavernaro

![git status](http://3.129.230.99/svg/roguetaver/Compilador-LogComp/)

Roteiro 9 - ATUAL

![Alt text](diagrama-roteiro9.jpeg?raw=true "Diagrama Sintático Roteiro 9")
![Alt text](diagrama-roteiro9-2.jpeg?raw=true "Diagrama Sintático Roteiro 9")


Roteiro 6 - OK

![Alt text](diagrama-roteiro6.jpeg?raw=true "Diagrama Sintático Roteiro 6")
![Alt text](diagrama-roteiro6-2.jpeg?raw=true "Diagrama Sintático Roteiro 6")

```
BLOCK = "{" , { STATEMENT }, "}" ;
STATEMENT = ( λ | ASSIGNMENT | PRINT | BLOCK | WHILE | IF), ";" ;
FACTOR = NUMBER | IDENTIFIER | (("+" | "-" | "!") , FACTOR) | "(" , RELEXPRESSION , ")" | SCANF;
TERM = FACTOR, { ("*" | "/" | "&&"), FACTOR } ;
EXPRESSION = TERM, { ("+" | "-" | "||"), TERM } ;
RELEXPRESSION = EXPRESSION , {("<" | ">" | "==") , EXPRESSION } ;
WHILE = "while", "(", RELEXPRESSION ,")", STATEMENT;
IF = "if", "(", RELEXPRESSION ,")", STATEMENT, (("else", STATEMENT) | λ );
ASSIGNMENT = IDENTIFIER, "=" , EXPRESSION ;
PRINT = "printf", "(" , EXPRESSION, ")" ;
SCANF = "scanf", "(", ")" ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT , { DIGIT } ;
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
```

Roteiro 5 - OK

![Alt text](diagrama-roteiro5.png?raw=true "Diagrama Sintático Roteiro 5 (OK)")
![Alt text](EBNF-roteiro5.png?raw=true "EBNF Roteiro 5 (OK)")

Roteiro 4 - OK

![Alt text](diagrama-roteiro3.png?raw=true "Diagrama Sintático Roteiro 4 (OK)")
![Alt text](EBNF-roteiro3.png?raw=true "EBNF Roteiro 4 (OK)")

Roteiro 3 - OK

![Alt text](diagrama-roteiro3.png?raw=true "Diagrama Sintático Roteiro 3")
![Alt text](EBNF-roteiro3.png?raw=true "EBNF Roteiro 3")

Roteiro 2 -OK

![Alt text](diagrama-roteiro2.png?raw=true "Diagrama Sintático Roteiro 2")

Roteiro 1 - OK

![Alt text](diagrama-roteiro1.png?raw=true "Diagrama Sintático Roteiro 1")
