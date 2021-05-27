from lib import *

a = None
b = None
n = None


def main():
    global a
    global b
    global n
    while True:
        print('1.Ввод данных',
              '2.Факторизация',
              '3.Решение СЛАУ',
              '4.Вычисление определителя',
              '5.Вычисление A^-1через AX+E',
              '6.Вычисление A^-1 через элементарные проебразования',
              '7.Эксп.1.Случайные матрицы',
              '8.Эксп.2.Плохо обусловленные матрицы',
              '9.Эксп.3.Обращение случайных матриц',
              sep='\n')
        var = int(input())
        if var == 1:
            a, b, n = input_data()
        elif var == 2:
            a, p, op_numb, znk = factor(a)
            print_LU(a, p, n)
        elif var == 3:
            x, op_numb = solve_SLAU(a, b, p, n)
            print_x(x)
        elif var == 4:
            print(det(a, p, n, znk))
        elif var == 5:
            v, op_numb = inverse(a, p, n)
            for i in v:
                print(i)
        elif var == 6:
            a, p1, op_numb = inverse2(a, p, n)
            print_inversed(a, p, p1, n)
        elif var == 7:
            exp1()
        elif var == 8:
            exp2()
        elif var == 9:
            exp3()
        else:
            print('Выход')
            break


if __name__ == '__main__':
    main()
