from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from ooui.graph.fields import get_value_for_operator


def process_timerange_data(values, timerange, interval=1):
    """
    Process time range data by combining values and filling gaps.

    :param list values: A list de diccionaris representing the original data.
    :param str timerange: The time range unit ("day", "week", "month", "year").
    :param int interval: The interval to increment dates by.

    :rtype: list
    :returns: A list containing the processed values with gaps filled.
    """
    combined_values = combine_values_for_timerange(values, timerange)
    filled_values = fill_gaps_in_timerange_data(
        combined_values, timerange, interval
    )

    return filled_values


def fill_gaps_in_timerange_data(values, timerange, interval):
    """
    Fill gaps in time range data by inserting missing dates.

    :param list values: A list of dictionaries representing the original data.
    :param str timerange: The time range unit ("day", "week", "month", "year").
    :param int interval: The interval to increment dates by.

    :rtype: list
    :returns: A new list containing all values with gaps filled in.
    """
    final_values = []
    unique_values = get_unique_values_grouped_by(values, 'type-stacked')

    for key, values_for_key in unique_values.items():
        values_for_key = sorted(values_for_key, key=lambda k: k['x'])
        for i in range(len(values_for_key)):
            value = values_for_key[i]
            final_values.append(value)

            if i == len(values_for_key) - 1:
                break

            date = value['x']
            next_date = values_for_key[i + 1]['x']

            missing_dates = get_missing_consecutive_dates(
                [date, next_date], timerange, interval
            )

            final_values.extend([
                {
                    'x': string_date,
                    'value': 0,
                    'type': value['type'],
                    'stacked': value['stacked']
                } for string_date in missing_dates
            ])

    return final_values


def add_time_unit(start_date, interval, units):
    if units == 'days':
        return start_date + timedelta(days=interval)
    elif units == 'weeks':
        return start_date + timedelta(weeks=interval)
    elif units == 'months':
        return start_date + relativedelta(months=interval)
    elif units == 'years':
        return start_date + relativedelta(years=interval)
    elif units == 'hours':
        return start_date + timedelta(hours=interval)
    else:
        raise ValueError("Unsupported units: {}".format(units))


def get_missing_consecutive_dates(dates, timerange, interval=1):
    """
    Retrieve the missing consecutive dates within a range according to a specific time unit.

    :param list dates: A list of strings representing the sorted original dates.
    :param str timerange: The time unit for checking consecutive dates ("day", "week", "month", "year").
    :param int interval: An optional interval to increment dates by.

    :rtype: list
    :returns: A list of missing dates as strings.
    """
    missing_dates = []
    units = "{}s".format(timerange)
    format_str = get_format_for_units(units)

    if len(dates) == 1:
        return dates

    sorted_dates = sorted(dates)

    for i in range(len(sorted_dates) - 1):
        date1 = datetime.strptime(sorted_dates[i], format_str)
        date2 = datetime.strptime(sorted_dates[i + 1], format_str)

        next_date = add_time_unit(date1, interval, units)

        while next_date < date2:
            missing_dates.append(next_date.strftime(format_str))
            next_date = add_time_unit(next_date, interval, units)

    return missing_dates


def combine_values_for_timerange(values, timerange):
    """
    Combine values according to a specific time range.

    :param list values: A list of dictionaries representing the original data.
    :param str timerange: The time range for adjusting and combining the values.

    :rtype: list
    :returns: A list of dictionaries containing the final combined values.
    """
    adjusted_values = adjust_x_values_for_time_range(values, timerange)
    unique_values = get_unique_values_grouped_by(adjusted_values, 'all')

    final_values = []

    for key, values_for_key in unique_values.items():
        operator = values_for_key[0]['operator']
        if operator == 'count':
            operator = '+'

        final_value = get_value_for_operator(
            operator, [entry['value'] for entry in values_for_key]
        )

        final_values.append(dict(values_for_key[0], value=final_value))

    return final_values


def adjust_x_values_for_time_range(values, timerange):
    """
    Adjust the "x" values in a list of items according to the specified
    time range.

    :param list values: A list of dictionaries containing the original data.
    :param str timerange: The time range for adjusting the "x" values.

    :rtype: list
    :returns: A new list where each item's "x" property is adjusted based on
        the time range.
    """
    return [
        dict(value, x=convert_date_to_time_range_adjusted(value['x'], timerange))
        for value in values
    ]


