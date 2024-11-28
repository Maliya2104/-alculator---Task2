numbers_dict = {"ноль": 0, "один": 1, "одна": 1, "два": 2, "две": 2, "три": 3, "четыре": 4, "пять": 5, "шесть": 6, "семь": 7, "восемь": 8,
                "девять": 9, "десять": 10, "одиннадцать": 11, "двенадцать": 12, "тринадцать": 13,
                "четырнадцать": 14, "пятнадцать": 15, 'шестнадцать': 16, 'семнадцать': 17,
                'восемнадцать': 18, "девятнадцать": 19, "двадцать": 20, "тридцать": 30, "сорок": 40,
                "пятьдесят": 50, "шестьдесят": 60, "семьдесят": 70, "восемьдесят": 80, "девяносто": 90, "сто": 100,
                "двести": 200, "триста": 300, "четыреста": 400, "пятьсот": 500, "шестьсот": 600, "семьсот": 700,
                "восемьсот": 800, "девятьсот": 900, "тысяча": 1000, "две тысячи": 2000, "три тысячи": 3000,
                "четыре тысячи": 4000, "пять тысяч": 5000, "шесть тысяч": 6000, "семь тысяч": 7000,
                "восемь тысяч": 8000, "девять тысяч": 9000}
add_numbers = {1: "одна", 2: "две"}
arithmetic_operations = {"умножить": '*', "разделить": ':', "плюс": '+', "минус": '-', "остаток от деления": '%'}
fractional_plural = {"десятых": 10, "сотых": 100, "тысячных": 1000, "десятитысячных": 10000, "cтотысячных": 100000, "милионных": 1000000}
fractional_singular = {"десятая": 10, "сотая": 100, "тысячная": 1000, "десятитысячная": 10000, "cтотысячная": 100000, "милионная": 1000000}
priority_operations = [':', '*', '%']

def is_number(num):
    '''Checking for the integer value.

    Args:
        num (?int): the value that is checked for belonging to an integer data type.

    Returns:
        True (bool): the return value upon successful verification.
        False (bool): the return value when the check fails.
    '''
    if not num:
        return False
    try:
        float(num)
        return True
    except ValueError:
        return False
def start_calc():
    '''The first starting function that is called when the code is run.

    By its structure, it is a procedure that does not accept or return values.
    '''
    print("""\nТебя приветствует текстовый калькулатор. Я поддерживаю операции: 
    + сложения,
    - вычитания,
    * умножения,
    / деления,
    % остатка от деления.
Пиши внимательно и не допускай орфографических ошибок, а если захочешь выйти, то напиши мне 'стоп'""")
    while True:
        result = user_input()
        if result:
            try:
                answer = recognition_list(result)
            except:
                print("Вычисление невозможно, порядок операций прописан неверно")
            if is_number(answer):
                print(f"Вычисление прошло успешно, мой ответ: {answer_output(answer)}")
def user_input():
    '''A function that controls user input.

    Returns:
        check_input(entered_operation) (list): the result of checking the correctness of the data entered by the user.
    '''
    entered_operation = input("\nВведи операцию, результат которой хочешь получить: ").lower()
    if entered_operation == "стоп":
        end_calc()
    if len(entered_operation.strip()) > 0:
        return check_input(entered_operation)

def find_and_replace(full_str, substr, elem):
    '''Search and replace function.

    This is where the argument is searched for in the string, and then replaced to facilitate further work with the
    data.

    Args:
        full_str (str): the string in which the search is performed.
        substr (str): the desired section of the string that needs to be replaced.
        elem (str): the symbol that is being replaced.

    Returns:
        full_str (str): the whole line after the replacement.
    '''
    while True:
        index = full_str.find(substr)
        if index == -1: return full_str
        full_str = full_str[:index] + elem + full_str[index+len(substr):]
