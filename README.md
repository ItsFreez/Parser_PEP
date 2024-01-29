# Проект парсинга pep

## Описание
Парсер предназначен для сбора информации о нововведениях Python, подсчета количества PEP и их статусов, а также для скачивания актуальной документации.

### Функции парсера:

* Сбор ссылок на статьи о нововведениях в Python;
* Сбор информации о версиях Python;
* Скачивание архива с актуальной документацией;
* Сбор статусов документов PEP и подсчёт их статусов;
* Вывод информации в терминал (в обычном и табличном виде) и сохранение результатов работы парсинга в формате csv;
* Логирование работы парсера;
* Обработка ошибок в работе парсера.

## Применяемые технологии

[![Python](https://img.shields.io/badge/Python-3.9-blue?style=flat-square&logo=Python&logoColor=3776AB&labelColor=d0d0d0)](https://www.python.org/)
[![Beautiful Soup 4](https://img.shields.io/badge/BeautifulSoup-4.9.3-blue?style=flat-square&labelColor=d0d0d0)](https://beautiful-soup-4.readthedocs.io)

### Порядок действий для запуска парсера

Клонировать репозиторий и перейти в папку c проектом:

```
git clone git@github.com:ItsFreez/bs4_parser_pep.git
```

```
cd bs4_parser_pep
```

Cоздать и активировать виртуальное окружение:

*Для Windows*
```
python -m venv env
source venv/Scripts/Activate
```
*Для MacOS/Linux*
```
python3 -m venv env
source env/bin/activate
```

Обновить менеджер pip и установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

## Работа с парсером

### Режимы работы
Сбор ссылок на статьи о нововведениях в Python:
```
python main.py whats-new
```
Сбор информации о последних версиях Python:
```
python main.py latest-versions
```
Скачивание архива с актуальной документацией:
```
python main.py download
```
Сбор статусов PEP и подсчет их количества:
```
python main.py pep
```

### Аргументы командной строки
Полный список аргументов:
```
python main.py -h
```
```
usage: main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}

Парсер документации Python

positional arguments:
  {whats-new,latest-versions,download,pep}
                        Режимы работы парсера

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```

## Директории для файлов с результатами парсинга
* _downloads_ - для архива с документацией Python;
* _results_ - для результатов парсинга;
* _logs_ - для логов.
