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

Nao e suportado o uso de 'ou','|' para as regras de derivacao, logo cada regra deve ser descrita exclusivamente no formato "Estado -> *terminais*NovoEstado"
