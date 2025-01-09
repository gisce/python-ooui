from datetime import datetime

def datetime_from_string(string, format_str):
    if format_str == '%Y-%W':
        # The "%W" format string doesn't work with strptime, so we need to
        # manually parse the week number and year.
        return datetime.strptime(string + '-0', '%Y-%W-%w')
    return datetime.strptime(string, format_str)