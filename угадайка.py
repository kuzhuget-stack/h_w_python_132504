import random
ugaday = int(input("Сейчас будем играть в угадайку. Угадай от 1 до 100: "))
number = random.randint(1, 101)
while number != ugaday:
    if ugaday < number:
        print("Надо больше")
        try_again = int(input("Еще раз: "))
    elif ugaday > number:
        print("Надо меньше")
        try_again = int(input("Еще раз: "))
    elif ugaday == number:
        print("YAS вы выиграли")
    else:
        break