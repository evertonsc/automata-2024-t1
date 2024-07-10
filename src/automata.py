"""Implementação de autômatos finitos."""

def load_automata(filename):
    """
    Lê os dados de um autômato finito a partir de um arquivo.

    A estrutura do arquivo deve ser:

    <lista de símbolos do alfabeto, separados por espaço (' ')>
    <lista de nomes de estados>
    <lista de nomes de estados finais>
    <nome do estado inicial>
    <lista de regras de transição, com "origem símbolo destino">

    Um exemplo de arquivo válido é:

    a b
    q0 q1 q2 q3
    q0 q3
    q0
    q0 a q1
    q0 b q2
    q1 a q0
    q1 b q3
    q2 a q3
    q2 b q0
    q3 a q1
    q3 b q2

    Caso o arquivo seja inválido uma exceção Exception é gerada.
    """
    with open(filename, "rt") as arquivo:
        lines = arquivo.readlines()

        if len(lines) < 5:
            raise Exception("Formato de arquivo inválido: linhas insuficientes.")

        Sigma = lines[0].strip().split()
        Q = lines[1].strip().split()
        F = lines[2].strip().split()
        q0 = lines[3].strip()

        delta = {}
        for line in lines[4:]:
            parts = line.strip().split()
            if len(parts) != 3:
                raise Exception("Formato de transição inválido.")
            origem, simbolo, destino = parts
            if origem not in Q or destino not in Q or simbolo not in Sigma:
                raise Exception("Transição contém estado ou símbolo inválido.")
            if origem not in delta:
                delta[origem] = {}
            delta[origem][simbolo] = destino

        if q0 not in Q:
            raise Exception("Estado inicial não está na lista de estados.")
        for f in F:
            if f not in Q:
                raise Exception("Estado final não está na lista de estados.")

        return Q, Sigma, delta, q0, F

def process(automata, words):
    """
    Processa a lista de palavras e retorna o resultado.

    Os resultados válidos são ACEITA, REJEITA, INVALIDA.
    """
    Q, Sigma, delta, q0, F = automata
    results = {}

    for word in words:
        current_state = q0
        is_valid = True
        for symbol in word:
            if symbol not in Sigma:
                results[word] = "INVALIDA"
                is_valid = False
                break
            if current_state not in delta or symbol not in delta[current_state]:
                current_state = None
                break
            current_state = delta[current_state][symbol]

        if not is_valid:
            continue

        if current_state is None or current_state not in F:
            results[word] = "REJEITA"
        else:
            results[word] = "ACEITA"

    return results
