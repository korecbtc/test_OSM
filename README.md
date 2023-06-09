# Тестирование Nominatim API
### Техническое задание
Написать DDT (data driven tests) тесты публичного API геокодинга openstreetmap.org
(проект Nominatim - https://nominatim.org/release-docs/develop/api/Overview/).
Необходимо протестировать прямое (адрес -> координаты) и обратное (координаты -> адрес) геокодирование.
Используйте Python, Pytest, Allure.
Обратите внимание на логирование, комментирование кода, перехват падений теста и возможность обозначить проблему при падении теста по отчету.
### Запуск проекта

 - Клонируйте репозиторий:
```
git@github.com:korecbtc/test_OSM.git
```
 - Перейдите в папку с проектом

 - Установите и активируйте виртуальное окружение:
```
python -m venv venv

source venv/Scripts/activate
```

 - Установите зависимости из файла requirements.txt

``` 
pip install -r requirements.txt
```
- Запустите тесты
```
pytest
```
### Результаты
Производилось тестирование двух эндпоинтов:

/search

/reverse

Проведены следующие тесты:
- /search Проверка поиска по адресу в свободной форме (параметр 'q'):

  -номер дома, улица, страна, город в разных сочетаниях
  
  -верхний, нижний регистр в адресе
- /search Проверка поиска по адресу в структурированной форме

  -номер дома, улица, страна, город в разных сочетаниях

  -верхний, нижний регистр в адресе

- /reverse Проверка поиска по широте и долготе

### Стек технологий
- Python
- Pytest
- Requests
- Allure

### Автор

Иван Корец