def check_input(entered_string):
    '''Full verification of the user's string for compliance with the requirements.

    In addition to checking, this function also converts a row into a sheet with a convenient data format to
    facilitate further calculation.

    Args:
        entered_string (str): user string.

    Returns:
        list_res (list): list of operands and operations, where each arithmetic operation is reduced to a character,
        and each number from the text format is converted to an integer value. Approximate view: [-12, '-', 9]
    '''
    entered_string = find_and_replace(entered_string, "скобка открывается", "(")
    entered_string = find_and_replace(entered_string, "скобка закрывается", ")")
    entered_string = find_and_replace(entered_string, "умножить на", "*")
    entered_string = find_and_replace(entered_string, "разделить на", ":")
    entered_string = find_and_replace(entered_string, "остаток от деления на", "%")
    entered_string = find_and_replace(entered_string, "остаток от деления", "%")

    if entered_string.count(")") != entered_string.count("("):
        print("Некорректный ввод скобок")
        return

    list_calc = entered_string.split()
    for ind, elem in enumerate(list_calc):
        if elem in arithmetic_operations.keys():
            list_calc[ind] = arithmetic_operations[elem]
    number = ''
    list_res = []
    merge_dict = {**fractional_plural, **fractional_singular}
    for index, word in enumerate(list_calc):
        if word in numbers_dict:
            if index != len(list_calc)-1:
                number += word + ' '
            else:
                if len(number) > 0 and not number_partition(number):
                    print(f"Число {number} в некорректной записи")
                    return
                number += word
                list_res.append(number_partition(number))
                number = ''
        elif word in arithmetic_operations.values() or word in (')','('):
            if not number_partition(number) and number != '':
                print(f"Число {number} в некорректной записи")
                return
            elif number != '':
                list_res.append(number_partition(number))
                number = ''
            list_res.append(word)
        elif word == "и":
            list_res.append(number_partition(number))
            number = ''
        elif word in merge_dict.keys() and len(number) > 0:
            try:
                list_res[-1] += number_partition(number)/merge_dict[word]
            except:
                print("He удалось преобразовать дробную часть")
                return
            number = ''
        else:
            print(arithmetic_operations.get(word))
            print(f"Введённое слово {word} калькулятором не распознано")
            return
    try:
        list_res = find_negative(list_res)
    except:
        print("Некорректный ввод арифметических операций")
        return
    return list_res

def find_negative(lst_op):
    '''Searching and formatting negative values.

    Args:
        lst_op (list): a formatted list with operands and operations.

    Returns:
        lst_op (list): a list in which all negative values are indicated.
    '''
    if lst_op[0] == "-" and isceloe(lst_op[1]):
        lst_op[1] = -lst_op[1]
        lst_op.pop(0)
    for ind, elem in enumerate(lst_op):
        if elem == "-" and lst_op[ind-1] in arithmetic_operations.values():
                lst_op[ind+1] = -lst_op[ind+1]
                lst_op.pop(ind)
    return lst_op

def number_partition(number):
    '''Сonverting the text format of writing a number to an integer type.

    Args:
        number (str): the line where the number is written in words.

    Returns:
        result (int): the result of converting a string to a number.
    '''
    list = number.split()
    result = 0
    for word in list:
        if result > 0 and numbers_dict[word] >= result:
            print(word, numbers_dict[word])
            print("Некорректный ввод числа")
            return
        try:
            result += numbers_dict[word]
        except:
            print(f"Число {word} в словаре числе не найдено")
    return result

def recognition_list(list_calc):
    '''Defines the order of calculation of arithmetic operations.

    The function determines the order of calculation, respecting the priorities of all operations.

    Args:
        list_calc (list): a list with formatted data.

    Returns:
        list_calc[0] (int): the final result of calculating arithmetic operations.
    '''
    while len(list_calc) > 1:
        if "(" in list_calc:
            bracket_ind1 = list_calc.index("(")
            bracket_ind2 = list_calc.index(")")
            list_calc[bracket_ind1] = priority_operation(list_calc[bracket_ind1 + 1:bracket_ind2])
            del list_calc[bracket_ind1 + 1:bracket_ind2 + 1]
        else:
            list_calc[0] = priority_operation(list_calc)
    return list_calc[0]

