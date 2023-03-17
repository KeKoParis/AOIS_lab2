import re


def solve(curr_table, curr_expression, index):  # finds pcnf and pdnf

    curr_expression = replace_negation(curr_table, curr_expression, index)
    curr_expression = replace_positive(curr_table, curr_expression, index)
    curr_expression = replace_signs(curr_expression)

    curr_table[index][3] = solve_expr(curr_expression)  # resolves logical expression

    return curr_table


# !((x1+!x2)*(x2+!x3))
def solve_sub_str(sub_str):
    sub_str = sub_str[1:len(sub_str) - 1]
    if sub_str[0] == '1' and sub_str[1] == 'a' and sub_str[len(sub_str) - 1] == '1':
        return '1'
    if (sub_str[0] == '1' or sub_str[len(sub_str) - 1] == '1') and sub_str[1] == 'o':
        return '1'
    return '0'


# ((x1+x2)*x3)

def solve_expr(curr_expression):
    while re.search(r'\([01]+[or|and]+[01]+\)', curr_expression):
        curr_expression = curr_expression.replace(re.search(r'\([01]+[or|and]+[01]+\)', curr_expression).group(),
                                                  solve_sub_str(
                                                      re.search(r'\([01]+[or|and]+[01]+\)', curr_expression).group()))

    return curr_expression


def replace_negation(curr_table, curr_expression, index):  # replaces negation vars to their values
    while curr_expression.find("!x1") != -1:
        curr_expression = curr_expression.replace("!x1", str(abs(curr_table[index][0] - 1)))
    while curr_expression.find("!x2") != -1:
        curr_expression = curr_expression.replace("!x2", str(abs(curr_table[index][1] - 1)))
    while curr_expression.find("!x3") != -1:
        curr_expression = curr_expression.replace("!x3", str(abs(curr_table[index][2] - 1)))

    return curr_expression


def replace_positive(curr_table, curr_expression, index):  # replaces positive vars to their values
    while curr_expression.find("x1") != -1:
        curr_expression = curr_expression.replace('x1', str(curr_table[index][0]))
        break
    while curr_expression.find("x2") != -1:
        curr_expression = curr_expression.replace("x2", str(curr_table[index][1]))
    while curr_expression.find("x3") != -1:
        curr_expression = curr_expression.replace("x3", str(curr_table[index][2]))

    return curr_expression


def replace_signs(curr_expression):  # replaces signs to their logical equivalent in python
    while curr_expression.find("+") != -1:
        curr_expression = curr_expression.replace("+", "or")
    while curr_expression.find("*") != -1:
        curr_expression = curr_expression.replace("*", "and")
    while curr_expression.find("!") != -1:
        curr_expression = curr_expression.replace("!", "")

    return curr_expression


def find_values_pcnf(curr_row):  # make pcnf form out of table
    new_expression: str = ""
    number = 1
    for i in curr_row:
        if number == 4:
            break
        if i == 0:
            new_expression += "x" + str(number)
        else:
            new_expression += "!x" + str(number)
        number += 1
        if number < 4:
            new_expression += " + "

    return new_expression


def find_values_pdnf(curr_row):  # make pdnf form out of table
    new_expression: str = ""
    number = 1
    for i in curr_row:
        if number == 4:
            break
        if i == 0:
            new_expression += "!x" + str(number)
        else:
            new_expression += "x" + str(number)
        number += 1
        if number < 4:
            new_expression += " * "

    return new_expression


def conv_bin(expr):
    bin_exp = ""
    c = 0
    for i in range(len(expr)):
        if c == 1:
            c = 0
            continue
        if expr[i] == "!":
            c = 1
            bin_exp += "1"
        if expr[i] == "x":
            bin_exp += "0"
    return bin_exp


def conv_dec(curr_row):
    dec = 0
    for i in range(len(curr_row)):
        dec += int(curr_row[i]) * (2 ** (3 - i - 1))

    return str(int(dec))


def convert(curr_table):
    coef = 7
    index = 0
    for i in curr_table:
        index += i[3] * (2 ** coef)
        coef = coef - 1

    return index


def fill_table(curr_table):
    check = 0
    for i in range(8):
        if i < 4:
            curr_table[i][0] = 0
        else:
            curr_table[i][0] = 1

        if check == 4:
            check = 0

        if check < 2:
            curr_table[i][1] = 0
        else:
            curr_table[i][1] = 1

        if i % 2 == 0:
            curr_table[i][2] = 0
        else:
            curr_table[i][2] = 1

        check = check + 1

    return curr_table


def build_pcnf(curr_table):
    pcnf: str = ""
    bin_pcnf = ""
    dec_pcnf = ""
    for row in curr_table:
        if row[3] == 0:
            pcnf += "("
            pcnf += find_values_pcnf(row)
            pcnf += ")*"
            bin_pcnf += conv_bin(find_values_pcnf(row))
            bin_pcnf += " "
            dec_pcnf += conv_dec(row) + " "

    return pcnf, bin_pcnf, dec_pcnf


def build_pdnf(curr_table):
    pdnf: str = ""
    bin_pdnf = ""
    dec_pdnf = ""
    for row in curr_table:
        if row[3] == 1:
            pdnf += "("
            pdnf += find_values_pdnf(row)
            pdnf += ")+"
            bin_pdnf += conv_bin(find_values_pdnf(row))
            bin_pdnf += " "
            curr_pdnf = conv_bin(find_values_pdnf(row))
            dec_pdnf += conv_dec(curr_pdnf) + " "

    return pdnf, bin_pdnf, dec_pdnf


def main():
    table = [[0 for i in range(4)] for j in range(8)]

    table = fill_table(table)

    expression = input("Enter expression: ")
    for i in range(8):
        table = solve(table, expression, i)

    is_reversed = 0
    if expression[0] == '!':
        is_reversed = 1
    for i in table:
        if i[3] == '0':
            if is_reversed == 1:
                i[3] = '1'
            i[3] = int(i[3])
        else:
            if is_reversed == 1:
                i[3] = '0'
            i[3] = int(i[3])

    for row in table:
        print(row)

    pcnf, bin_pcnf, dec_pcnf = build_pcnf(table)
    pdnf, bin_pdnf, dec_pdnf = build_pdnf(table)

    pcnf = pcnf[:len(pcnf) - 1]
    pdnf = pdnf[:len(pdnf) - 1]

    print("\n pcnf", pcnf)
    print("\n bin ", bin_pcnf)
    print("\n dec ", dec_pcnf)
    print("\n pdnf", pdnf)
    print("\n bin ", bin_pdnf)
    print("\n dec ", dec_pdnf)
    print("\n index ", convert(table))

main()
