from datetime import datetime

def datetime_from_string(string, format_str):
    if format_str == '%Y-%W':
        # The "%W" format string doesn't work with strptime, so we need to
        # manually parse the week number and year.
        return datetime.strptime(string + '-0', '%Y-%W-%w')
    elif format_str == "%Y-%m-%d":
        return datetime.strptime(string[:10], format_str)
    elif format_str == "%Y-%m-%d %H:%M":
        return datetime.strptime(string[:16], format_str)
    return datetime.strptime(string, format_str)