Trabalho Final - Compiladores

Alunos:  
Alfredo Cossetin Neto  
Mauro Roberto Machado Trevisan

Para usar:  
$ python3 parser.py grammar.txt  

Então insira a palavra via terminal

O arquivo grammar.txt deve seguir o modelo:  
L1: Símbolo inicial  
L2: Símbolos não terminais  
L3: Símbolos terminais  
L4 ... : Regras de derivação.

Não é suportado o uso de 'ou', '|', para as regras de derivação, logo cada regra deve ser descrita exclusivamente no formato "Estado -> terminaisNovoEstado"

Definição formal do arquivo grammar.txt:

G = (V, T, P, S)

V (Símbolos Não Terminais): { S, A, A', B, B', C, R, R', I, N, T }
T (Símbolos Terminais): { símbolo inicial, símbolos não terminais, símbolos terminais, \n, ], [, -> }
P (Regras de Produção):
  S → I \n A
  A → [A'] \n B
  A' → N | N,A'
  B → [B'] \n C
  B' → T | T,B'
  C → R | R \n C
  R → N -> R' | N -> R'N
  R' → T | TR'
  I → símbolo inicial
  N → símbolos não terminais
  T → símbolos terminais
