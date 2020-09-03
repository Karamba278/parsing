from pprint import pprint
import requests
import json

# Задание 1 Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.
url = 'https://api.github.com/users/Karamba278/repos'  #Сразу вставил имя юзера (себя) в ссылку, но можнод для
# удобства и отдельно его вводить
response = requests.get(url)
j_data = response.json()
#pprint(j_data)
for repos in j_data:
    print(repos['name'])

# т.к. нам могут потребоваться и другие данные, то запишем в файл всю информацию о репозиториях
with open('GitHubUserRep.json', "w") as write_f:
    json.dump(j_data, write_f)

# Задание 2 Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

# Раз на вебинаре разрекламировали НАСА, то возьмем НАСА API :)
url = 'https://api.nasa.gov/planetary/apod'

api_key = 'aydx4dSBSpKHD8tGxFrVqOYxxe2df2lirt0rKGxj'

params = {'api_key':api_key}

response2 = requests.get(url, params=params)
j_data2 = response2.json()
pprint(j_data2)

with open('NASA_data.json', "w") as write_f2:
    json.dump(j_data2, write_f2)