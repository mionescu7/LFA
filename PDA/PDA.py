def pda_balanced_parentheses(input_string, debug=False):
    stack = []
    for i, ch in enumerate(input_string):
        if debug:
            print(f"i={i}, char={ch}, stack={stack}")
        if ch == '(':
            stack.append('(')
        elif ch == ')':
            if not stack:
                return False
            stack.pop()
        else:
            return False  # caracter invalid
    return len(stack) == 0


def read_lines_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


lines = read_lines_from_file("input.txt")

for line in lines:
    result = pda_balanced_parentheses(line, debug=False)
    print(f"{line:10} -> {'CORECT' if result else 'INCORECT'}")
