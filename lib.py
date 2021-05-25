import copy
from random import randint
from operator import mul, sub

import numpy


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
        n = randint(3, 7)
        a_arr = [[randint(1, 10) for i in range(n)] for j in range(n)]
        b_arr = [randint(1, 10) for i in range(n)]

    print(numpy.linalg.det(a_arr))


    print('массив А = ')
    for i in a_arr:
        print(i)
    print('массив В =')
    print(b_arr)

    return a_arr, b_arr, n


def factor(arr):
    n = len(arr)
    for k in range(n):
        print('k=', k)
        for i in range(k + 1):
            sum = 0
            print('i=', i)
            for p in range(i):
                print('p=', p)
                sum += arr[k][p] * arr[p][i]
                print('sum', sum)
            arr[k][i] -= sum
        for i in arr:
            print(i)
        for j in range(k + 1, n):
            sum = 0
            for p in range(k):
                sum += arr[k][p] * arr[p][j]
            arr[k][j] -= sum

        for j in range(k + 1, n):
            arr[k][j] /= arr[k][k]
    return arr


def SwapRows(A, B, row1, row2):
    A[row1], A[row2] = A[row2], A[row1]
    B[row1], B[row2] = B[row2], B[row1]


def DivideRow(A, B, row, divider):
    A[row] = [a / divider for a in A[row]]
    B[row] /= divider


def CombineRows(A, B, row, source_row, weight):
    A[row] = [(a + k * weight) for a, k in zip(A[row], A[source_row])]
    B[row] += B[source_row] * weight


def solve_SLAU(A, B):
    # return numpy.linalg.solve(A, B)
    column = 0
    while (column < len(B)):
        current_row = None
        for r in range(column, len(A)):
            if current_row is None or abs(A[r][column]) > abs(A[current_row][column]):
                current_row = r
        if current_row is None:
            print("решений нет")
            return None
        if current_row != column:
            SwapRows(A, B, current_row, column)
        DivideRow(A, B, column, A[column][column])
        for r in range(column + 1, len(A)):
            CombineRows(A, B, r, column, -A[r][column])
        column += 1
    X = [0 for b in B]
    for i in range(len(B) - 1, -1, -1):
        X[i] = B[i] - sum(x * a for x, a in zip(X[(i + 1):], A[i][(i + 1):]))
    print("Получили ответ:")
    print("\n".join("X{0} =\t{1:10.2f}".format(i + 1, x) for i, x in enumerate(X)))
    return X


def det(a):
    res = 1
    n = len(a)
    for i in range(n):
        # выбираем опорный элемент
        j = max(range(i, n), key=lambda k: abs(a[k][i]))
        if i != j:
            a[i], a[j] = a[j], a[i]
            res *= -1
        # убеждаемся, что матрица не вырожденная
        if a[i][i] == 0:
            return 0
        res *= a[i][i]
        # "обнуляем" элементы в текущем столбце
        for j in range(i + 1, n):
            b = a[j][i] / a[i][i]
            a[j] = [a[j][k] - b * a[i][k] for k in range(n)]
    return res


def minor(a, i, j):
    M = copy.deepcopy(a)
    del M[i]
    for i in range(len(a[0]) - 1):
        del M[i][j]
    return M


def inverse(a):
    result = [[0 for i in range(len(a))] for j in range(len(a))]
    for i in range(len(a)):
        for j in range(len(a[0])):
            tmp = minor(a, i, j)
            if i + j % 2 == 1:
                result[i][j] = -1 * det(tmp) / det(a)
            else:
                result[i][j] = 1 * det(tmp) / det(a)
    return result


def inverse2(a):
    b = [[1 if i == j else 0 for i in range(len(a))] for j in range(len(a))]
    for i in range(len(a)):
        for j in range(i):
            a[i, j] *= -1

        # for (i = n - 1; i > -1; i--)
        #     {
        #         a[i, p[i]] = 1 / a[i, p[i]];
        #
        #     for (j = i - 1; j > -1; j--)
        #     {
        #         a[j, p[i]] *= -a[i, p[i]];
        #     }
        #     }
        #
        # // L ^ -1
        # for (k = 0; k < n - 2; k++)
        #     {
        #     for (i = k + 2; i < n; i++)
        #     for (j = 0; j <= k; j++)
        #     a[i, p[j]] += a[i, p[k + 1]] * a[k + 1, p[j]];
        #     }
        #
        # // U ^ -1
        # for (k = n - 1; k > 0; k--)
        #     {
        #     for (i = 0; i < k - 1; i++)
        #     for (j = k; j < n; j++)
        #     a[i, p[j]] += a[i, p[k - 1]] * a[k - 1, p[j]];
        #     for (j = n - 1; j >= k; j--)
        #     a[k - 1, p[j]] *= a[k - 1, p[k - 1]];
        #     }
        #
        # for (i = 0; i < n; i++)
        #     {
        #     for (j = 0; j < n; j++)
        #     {
        #     if (j < i)
        #     {
        #     sum = 0;
        #     for (k = i; k < n; k++)
        #     sum += a[i, p[k]] * a[k, p[j]];
        #     }
        #     else
        #     {
        #     sum = a[i, p[j]];
        #     for (k = j + 1; k < n; k++)
        #     sum += a[i, p[k]] * a[k, p[j]];
        #     }
        #
        #     a[i, p[j]] = sum;
        #     }