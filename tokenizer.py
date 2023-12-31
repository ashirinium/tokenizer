# pylint: disable=locally-disabled, multiple-statements, fixme, line-too-long, 
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=too-many-return-statements, too-many-branches, too-many-statements, too-many-locals
# pylint: disable=invalid-name

punctuators = [',', ';', ':', '(', ')', '{', '}', '[', ']', "==", "!=", "<=", ">=", "+=", "-=", "*=", "/=", "++", "--", "+", "-", "*", "/", "%", "<", ">", "=", "!", "&", "|", "^", "~", "<<", ">>", "&&", "||", "?", ":", "."]

def is_numeric(str_input: str):
    if str_input.isdigit():
        return True
    if str_input[0] == '.' and str_input[1:].isdigit():
        return True
    if str_input[0] == '-' and str_input[1:].isdigit():
        return True
    if str_input[0].isdigit() and str_input[1] == '.' and str_input[2:].isdigit():
        return True
    return False

def handle_string_literal(idx, s):
    #assumes the first " has already been handled"
    if s[idx] == '"':
        return ''
    curr = s[idx]
    return curr + handle_string_literal(idx + 1, s)

def handle_retarded_single_quote(idx, s, nxt):
    curr = s[idx]
    if nxt == "\\":
        return f"{curr}{nxt}{s[idx + 1:idx + 4]}"
    return f"{curr}{s[idx + 1:idx + 3]}"

def skip_whitespace(idx, s):
    while idx < len(s) and s[idx] in (' ', '\n', '\t'):
        idx += 1
    return idx

def get_next_token(start_index, str_input, prev_tokn=''):
    if start_index >= len(str_input):
        return start_index, ''

    start_index = skip_whitespace(start_index, str_input)
    curr = str_input[start_index]
    nxt = str_input[start_index + 1] if start_index + 1 < len(str_input) else ''
    curr_tokn = curr + nxt if curr + nxt in punctuators else curr

    if (prev_tokn+curr_tokn).isdigit() and nxt == '.' or curr == '.' and nxt.isdigit():
        _, next_tok = get_next_token(start_index + 2, str_input, prev_tokn+curr+nxt)
        if next_tok[0].isdigit():
            return start_index, f"{curr}{nxt}{next_tok}"
    if curr == "'":
        return start_index, handle_retarded_single_quote(start_index, str_input, nxt)

    if curr == '"':
        return start_index, f"\"{handle_string_literal(start_index+1, str_input)}\"" #because I am retarded

    if curr_tokn in punctuators:
        return start_index, curr_tokn

    if nxt in punctuators or nxt in (' ', '\n', '\t', "'"):
        return start_index, curr
    _, next_word = get_next_token(start_index + len(curr_tokn), str_input, prev_tokn+curr_tokn)
    return start_index, curr + next_word


def tokenize(str_input) -> [str]:
    tokens = []
    curr_idx = 0
    while curr_idx < len(str_input):
        i, token = get_next_token(curr_idx, str_input)
        tokens.append(token)
        curr_idx = i + len(token)
    return tokens
