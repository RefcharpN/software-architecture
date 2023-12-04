import random

file1 = open("./lecture_text/random_text.txt", "r")

# считываем все строки
lines = file1.readlines()

print(random.choice(lines))