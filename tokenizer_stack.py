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

def tokenize(str_input: str) -> [str]:
    delimiters_pattern = f'({"|".join(map(re.escape, word_breakers))})'
    result = re.split(delimiters_pattern, str_input)
    cleaned = [r for r in result if r.strip()]
    cleaned.reverse()
    return get_tokens(cleaned)

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

def get_tokens(word_list: [str]) -> [str]:
    if len(word_list) <= 1:
        return word_list
    top = word_list.pop()
    peek = word_list[-1]

    if top+peek in double_breakers:
        return [top+word_list.pop()] + get_tokens(word_list)

    if top.isdigit() and peek == ".":
        next_token = word_list[-2]
        if next_token[0].isdigit():
            word_list.pop()
            word_list.pop()
            return [top + peek + next_token] + get_tokens(word_list)

    if top == "." and peek[0].isdigit():
        return [top + word_list.pop()] + get_tokens(word_list)

    if top == "'":
        if peek == "\\":
            peek = word_list.pop()
            first, second = extract_next_two_chars(word_list)
            return [top + peek + first + second] + get_tokens(word_list)
        first, second = extract_next_two_chars(word_list)
        return [top + first + second] + get_tokens(word_list)

    if top == '"':
        word = word_list.pop()
        while word != '"':
            top += word
            word = word_list.pop()
        return [top+word] + get_tokens(word_list)

    return [top] + get_tokens(word_list)