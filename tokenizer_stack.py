#pylint: disable=missing-function-docstring
#pylint: disable=missing-module-docstring
#pylint: disable=too-many-return-statements, too-many-branches, too-many-statements, too-many-locals, line-too-long

import re

TEST = '''== void class A_B_C: 35
int a=b==++==6
while(a<===b!!!=+-**55)
{{
    c="abc+=56"abc_d
c='a'+'bcd'+'

9.9abc95.68.b8c.d'''

word_breakers = ['\n', " ", ":", "=", "+", "-", "*", "/", "%", "<", ">", "!", "&", "|", "^", "~", "?", ".", ",", ";", "(", ")", "{", "}", "[", "]", "'", "\""]
double_breakers = ["==", "!=", "<=", ">=", "+=", "-=", "*=", "/=", "++", "--", "<<", ">>", "&&", "||", "!"]

def get_tokens(str_input: str):
    delimiters_pattern = f'({"|".join(map(re.escape, word_breakers))})'
    result = re.split(delimiters_pattern, str_input)
    cleaned = [r for r in result if r.strip()]
    cleaned.reverse()
    return cleaned

def tokenize(word_list: [str]):
    if len(word_list) <= 1:
        return word_list
    top = word_list.pop()
    peek = word_list[-1]

    if top+peek in double_breakers:
        return [top+word_list.pop()] + tokenize(word_list)

    if top.isdigit() and peek == ".":
        next_token = word_list[-2]
        if next_token[0].isdigit():
            word_list.pop()
            word_list.pop()
            return [top + peek + next_token] + tokenize(word_list)

    if top == "." and peek[0].isdigit():
        return [top + word_list.pop()] + tokenize(word_list)

    if top == "'":
        if peek == "\\":
            peek = word_list.pop()
            first, second = extract_next_two_chars(word_list)
            return [top + peek + first + second] + tokenize(word_list)
        first, second = extract_next_two_chars(word_list)
        return [top + first + second] + tokenize(word_list)

    if top == '"':
        word = word_list.pop()
        while word != '"':
            top += word
            word = word_list.pop()
        return [top+word] + tokenize(word_list)

    return [top] + tokenize(word_list)


def extract_next_two_chars(stack: [str]):
    word   = stack.pop()
    first  = None
    second = None
    if len(word) > 1:
        first  = word[0]
        second = word[1]
        if word[2:]:
            stack.append(word[2:])
    else:
        first = word
        second = stack.pop()
    return first, second


def get_test_tuples():
    expected_output_str = []
    with open("out.txt", "r", encoding="utf-8") as file:
        expected_output_str = [x.rstrip() for x in file.readlines()]
        file.close()
    return expected_output_str

def run_test(words):
    print("Running test...")
    expected_output = get_test_tuples()
    curr_idx = 0
    for word in words:
        assert word == expected_output[curr_idx], f"Expected {expected_output[curr_idx]} but got {word} instead. Index: {curr_idx}"
        curr_idx += 1
    print("Successfully passed test!")


def main():
    tokens = get_tokens(TEST)
    words = tokenize(tokens)
    run_test(words)
    
    

main()
