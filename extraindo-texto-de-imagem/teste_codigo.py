def imprimirNumeros(a,b):
    divisaiInteira = a // b
    divisaoFlutuante = a/b
    print(f'{divisaiInteira}\n{divisaoFlutuante}')

if __name__ == '__main__':
    a = int(input())
    b = int(input())
    imprimirNumeros(a,b)