class Grammar:
    def __init__(self, start_symbol, non_terminals, terminals, rules):
        self.start_symbol = start_symbol
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.rules = rules

    def parse(self, word):
        derivation = []
        curr_word = ""
        if self._parse_recursive(self.start_symbol, word, derivation):
            for d in derivation:
                print('Derivação: ', d)
                curr_word = curr_word.replace(d.split(' -> ')[0], d.split(' -> ')[1]) if curr_word else d.split(' -> ')[1] 
                print(curr_word)

            return True
        else:
            return False

    def _parse_recursive(self, current_symbol, remaining_word, derivation):
        if not remaining_word and not current_symbol:
            return True

        if not remaining_word:
            if '&' in self.rules.get(current_symbol, []):
                derivation.append(f"{current_symbol} -> &")
                return True
            return False

        for rule in self.rules.get(current_symbol, []):
            if rule == '&':
                derivation.append(f"{current_symbol} -> &")
                if self._parse_recursive('', remaining_word, derivation):
                    return True
                derivation.pop()
            elif remaining_word.startswith(rule[0]):
                derivation.append(f"{current_symbol} -> {rule}")

                new_current_symbol = rule[1:] if len(rule) > 1 else ''
                if self._parse_recursive(new_current_symbol + current_symbol[1:], remaining_word[1:], derivation):
                    return True
                derivation.pop()

        return False

def read_grammar(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        start_symbol = lines[0].strip()
        
        non_terminals_line = lines[1].strip().strip('[]')
        non_terminals = non_terminals_line.split(', ')
        
        terminals_line = lines[2].strip().strip('[]')
        terminals = terminals_line.split(', ')
        
        rules = {}
        
        # Verificar se todos os símbolos nas regras estão corretos
        all_symbols = set(non_terminals + terminals)
        
        for line in lines[3:]:
            lhs, rhs = line.strip().split(' -> ')

            if lhs not in all_symbols:
                raise ValueError(f"Símbolo '{lhs}' na regra não está na lista de símbolos definidos.")
            
            rhs_symbols = list(rhs)
            for symbol in rhs_symbols:
                if symbol != '&' and symbol not in all_symbols:
                    raise ValueError(f"Símbolo '{symbol}' na regra não está na lista de símbolos definidos.")
                
            for i in range(len(rhs_symbols) -1):
                if rhs_symbols[i] in non_terminals:
                    raise ValueError("A gramática deve ser GLD (Gramática Linear à Direita).")
                
            if lhs not in rules:
                rules[lhs] = []
            rules[lhs].append(rhs)
        
        return Grammar(start_symbol, non_terminals, terminals, rules)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Uso: python parser.py <arquivo_gramatica> <palavra>")
        sys.exit(1)

    grammar_file = sys.argv[1]
    word = sys.argv[2]

    try:
        grammar = read_grammar(grammar_file)
    except ValueError as e:
        print(f"Erro ao ler gramática: {e}")
        sys.exit(1)

    if grammar.parse(word):
        print(f"A palavra '{word}' é aceita pela gramática.")
    else:
        print(f"A palavra '{word}' não é aceita pela gramática.")
