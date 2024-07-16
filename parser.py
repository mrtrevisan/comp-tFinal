import sys

class Grammar:
    def __init__(self, start_symbol : str, non_terminals : list[str], terminals : list[str], rules : dict[str, list[str]]):
        self.start_symbol = start_symbol
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.rules = rules

    # retorna a substring terminal (mais a esquerda) na string passada
    def get_terminal_substring(self, str : str) -> str:
        for i, char in enumerate(str):
            if char in self.non_terminals:
                return str[:i]
        return str

    # chama a função de parsing recursiva e printa as derivações
    def parse(self, word : str) -> bool:
        derivation : list[str] = []
        curr_word = ""
        ok = self._parse_recursive(self.start_symbol, word, derivation)

        print()
        for d in derivation:
            print(f'[*] Ação: ', d)
            curr_word = curr_word.replace(d.split(' -> ')[0], d.split(' -> ')[1]) if curr_word else d.split(' -> ')[1] 
            print(f'\t{curr_word}')
        return ok

    # função de parsing resursivo
    def _parse_recursive(self, current_symbol : str, remaining_word : str, derivation : list[str]) -> bool:
        # se acabou a palavra e os símbolos não-terminais
        # aceita
        if not remaining_word and not current_symbol:
            return True

        # calcula os símbolos terminais esperados para o não terminal
        expected = list(map(self.get_terminal_substring, self.rules.get(current_symbol, [])))

        # acabou a palavra mas resta um símbolo não-terminal
        # verifica se esse símbolo deriva para vazio
        # se sim, aceita
        # se não, emite mensagem de erro e rejeita
        if not remaining_word:
            if '&' in self.rules.get(current_symbol, []):
                derivation.append(f"{current_symbol} -> &")
                return True
            else:
                print("[!] Esperado algum símbolo: ", expected)
                return False
        
        # encontrou caracter inesperado na entrada
        # emite mensagem de erro
        # descarta o caracter e continua... mas não aceita
        if current_symbol and not remaining_word.startswith(tuple(expected)):
            print("[!] Caracter inesperado na entrada: ", remaining_word[0])
            
            self._parse_recursive(current_symbol, remaining_word[1:], derivation)
            return False
        
        # processa derivações
        for rule in self.rules.get(current_symbol, []):
            # derivação para vazio
            if rule == '&':
                # verifica o resto da palavra
                derivation.append(f"{current_symbol} -> &")
                if self._parse_recursive('', remaining_word, derivation):
                    # derivação válida para vazio, retorna true
                    return True
                else:
                    # não pode derivar para vazio aqui
                    derivation.pop()
            
            # derivação para símbolo
            else:
                # calcula o fim dos terminais na derivação
                terminal_end = 0
                while rule[terminal_end] in self.terminals:
                    terminal_end += 1

                # se a derivação é aplicável
                if remaining_word.startswith(rule[0:terminal_end]):
                    derivation.append(f"{current_symbol} -> {rule}")
                    # calcula o novo símbolo
                    new_current_symbol = rule[terminal_end:] if len(rule) > terminal_end else ''
                    # continua
                    return self._parse_recursive(new_current_symbol + current_symbol[1:], remaining_word[terminal_end:], derivation)
        
        # se nada der certo, não aceita
        return False

# lê a gramática do arquivo e retorna em um objeto Grammar
def read_grammar(file_path : str) -> Grammar:
    # abre o arquivo para leitura
    with open(file_path, 'r') as file:
        # pega as linhas
        lines = file.readlines()

        # símbolo inicial
        start_symbol = lines[0].strip()

        # símbolos não terminais
        non_terminals_line = lines[1].strip().strip('[]')
        non_terminals = non_terminals_line.split(', ')

        # símbolos terminais
        terminals_line = lines[2].strip().strip('[]')
        terminals = terminals_line.split(', ')
        
        # regras
        rules = {}
        all_symbols = set(non_terminals + terminals)
        # para cada linha de derivações
        for line in lines[3:]:
            lhs, rhs = line.strip().split(' -> ')
            # verifica se o símbolo não terminal está declarado
            if lhs not in all_symbols:
                raise ValueError(f"Símbolo não terminal'{lhs}' na regra não está na lista de símbolos definidos.")
            
            # e se os símbolos terminais estão declarados
            rhs_symbols = list(rhs)
            for symbol in rhs_symbols:
                if symbol != '&' and symbol not in all_symbols:
                    raise ValueError(f"Símbolo '{symbol}' na regra não está na lista de símbolos definidos.")
                
            # verifica também se a gramática é GLD
            for i in range(len(rhs_symbols) -1):
                if rhs_symbols[i] in non_terminals:
                    raise ValueError("A gramática deve ser GLD (Gramática Linear à Direita).")
                
            # monta o dict de regras
            if lhs not in rules:
                rules[lhs] = []
            rules[lhs].append(rhs)

        # ordena de modo a garantir que as derivações para vazio estão ao final de cada regra
        rules = {key: sorted(values, key=lambda x: (x == '&', x)) for key, values in rules.items()}

        return Grammar(start_symbol, non_terminals, terminals, rules)

# main
def main() -> None:
    # o nome do arquivo da gramática é passado como argumento
    if len(sys.argv) < 2:
        print("Uso: python parser.py <arquivo_gramatica>")
        sys.exit(1)

    try:
        grammar_file = sys.argv[1]
        grammar = read_grammar(grammar_file)
    except ValueError as e:
        print(f"Erro ao ler gramática: {e}")
        sys.exit(1)

    # a palavra é passada via command line
    word = input("Insira a palavra: ")

    if grammar.parse(word):
        print(f"\n-> A palavra '{word}' é aceita pela gramática.")
    else:
        print(f"\n-> A palavra '{word}' NÃO é aceita pela gramática.")

    return

if __name__ == "__main__":
    main()