def convert_date_to_time_range_adjusted(date, timerange):
    """
    Adjust a date to a specific time range format.

    :param str date: The original date string.
    :param str timerange: The time range for adjustment
        ("hour", "day", "week", "month", "year").

    :rtype: str
    :returns: The adjusted date in the specified time range format.
    """
    format_str = get_date_format(date)
    moment_date = datetime.strptime(date, format_str)

    if timerange == 'hour':
        return moment_date.strftime('%Y-%m-%d %H:00')
    elif timerange == 'day':
        return moment_date.strftime('%Y-%m-%d')
    elif timerange == 'week':
        return moment_date.strftime('%Y-%W')
    elif timerange == 'month':
        return moment_date.strftime('%Y-%m')
    elif timerange == 'year':
        return moment_date.strftime('%Y')
    else:
        raise ValueError("Unsupported timerange: {}".format(timerange))


def get_date_format(date_str):
    """
    Determine the appropriate date format string based on whether the input
    string contains a colon.

    :param str date_str: A string representing the date to be checked.

    :rtype: str
    :returns: The appropriate date format string compatible with
        `datetime.strptime`.
    """
    if ':' in date_str:
        return '%Y-%m-%d %H:%M:%S'
    elif date_str.count('-') == 1:
        return '%Y-%m'
    else:
        return '%Y-%m-%d'


def get_unique_values_grouped_by(values, group_by):
    """
    Group values by unique keys determined by the grouping criteria.

    :param list values: A list of dictionaries representing the values.
    :param str group_by: Grouping criteria. Can be "all" or "type-stacked".

    :rtype: dict
    :returns: A dictionary where keys are unique identifiers based on the
        grouping criteria, and values are lists of grouped items.
    """
    unique_values = {}

    for value in values:
        x = value.get('x')
        value_type = value.get('type')
        stacked = value.get('stacked')

        if group_by == 'all':
            unique_key = "{}-{}-{}".format(x, value_type, stacked)
        else:
            unique_key = "{}-{}".format(value_type, stacked)

        if unique_key not in unique_values:
            unique_values[unique_key] = []

        unique_values[unique_key].append(value)

    return unique_values


def get_format_for_units(units):
    """
    Retrieve the appropriate date format string based on the units provided.

    :param str units: A string representing the time units
        (e.g., "days", "weeks", "months", "years", or "hours").

    :rtype: str
    :returns: The appropriate date format string based on the provided units.
    """
    if units == 'days':
        return '%Y-%m-%d'
    elif units == 'weeks':
        return '%Y-%W'
    elif units == 'months':
        return '%Y-%m'
    elif units == 'years':
        return '%Y'
    else:
        return '%Y-%m-%d %H:%M'


def check_dates_consecutive(dates, unit):
    """
    Check if the dates in the list are consecutive based on the provided unit.

    :param list dates: A list of strings representing the dates to be checked.
    :param str unit: The unit to check for consecutiveness ("hours", "days", "weeks", "months", or "years").

    :rtype: bool
    :returns: True if the dates are consecutive in the given unit, otherwise False.
    """
    if len(dates) == 0:
        return False

    if len(dates) == 1:
        return True

    consecutive = False
    format_str = get_format_for_units(unit)

    for i in range(len(dates) - 1):
        date1 = datetime.strptime(dates[i], format_str)
        date2 = datetime.strptime(dates[i + 1], format_str)

        if unit == 'hours':
            diff = (date2 - date1).total_seconds() / 3600
        elif unit == 'days':
            diff = (date2 - date1).days
        elif unit == 'weeks':
            diff = (date2 - date1).days // 7
        elif unit == 'months':
            diff = relativedelta(date2, date1).months + (relativedelta(date2, date1).years * 12)
        elif unit == 'years':
            diff = relativedelta(date2, date1).years
        else:
            raise ValueError("Unsupported unit: {}".format(unit))

        if abs(diff) == 1:
            consecutive = True
        else:
            consecutive = False
            break

    return consecutive
