user = input("Введите температуру: ")
if len(user) < 2:
    print("Введите нормально")
else:
    temp = user[:-1] # берем только число
    bukva = user[-1] #берем букву
if temp[0] == "-": # если градус отрицателен, то мы сначала забираем только число, переводим его в int, и потом возвращаем минус
    only_digits = temp[1:]
    temp_ch = int(only_digits) * (-1)
else:
    temp_ch = int(temp) # если положителен, то ничего не делаем
if bukva == "C":
    result = (temp_ch * 9/5) + 32
    print(f"Вывод: {int(result)}F")
elif bukva == "F":
    result = (temp_ch-32)*5/9
    print(f"Вывод: {int(result)}C")
else:
    print("Шкала должна быть C или F.")