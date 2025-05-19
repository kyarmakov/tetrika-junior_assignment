import csv
import re

import requests
from bs4 import BeautifulSoup

url = 'https://ru.wikipedia.org/'
animals_url = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'

response = requests.get(animals_url)
soup = BeautifulSoup(response.text, 'html.parser')

ru_animals = []

# Получаем список животных
while next_page_lnk := soup.find('a', string='Следующая страница'):
    soup = BeautifulSoup(response.text, 'html.parser')

    items = []
    for div in soup.select('div.mw-category-columns'):
        items = div.find_all('a')

    animals = list(map(lambda i: i.text, items))
    for animal in animals:
        if bool(re.search('[а-яА-Я]', animal[0])):
            ru_animals.append(animal)

    next_page_lnk = soup.find('a', string='Следующая страница')
    if next_page_lnk:
        response = requests.get(url + next_page_lnk.get('href'))

# Записываем количество животных на каждую букву алфавита в словарь
animals_dict = {}
for animal in ru_animals:
    if animal[0] not in animals_dict:
        animals_dict[animal[0]] = 0
    else:
        animals_dict[animal[0]] += 1

# Записываем количество животных на каждую букву алфавита в beasts.csv
with open('beasts.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for letter, number in sorted(animals_dict.items()):
        writer.writerow([letter, number])

# Проверяем файл beasts.csv
with open('beasts.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        letter, number = row[0], row[1]
        if letter not in animals_dict:
            raise Exception(f'ERR: в файле beasts.csv нет буквы {letter}')
        if int(number) != animals_dict[letter]:
            raise Exception(f'ERR: в файле beasts.csv значение для буквы {letter} '
                             f'отличается от эталонного {animals_dict[letter]}')

