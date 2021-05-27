import time
from copy import deepcopy
from math import pi, tan, sin, exp, log
from random import randint, uniform


def column(row):
    i = 0
    n = len(row)
    while not row[i] and i < n:
        i += 1
    return i if i < n else -1


def input_data():
    if int(input('1- ручной ввод \n2- автоматическая генерация')) == 1:
        pass
        n = int(input('Введите размер массива'))
        a_arr = [[int(input('{} строка , {} элемент'.format(j, i))) for i in range(n)] for j in range(n)]
        # a_arr = [
        #     [1, 0, 1, 0],
        #     [-1, 1, -2, 1],
        #     [4, 0, 1, -2],
        #     [4, -4, 0, 1],
        # ]
        b_arr = [int(input('{} элемент'.format(i))) for i in range(n)]
        # b_arr = [2, -2, 0, 5]
    else:
        n = randint(3, 10)
        a_arr = [[uniform(-100, 100) for i in range(n)] for j in range(n)]
        b_arr = [uniform(-100, 100) for i in range(n)]

    print('массив А = ')
    for i in a_arr:
        print(i)
    print('массив В =')
    print(b_arr)

    return a_arr, b_arr, n


def factor(arr):
    n = len(arr)
    znk = 1
    op_numb = 0
    t = [int(i) for i in range(n)]
    for k in range(n):
        for i in range(k + 1):
            sum = 0
            for p in range(i):
                sum += arr[k][t[p]] * arr[p][t[i]]
                op_numb += 1
            arr[k][t[i]] -= sum
        for j in range(k + 1, n):
            sum = 0
            for p in range(k):
                sum += arr[k][t[p]] * arr[p][t[j]]
                op_numb += 1
            arr[k][t[j]] -= sum
        imax = k
        for i in range(k + 1, n):
            if abs(arr[k][t[i]]) > abs(arr[k][t[imax]]):
                imax = i
        if imax != k:
            znk = -znk
            t[k], t[imax] = t[imax], t[k]

        for j in range(k + 1, n):
            arr[k][t[j]] /= arr[k][t[k]]
            op_numb += 1
    return arr, t, op_numb, znk


def print_LU(A, p, n):
    # Вывод PA
    print(p)
    print('Массив PA:')
    for i in range(n):
        for j in range(n):
            print(A[i][p[j]], end='\t')
        print('\n')

    print('Массив L:')
    # Вывод L
    for i in range(n):
        for j in range(n):
            print(A[i][p[j]], end='\t') if j <= i else print(0, end='\t')
        print('\n')

    print('Массив U:')
    # Вывод U
    for i in range(n):
        for j in range(n):
            if j == i:
                print(1, end='\t')
            elif j > i:
                print(A[i][p[j]], end='\t')
            else:
                print(0, end='\t')
        print('\n')


def solve_SLAU(A, B, p, n):
    y = [0 for i in range(n)]
    x = [0 for i in range(n)]
    op_numb = 0

    for i in range(n):
        sum = 0
        for j in range(i):
            sum += A[i][p[j]] * y[j]
            op_numb += 1
        y[i] = (B[i] - sum) / A[i][p[i]]
        op_numb += 1

    for i in range(n - 1, -1, -1):
        sum = 0
        for j in range(i + 1, n):
            sum += A[i][p[j]] * x[p[j]]
            op_numb += 1
        x[p[i]] = (y[i] - sum)

    return x, op_numb


def print_x(x):
    print("Получили ответ:")
    print("\n".join("X{0} =\t{1}".format(i + 1, j) for i, j in enumerate(x)))


def det(a, p, n, znk):
    det = 1
    for i in range(n):
        det *= a[i][p[i]]
    return det * znk


def inverse(a, p, n):
    b = [0 for i in range(n)]
    v = [[0 for j in range(n)] for i in range(n)]
    op_numb = 0
    op_numb_sum = 0
    for i in range(n):
        for j in range(n):
            b[j] = 0 if j != i else 1
        x, op_numb = solve_SLAU(a, b, p, n)

        for j in range(n):
            v[j][i] = x[j]
        op_numb_sum += op_numb
    return v, op_numb_sum


