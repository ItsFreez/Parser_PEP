# main.py
import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, DOWNLOADS_DIR, EXPECTED_STATUS,
                       MAIN_DOC_URL, PEP_DOC_URL)
from exceptions import NotFoundVersionsException
from outputs import control_output
from utils import get_soup, find_tag

LOGGING_DOWNLOAD = 'Архив был загружен и сохранён: {0}'
LOGGING_URL = 'Не удалось получить информацию по ссылке: {0}'


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = get_soup(session, whats_new_url)
    if soup is None:
        logging.info(LOGGING_URL.format(whats_new_url))
        return
    sections_by_python = soup.select(
        '#what-s-new-in-python div.toctree-wrapper li.toctree-l1'
    )
    missed_urls = ['Не удалось получить информацию со следующих ссылок:']
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        href = section.select_one('a')['href']
        version_link = urljoin(whats_new_url, href)
        soup = get_soup(session, version_link)
        if soup is None:
            missed_urls.append(f'{version_link}')
            continue
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append((version_link, h1.text, dl_text))
    if len(missed_urls) > 1:
        logging.info('\n'.join(missed_urls))
    return results


def latest_versions(session):
    soup = get_soup(session, MAIN_DOC_URL)
    if soup is None:
        logging.info(LOGGING_URL.format(MAIN_DOC_URL))
        return
    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise NotFoundVersionsException('Не были найдены версии Python')
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((a_tag['href'], version, status))
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = get_soup(session, downloads_url)
    if soup is None:
        logging.info(LOGGING_URL.format(MAIN_DOC_URL))
        return
    main_tag = find_tag(soup, 'div', attrs={'role': 'main'})
    table_tag = find_tag(main_tag, 'table', attrs={'class': 'docutils'})
    pdf_a4_link = find_tag(
        table_tag, 'a', attrs={'href': re.compile(r'.+pdf-a4\.zip$')}
    )['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / DOWNLOADS_DIR
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(LOGGING_DOWNLOAD.format(archive_path))


def pep(session):
    soup = get_soup(session, PEP_DOC_URL)
    if soup is None:
        logging.info(LOGGING_URL.format(PEP_DOC_URL))
        return
    rows = soup.select('#numerical-index tbody tr')
    count_status = defaultdict(int)
    missed_urls = ['Не удалось получить информацию со следующих ссылок:']
    mismatched_status = ['Несовпадающие статусы:']
    for row in tqdm(rows):
        preview_status = find_tag(row, 'abbr').text[1:]
        href_pep = find_tag(row, 'a')['href']
        link_pep = urljoin(PEP_DOC_URL, href_pep)
        soup_pep = get_soup(session, link_pep)
        if soup_pep is None:
            missed_urls.append(f'{link_pep}')
            continue
        row_status = find_tag(soup_pep, 'dt', string='Status')
        real_status = row_status.find_next_sibling('dd').text
        if real_status not in EXPECTED_STATUS[preview_status]:
            mismatched_status.extend(
                (f'{link_pep}',
                 f'Статус в карточке: {real_status}',
                 f'Ожидаемые статусы: {EXPECTED_STATUS[preview_status]}')
            )
        count_status[real_status] += 1
    if len(missed_urls) > 1:
        logging.info('\n'.join(missed_urls))
    if len(mismatched_status) > 1:
        logging.info('\n'.join(mismatched_status))
    return [
        ('Статус', 'Количество'),
        *count_status.items(),
        ('Всего', sum(count_status.values()))
    ]


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    try:
        configure_logging()
        logging.info('Парсер запущен!')
        arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
        args = arg_parser.parse_args()
        logging.info(f'Аргументы командной строки: {args}')
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
    except NotFoundVersionsException as exc:
        logging.exception(
            'Возникла ошибка при поиске версий Python', exc_info=exc
        )
    except Exception as exc:
        logging.exception('Возникла непредвиденная ошибка', exc_info=exc)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
