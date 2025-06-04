def is_balanced_ab_turing(tape_input, debug=False):
    tape = list(tape_input) + ['_']
    head = 0
    state = 'START'

    while True:
        if debug:
            print(f"[{state}] HEAD={head}, TAPE={''.join(tape)}")

        if state == 'START':
            # cauta primul 'a' sau 'b' nemarcat
            while head < len(tape) and tape[head] in ('X', 'Y'):
                head += 1

            if tape[head] == '_':
                return True  # toate caracterele au fost pereche

            if tape[head] == 'a':
                tape[head] = 'X'
                state = 'MATCH_b'
                head += 1
            elif tape[head] == 'b':
                tape[head] = 'Y'
                state = 'MATCH_a'
                head += 1
            else:
                return False  # caracter invalid

        elif state == 'MATCH_b':
            while tape[head] in ('a', 'X', 'Y'):
                head += 1
                if head >= len(tape):
                    return False  # nu s-a gasit pereche

            if tape[head] == 'b':
                tape[head] = 'Y'
                state = 'REWIND'
                head -= 1
            else:
                return False  # nu e pereche valida

        elif state == 'MATCH_a':
            while tape[head] in ('b', 'X', 'Y'):
                head += 1
                if head >= len(tape):
                    return False

            if tape[head] == 'a':
                tape[head] = 'X'
                state = 'REWIND'
                head -= 1
            else:
                return False

        elif state == 'REWIND':
            while head >= 0 and tape[head] != '_':
                head -= 1
            head += 1
            state = 'START'

def read_lines_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.rstrip('\n') for line in f]

lines = read_lines_from_file("input.txt")

for line in lines:
    if not line.strip():
        print("Nu este echilibrat")
        continue
    result = is_balanced_ab_turing(line, debug=False)
    print(f"{line:10} -> {'Echilibrat' if result else 'Nu este echilibrat'}")
