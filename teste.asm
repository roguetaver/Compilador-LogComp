; constantes
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
PUSH DWORD 0
MOV EBX, 2
MOV [EBP-8], EBX
PUSH DWORD 0
MOV EBX, 3
MOV [EBP-12], EBX
LOOP_20:
PUSH EBX
POP EAX
MOV EBX, 6
MOV EBX, 6
CMP EAX, EBX
CALL binop_jl
MOV EBX, 6
CMP EBX, False
JE EXIT_20
PUSH EBX
POP EAX
MOV EBX, 1
MOV EBX, 1
ADD EAX, EBX
MOV EBX, EAX
MOV EBX, 1
MOV [EBP-12], EBX
PUSH EBX
CALL print
POP EBX
JMP LOOP_20
EXIT_20:
PUSH EBX
POP EAX
MOV EBX, 3
MOV EBX, 3
CMP EAX, EBX
CALL binop_jg
MOV EBX, 3
CMP EBX, False
JE EXIT_27
PUSH EBX
CALL print
POP EBX
EXIT_27:
POP EBP 
MOV EAX, 1 
INT 0x80 
