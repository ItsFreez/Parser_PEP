import logging

from requests import RequestException
from bs4 import BeautifulSoup

from exceptions import ParserFindTagException


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )


def get_soup(session, url):
    response = get_response(session, url)
    if response is None:
        return None
    return BeautifulSoup(response.text, features='lxml')


def find_tag(soup, tag, string=None, attrs=None):
    if string is not None:
        searched_tag = soup.find(
            lambda tag_search: tag_search.name == tag
            and string in tag_search.text,
            attrs=(attrs or {})
        )
    else:
        searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {string} {attrs}'
        raise ParserFindTagException(error_msg)
    return searched_tag
