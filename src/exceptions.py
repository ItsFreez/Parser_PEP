class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class NotFoundVersionsException(Exception):
    """Вызывается, когда парсер не может найти список версий Python."""
    pass
