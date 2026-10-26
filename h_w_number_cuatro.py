while True:
    num = input("Введите N число >= 2, а программа выведет все простые числа, которые существуют до него: ")
    if num.isdigit() and int(num) >=2:
        n = int(num)
        break
    else:
        print("Вводите только N числа >=2")
A = [] #Пусть A — булевый массив, индексируемый числами от 2 до n, изначально заполненный значениями true.
for x in range(n+1):
    A.append(True)
i = 2
while i**2 <= n:
    if A[i] == True:
        j = i**2
        while j <=n:
            A[j] = False
            j = j+i
    i = i +1
for i in range(2, n+1):
    if A[i] == True:
        print(i)