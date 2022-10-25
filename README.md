# Сравниваем вакансии программистов

Программа, которая считает количество вакансий и среднюю зарплату из двух разных источников.

### Как установить

Для начала надо создать .env файл в директории программы и заполнить его:
```
SJ_APIKEY=*ключ API*
```
Где достать:

[API SuperJob](https://api.superjob.ru/), создать приложение, получить `Secret Key`

-------

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
### Как запустить
Просто запустить скрипт
```
python main.py
```
### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).