def inverse2(a, p, n):
    op_numb = 0

    for i in range(n):
        for j in range(i + 1, n):
            a[i][p[j]] = -a[i][p[j]]

    for j in range(n):
        a[j][p[j]] = 1 / a[j][p[j]]
        op_numb += 1
        for i in range(j + 1, n):
            a[i][p[j]] = -a[i][p[j]] * a[j][p[j]]
            op_numb += 1

    for k in range(n - 1, 0, -1):
        for i in range(k - 1):
            for j in range(k, n):
                a[i][p[j]] += a[i][p[k - 1]] * a[k - 1][p[j]]
                op_numb += 1

    for k in range(n - 1):
        for i in range(k + 2, n):
            for j in range(k + 1):
                a[i][p[j]] += a[i][p[k + 1]] * a[k + 1][p[j]]
                op_numb += 1
        for j in range(k + 1):
            a[k + 1][p[j]] = a[k + 1][p[j]] * a[k + 1][p[k + 1]]
            op_numb += 1

    for i in range(n):
        for j in range(n):
            if i < j:
                sum = 0
                for k in range(j, n):
                    sum += a[i][p[k]] * a[k][p[j]]
                    op_numb += 1
            if i >= j:
                sum = a[i][p[j]]
                for k in range(i + 1, n):
                    sum += a[i][p[k]] * a[k][p[j]]
                    op_numb += 1
            a[i][p[j]] = sum

    p1 = get_p1(p, n)

    return a, p1, op_numb


def get_p1(p, n):
    p1 = [0 for i in range(n)]
    for i in range(n):
        p1[p[i]] = i
    return p1


def print_inversed(a, p, p1, n):
    for i in range(n):
        for j in range(n):
            print(a[p1[i]][p[j]], end='\t')
        print('\n')


def print_table1(exp, mode='def'):
    if mode == 'def':
        print("{0:20}\t{1:20}\t{2:20}\t{3:20}\t{4:20}\n".format('Порядок', 'Время', 'Точность', 'Теоритическое ЧО',
                                                                'Реальное ЧО'))
        print(
            "\n".join("{0:<20}\t{1:<20}\t{2:<20}\t{3:<20}\t{4:<20}".format(i[0], i[1], i[2], i[3], i[4]) for i in exp))
    else:
        print("{0:20}\t{1:20}\t{2:20}\t{3:20}\t{4:20}\t{5:20}\t{6:20}\t{7:20}\n".format('Порядок', 'Время', 'Время 2',
                                                                                        'Точность',
                                                                                        'Точность 2',
                                                                                        "Теоритическое ЧО",
                                                                                        "Реальное ЧО", "Реальное ЧО 2"))
        print(
            "\n".join(
                "{0:<20}\t{1:<20}\t{2:<20}\t{3:<20}\t{4:<20}\t{5:<20}\t{6:<20}\t{7:<20}".format(i[0], i[1], i[2], i[3],
                                                                                                i[4], i[5], i[6], i[7])
                for i in exp))
    print('\n')


def exp1():
    exp = [[0 for j in range(5)] for i in range(20)]
    counter = 0
    for n in range(5, 105, 5):
        exp[counter][0] = n
        a = [[uniform(-100, 100) for i in range(n)] for j in range(n)]
        b = [uniform(-100, 100) for i in range(n)]
        copy = deepcopy(a)

        start_time = time.time()
        a, p, op_numb1, znk = factor(a)
        x, op_numb2 = solve_SLAU(a, b, p, n)
        exp[counter][1] = time.time() - start_time

        x_ex = [int(i) for i in range(n)]
        b = [0 for i in range(n)]

        for i in range(n):
            for j in range(n):
                b[i] += copy[i][j] * x_ex[j]

        x, op_numb = solve_SLAU(a, b, p, n)

        for i in range(n):
            ex = abs(x_ex[i] - x[i])
            if i == 0:
                max_e = ex
            elif ex > max_e:
                max_e = ex
        exp[counter][2] = max_e
        exp[counter][3] = pow(n, 3) / 3
        exp[counter][4] = op_numb1 + op_numb2
        counter += 1
    print_table1(exp)


