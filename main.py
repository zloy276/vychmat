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
              sep='\n')
        var = int(input())
        if var == 1:
            a, b, n = input_data()
        elif var == 2:
            a = factor(a)
        elif var == 3:
            print(solve_SLAU(a,b))
        elif var == 4:
            print(det(a))
        elif var == 5:
            for i in inverse(a):
                print(i)
        elif var == 6:
            inverse2(a)
        else:
            print('Выход')
            break


if __name__ == '__main__':
    main()
