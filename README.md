# Парсер PEP

## Описание
**Парсер PEP** собирает информацию о нововведениях Python, подсчитывает количество PEP и их статусы, а также скачивает актуальную документацию.

### Функции парсера:

* Сбор ссылок на статьи о нововведениях в Python;
* Сбор информации о версиях Python;
* Скачивание архива с актуальной документацией;
* Сбор статусов документов PEP и подсчёт их статусов;
* Вывод информации в терминал (в обычном и табличном виде) и сохранение результатов работы парсинга в формате csv;
* Логирование работы парсера;
* Обработка ошибок в работе парсера.

## Стек технологий

![](https://img.shields.io/badge/Python-3.9-black?style=flat&logo=python)
![](https://img.shields.io/badge/BeautifulSoup-4.9.3-black?style=flat&logo=beautifulsoup)

## Порядок действий для запуска парсера

***1. Клонировать репозиторий и перейти в папку c проектом***

```shell
git git@github.com:ItsFreez/Parser_PEP.git
```

```shell
cd Parser_PEP
```

***2. Cоздать и активировать виртуальное окружение***

*Для Windows*
```shell
python -m venv env
source venv/Scripts/Activate
```
*Для MacOS/Linux*
```shell
python3 -m venv env
source env/bin/activate
```

***3. Обновить менеджер pip и установить зависимости из файла requirements.txt***

```shell
python -m pip install --upgrade pip
```

```shell
pip install -r requirements.txt
```

## Работа с парсером

### Режимы работы
Сбор ссылок на статьи о нововведениях в Python:
```shell
python main.py whats-new
```
Сбор информации о последних версиях Python:
```shell
python main.py latest-versions
```
Скачивание архива с актуальной документацией:
```shell
python main.py download
```
Сбор статусов PEP и подсчет их количества:
```shell
python main.py pep
```

### Аргументы командной строки
Полный список аргументов:
```shell
python main.py -h
```
```shell
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

### Директории для файлов с результатами парсинга
* _downloads_ - для архива с документацией Python;
* _results_ - для результатов парсинга;
* _logs_ - для логов.

### Автор проекта

[ItsFreez](https://github.com/ItsFreez)