def exp2():
    non_fixed(Guilbert, "Матрица Гилберта")
    fixed(Second, "Вторая")
    fixed(Third, "Третья")
    non_fixed(Fouth, "Четвертая")
    non_fixed(Fifth, "Пятая")
    fixed(Sixth, "Шестая")
    non_fixed(Seventh, "Седьмая")
    non_fixed(Eighth, "Восьмая")
    non_fixed(Ninth, "Девятая")
    fixed(Tenth, "Десятая")


def non_fixed(func, title):
    exp = [[0 for j in range(5)] for i in range(10)]
    counter = 0
    for n in range(4, 44, 4):
        exp[counter][0] = n
        a = func(n)
        x_ex = [int(i) for i in range(n)]
        b = [0 for i in range(n)]

        for i in range(n):
            for j in range(n):
                b[i] += a[i][j] * x_ex[j]

        start_time = time.time()
        a, p, op_numb1, znk = factor(a)
        x, op_numb2 = solve_SLAU(a, b, p, n)
        exp[counter][1] = time.time() - start_time

        for i in range(n):
            ex = abs(x_ex[i] - x[i])
            if i == 0:
                max_e = ex
            elif ex > max_e:
                max_e = ex
        exp[counter][2] = max_e
        exp[counter][3] = pow(n, 3) / 3
        exp[counter][4] = op_numb1 + op_numb2
        counter += 1
    print(title, end='\n')
    print_table1(exp)


def fixed(func, title):
    exp = [[0 for j in range(5)] for i in range(1)]
    counter = 0

    a, n = func()
    exp[counter][0] = n

    x_ex = [int(i) for i in range(n)]
    b = [0 for i in range(n)]

    for i in range(n):
        for j in range(n):
            b[i] += a[i][j] * x_ex[j]

    start_time = time.time()
    a, p, op_numb1, znk = factor(a)
    x, op_numb2 = solve_SLAU(a, b, p, n)
    exp[counter][1] = time.time() - start_time

    for i in range(n):
        ex = abs(x_ex[i] - x[i])
        if i == 0:
            max_e = ex
        elif ex > max_e:
            max_e = ex

    exp[counter][2] = max_e
    exp[counter][3] = pow(n, 3) / 3
    exp[counter][4] = op_numb1 + op_numb2

    print(title, end='\n')
    print_table1(exp)


