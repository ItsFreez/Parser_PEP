class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""


class NotFoundVersionsException(Exception):
    """Вызывается, когда парсер не может найти список версий Python."""
