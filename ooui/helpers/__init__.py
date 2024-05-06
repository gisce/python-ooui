import six


def parse_bool_attribute(attribute):
    """
    Parse a boolean attribute.
    :param attribute:
    :return: bool
    """
    return str(attribute).lower() in ("1", "true")


def replace_entities(text):
    """
    Replace all HTML entities with their respective unicode characters.
    :param text:
    :return:
    """
    if six.PY2:
        from HTMLParser import HTMLParser
        parser = HTMLParser()
        return parser.unescape(text)
    else:
        import html
        return html.unescape(text)