def Guilbert(n):
    a = [[0 for j in range(n)] for i in range(n)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            a[i - 1][j - 1] = 1 / (i + j - 1)
    return a


def Second():
    n = 20
    a = [[0 for j in range(n)] for i in range(n)]
    for i in range(n - 1):
        a[i][i] = 1
        a[i][i + 1] = 1
    a[n - 1][n - 1] = 1
    return a, n


def Third():
    n = 7
    a = [[5, 4, 7, 5, 6, 7, 5], [4, 12, 8, 7, 8, 8, 6], [7, 8, 10, 9, 8, 7, 7],
         [5, 7, 9, 11, 9, 7, 5], [6, 8, 8, 9, 10, 8, 9], [7, 8, 7, 7, 8, 10, 10],
         [5, 6, 7, 5, 9, 10, 10]]
    return a, n


def Fouth(n):
    a = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                a[i][i] = 0.01 / (n - i + 1) / (i + 1)
            elif i < j:
                a[i][j] = 0
            else:
                a[i][j] = i * (n - j)
    return a


def Fifth(n):
    a = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                a[i][i] = 0.01 / (n - i + 1) / (i + 1)
            elif i < j:
                a[i][j] = j * (n - j)
            else:
                a[i][j] = i * (n - j)
    return a


def Sixth():
    n = 8
    t = pi * 0.999
    a = [[cot(t), csc(t), (1 - cot(t)), csc(t), 1, 1, 1, 1, ],
         [-csc(t), cot(t), -csc(t), (1 + cot(t)), 1, 1, 1, 1],
         [(1 - cot(t)), csc(t), cot(t), csc(t), (1 - cot(t)), csc(t), 1, 1],
         [-csc(t), (1 + cot(t)), -csc(t), cot(t), -csc(t), (1 + cot(t)), 1, 1],
         [1, 1, (1 - cot(t)), csc(t), cot(t), csc(t), (1 - cot(t)), csc(t)],
         [1, 1, -csc(t), (1 + cot(t)), -csc(t), cot(t), -csc(t), (1 + cot(t))],
         [1, 1, 1, 1, (1 - cot(t)), csc(t), cot(t), csc(t)],
         [1, 1, 1, 1, -csc(t), (1 + cot(t)), -csc(t), cot(t)]]
    return a, n


def cot(a):
    return 1 / tan(a)


def csc(a):
    return 1 / sin(a)


def Seventh(n):
    a = [[0 for j in range(n)] for i in range(n)]
    w = 5
    k = n - 1
    for i in range(n):
        for j in range(n):
            if i == j:
                a[i][j] = pow(w, abs(n - 2 * j) / 2)
            elif i == 0 or j == 0:
                a[i][j] = a[0][0] / pow(w, j + 1)
            elif i == k or j == k:
                a[i][j] = a[k][k] / pow(w, j)
            else:
                a[i][j] = 0
    return a


def Eighth(n):
    a = [[0 for j in range(n)] for i in range(n)]
    h = 0.000001
    for i in range(n):
        for j in range(n):
            a[i][j] = exp(i * j * h)

    return a


def Ninth(n):
    c = 99999
    a = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            a[i][j] = c + log(i + 1 * j + 1, 2)
    return a


def Tenth():
    n = 4
    k = pow(10, -4)
    a = [[0.9143 * k, 0, 0, 0],
         [0.8762, 0.7156 * k, 0, 0],
         [0.7943, 0.8143, 0.9504 * k, 0],
         [0.8017, 0.6123, 0.7165, 0.7123 * k]]
    return a, n


def exp3():
    exp = [[0 for j in range(8)] for i in range(20)]
    counter = 0
    for n in range(5, 105, 5):
        exp[counter][0] = n
        a = [[uniform(-100, 100) for i in range(n)] for j in range(n)]
        b = [uniform(-100, 100) for i in range(n)]
        copy = deepcopy(a)

        a, p, op_numb, znk = factor(a)

        start_time = time.time()
        v, op_numb1 = inverse(a, p, n)
        exp[counter][1] = time.time() - start_time

        start_time = time.time()
        a, p1, op_numb2 = inverse2(a, p, n)
        exp[counter][2] = time.time() - start_time

        exp[counter][3] = exp_accuracy(copy, v, n)

        c = [[a[p1[i]][p[j]] for j in range(n)] for i in range(n)]

        exp[counter][4] = exp_accuracy(copy, c, n)

        exp[counter][5] = pow(n, 3)
        exp[counter][6] = op_numb1 + op_numb
        exp[counter][7] = op_numb2 + op_numb
        counter += 1
    print_table1(exp, mode='exp3')


def exp_accuracy(a, b, n):
    m = mult(a, b, n)
    e = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    m = sub(e, m, n)
    max_a = 0
    max_mult = 0

    for i in range(n):
        sum_a = 0
        sum_mult = 0
        for j in range(n):
            sum_a += abs(a[i][j])
            sum_mult += abs(m[i][j])
        if i == 0:
            max_a = sum_a
            max_mult = sum_mult
        else:
            if sum_a > max_a:
                max_a = sum_a
            if sum_mult > max_mult:
                max_mult = sum_mult

    return max_mult / max_a


def mult(a, b, n):
    r = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                r[i][j] += a[i][k] * b[k][j]
    return r


def sub(a, b, n):
    r = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            r[i][j] = a[i][j] - b[i][j]
    return r