def priority_operation(list_oper):
    '''Сalculation of the transmitted arithmetic operation.

    Args:
        list_oper (list): calculation priority operation.

    Returns:
        list_oper[0] (int): the result of calculating the priority arithmetic operation.
    '''
    while len(list_oper) > 1:
        operations = [op for op in list_oper if op in arithmetic_operations.values()]
        for op in operations:
            if op in priority_operations:
                op_ind, oper = list_oper.index(op), op
                break
        else:
            op_ind, oper = list_oper.index(operations[0]), operations[0]
        list_oper[op_ind - 1] = calculation_operation(list_oper[op_ind - 1], list_oper[op_ind + 1], oper)
        del list_oper[op_ind:op_ind + 2]
    return list_oper[0]
def calculation_operation(number1, number2, oper):
    '''Performing a specific action with two operands.

    Args:
        number1 (int): the first operand.
        number2 (int): the second operand.
        oper (str): the type of operation indicated by the symbol.

    Returns:
        number1 ... number2 (int/float): the result of calculating two operands.
    '''
    match oper:
        case "*":
            return number1 * number2
        case "+":
            return number1 + number2
        case "-":
            return number1 - number2
        case ":":
            if number2 != 0:
                return number1 / number2
            print("Деление на ноль невозможно")
            return
        case "%":
            return number1 % number2

def isceloe(num):
    '''Checking for the absence of the fractional part of the number.

    Args:
        num (int/float): the value being checked.

    Returns:
        True (bool): if the number does not have a fractional number.
        False (bool): if a number has a fractional number.
    '''
    return num % 1 == 0

def answer_output(num):
    '''Converts the result of the calculation to a text format.

    Args:
        num (int/float): the number to be translated.

    Returns:
        answer (str): the text format of the response.
    '''
    answer = ""
    if num < 0:
        answer += "минус "
        num = -num
    if isceloe(num):
        return answer + converting_answer(int(num))
    whole_part = int(num//1)
    answer += converting_answer(int(whole_part)) + " и " + converting_fract(format(num, '.4f').rstrip('0').rstrip('.')[2:])
    return answer

def converting_answer(num, fract = False):
    '''Сonverts an integer value to a text format.

    Args:
        num (int/float): the number to be translated.
        *fract (bool): output parameter.

    Returns:
        str_ans (str): the text format of the integer value.
    '''
    str_ans = ""
    str_num = str(num)
    for ind, sym in enumerate(str_num):
        if int(str_num[ind:]) <= 20 and int(str_num[ind:]) > 0:
            if int(str_num[ind:]) in [1,2] and fract:
                str_ans += [val for val in numbers_dict if numbers_dict[val] == int(str_num[ind:])][1]
            else:
                str_ans += [val for val in numbers_dict if numbers_dict[val] == int(str_num[ind:])][0]
            break
        elif sym == "0" and num>0:
            continue
        variable = int(sym + '0' * len(str_num[ind+1:]))
        str_ans += [val for val in numbers_dict if numbers_dict[val] == variable][0] + " "
    return str_ans

def converting_fract(fract):
    '''Сonverts a fractional value to a text format.

    Args:
        fract (str): fractional part of a number.

    Returns:
        res (str): the text format of the fractional value.
    '''
    res = ""
    current_dict = fractional_singular if int(fract[-1]) == 1 else fractional_plural
    res += converting_answer(int(fract), True) + " "
    res += list(filter(lambda x: current_dict[x] == int(pow(10,len(fract))), current_dict))[0]
    return res

def end_calc():
    '''Terminates the program.

    This is a procedure that has no return values or arguments. It is used to force the termination of the program.
    '''
    print("Ещё увидимся!")
    raise SystemExit

start_calc()



