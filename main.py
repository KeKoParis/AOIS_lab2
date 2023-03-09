def solve(curr_table, curr_expression, index):
    curr_expression = replace_negative(curr_table, curr_expression, index)
    curr_expression = replace_positive(curr_table, curr_expression, index)
    curr_expression = replace_signs(curr_expression)

    curr_table[index][3] = eval(curr_expression)

    return curr_table


def replace_negative(curr_table, curr_expression, index):
    while curr_expression.find("!x1") != -1:
        curr_expression = curr_expression.replace("!x1", str(abs(curr_table[index][0] - 1)))
    while curr_expression.find("!x2") != -1:
        curr_expression = curr_expression.replace("!x2", str(abs(curr_table[index][1] - 1)))
    while curr_expression.find("!x3") != -1:
        curr_expression = curr_expression.replace("!x3", str(abs(curr_table[index][2] - 1)))

    return curr_expression


def replace_positive(curr_table, curr_expression, index):
    while curr_expression.find("x1") != -1:
        curr_expression = curr_expression.replace('x1', str(curr_table[index][0]))
        break
    while curr_expression.find("x2") != -1:
        curr_expression = curr_expression.replace("x2", str(curr_table[index][1]))
    while curr_expression.find("x3") != -1:
        curr_expression = curr_expression.replace("x3", str(curr_table[index][2]))

    return curr_expression


def replace_signs(curr_expression):
    while curr_expression.find("+") != -1:
        curr_expression = curr_expression.replace("+", " or ")
    while curr_expression.find("*") != -1:
        curr_expression = curr_expression.replace("*", " and ")

    return curr_expression


def find_values_pcnf(curr_row):
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


def find_values_pdnf(curr_row):
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


table = [[0 for i in range(4)] for j in range(8)]

check = 0
for i in range(8):
    if i < 4:
        table[i][0] = 0
    else:
        table[i][0] = 1

    if check == 4:
        check = 0

    if check < 2:
        table[i][1] = 0
    else:
        table[i][1] = 1

    if i % 2 == 0:
        table[i][2] = 0
    else:
        table[i][2] = 1

    check = check + 1

expression = input("Enter expression: ")

for i in range(8):
    table = solve(table, expression, i)

for row in table:
    print(row)

pcnf: str = ""
pdnf: str = ""
for row in table:
    if row[3] == 0:
        pcnf += "("
        pcnf += find_values_pcnf(row)
        pcnf += ")*"

    if row[3] == 1:
        pdnf += "("
        pdnf += find_values_pdnf(row)
        pdnf += ")+"

pcnf = pcnf[:len(pcnf) - 1]
pdnf = pdnf[:len(pdnf) - 1]

print("\n pcnf", pcnf)
print("\n pdnf", pdnf)
