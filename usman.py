def word_generator(index, file_input):
    word = ""
    punctuators = [",", ";", ":", "(", ")", "{", "}", "[", "]"]
    all_digits = True

    while index < len(file_input):
        curr = file_input[index]
        nxt = ""
        if index + 1 < len(file_input): nxt = file_input[index + 1]

        if curr == " ":
            index += 1
            if len(word) > 0: return index, word
            continue

        elif curr == "\n":
            index += 1
            if len(word) > 0: return index, word
            continue

        elif curr in punctuators:
            if len(word) > 0: return index, word
            return index + 1, curr

        elif curr == "+" or curr == "-":
            if len(word) > 0: return index, word
            if nxt == "=" or nxt == curr: return index + 2, curr + nxt
            return index + 1, curr

        elif curr == "*" or curr == "%" or curr == "<" or curr == ">" or curr == "=" or curr == "!":
            if len(word) > 0: return index, word
            if nxt == "=": return index + 2, curr + nxt
            return index + 1, curr

        elif curr == "/":
            if len(word) > 0: return index, word
            if nxt == "=": return index + 2, curr + nxt
            if nxt == "/":
                while curr != "\n" and index < len(file_input):
                    curr = file_input[index]
                    index += 1
                continue 
            if nxt == "*":
                index += 2
                curr = file_input[index]
                nxt = file_input[index + 1]
                while (curr != "*" or nxt != "/") and index < len(file_input):
                    curr = file_input[index]
                    nxt = file_input[index + 1]
                    index += 1
                index += 2
                continue
            return index + 1, curr     

        elif curr == ".":
            if not (all_digits and nxt.isdigit()):
                if len(word) > 0: return index, word
                return index + 1, curr 

        elif curr == "\'": # 'a \n?
            if len(word) > 0: return index, word
            third = fourth = ""
            if index + 2 < len(file_input): third = file_input[index + 2]
            if index + 3 < len(file_input): fourth = file_input[index + 3]
            if nxt == "\\":
                word = curr + nxt + file_input[index + 2] + file_input[index + 3]
                return index + 4, word
            else: 
                word = curr + nxt + file_input[index + 2]
                return index + 3, word

        elif curr == "\"":
            if len(word) > 0: return index, word
            word += curr
            index += 1
            curr = file_input[index]
            while curr != "\"" and index < len(file_input):
                curr = file_input[index]
                if curr == "\n": return index, word
                word += curr
                index += 1
            return index, word
            
        all_digits = all_digits and curr.isdigit()
        word += curr
        index += 1

    return index, word


TEST = '''== void class A_B_C: 35
int a=b==++==6
while(a<===b!!!=+-**55)
{{
    c="abc+=56"abc_d
c='a'+'bcd'+'

9.9abc95.68.b8c.d'''
# Driver code
def driver_code(file_name):
    index = 0
    while index < len(TEST):
        index, word = word_generator(index, TEST)
        print(word)

driver_code("code.txt")