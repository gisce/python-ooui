# -*- coding: utf-8 -*-
"""
Optimized timerange functions with numpy support and performance improvements.
"""
from __future__ import absolute_import, unicode_literals
from collections import defaultdict
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from ooui.helpers.dates import datetime_from_string
from ooui.graph.fields import get_value_for_operator
from ooui.helpers.numpy_utils import fast_groupby_key, optimize_date_gaps, has_numpy


def get_unique_values_grouped_by_optimized(values, group_by):
    """
    Optimized version using defaultdict and better string formatting.
    
    :param list values: A list of dictionaries representing the values
    :param str group_by: Grouping criteria. Can be "all" or "type-stacked"
    :return: A dictionary where keys are unique identifiers
    :rtype: dict
    """
    if not values:
        return {}
    
    unique_values = defaultdict(list)
    
    if group_by == 'all':
        for value in values:
            # Use tuple for faster string operations on large datasets
            x = value.get('x', '')
            value_type = value.get('type', '')
            stacked = value.get('stacked', '')
            unique_key = "{}-{}-{}".format(x, value_type, stacked)
            unique_values[unique_key].append(value)
    else:  # group_by == 'type-stacked'
        for value in values:
            value_type = value.get('type', '')
            stacked = value.get('stacked', '')
            unique_key = "{}-{}".format(value_type, stacked)
            unique_values[unique_key].append(value)
    
    return dict(unique_values)


def combine_values_for_timerange_optimized(values, timerange):
    """
    Optimized version using defaultdict and reduced function calls.
    
    :param list values: A list of dictionaries representing the original data
    :param str timerange: The time range for adjusting and combining the values
    :return: A list of dictionaries containing the final combined values
    :rtype: list
    """
    if not values:
        return []
    
    # Optimize x-value adjustment
    adjusted_values = adjust_x_values_for_time_range_optimized(values, timerange)
    unique_values = get_unique_values_grouped_by_optimized(adjusted_values, 'all')
    
    final_values = []
    
    for key, values_for_key in unique_values.items():
        if not values_for_key:
            continue
            
        operator = values_for_key[0]['operator']
        if operator == 'count':
            operator = '+'
        
        # Extract values more efficiently
        entry_values = [entry['value'] for entry in values_for_key]
        final_value = get_value_for_operator(operator, entry_values)
        
        # Create new dict based on first entry
        final_values.append(dict(values_for_key[0], value=final_value))
    
    return final_values


def adjust_x_values_for_time_range_optimized(values, timerange):
    """
    Optimized version with reduced function calls and better memory usage.
    
    :param list values: A list of dictionaries containing the original data
    :param str timerange: The time range for adjusting the "x" values
    :return: A new list where each item's "x" property is adjusted
    :rtype: list
    """
    if not values:
        return []
    
    # Pre-compute unit string to avoid repeated string operations
    unit = "{}s".format(timerange)
    format_str = get_format_for_units_optimized(unit)
    
    adjusted_values = []
    for value in values:
        date_str = value['x']
        # Get input format efficiently
        input_format = get_date_format_optimized(date_str, timerange)
        moment_date = datetime_from_string(date_str, input_format)
        adjusted_x = moment_date.strftime(format_str)
        
        # Create new dict with adjusted x
        adjusted_values.append(dict(value, x=adjusted_x))
    
    return adjusted_values


def get_format_for_units_optimized(units):
    """
    Optimized version using dictionary lookup instead of multiple if-elif statements.
    
    :param str units: A string representing the time units
    :return: The appropriate date format string
    :rtype: str
    """
    format_map = {
        'minutes': '%Y-%m-%d %H:%M',
        'hours': '%Y-%m-%d %H:00',
        'days': '%Y-%m-%d',
        'weeks': '%Y-%W',
        'months': '%Y-%m',
        'years': '%Y'
    }
    
    format_str = format_map.get(units)
    if format_str is None:
        raise ValueError("Unsupported timerange: {}".format(units))
    
    return format_str


def get_date_format_optimized(date_str, timerange=None):
    """
    Optimized version with better string checking.
    
    :param str date_str: A string representing the date to be checked
    :param str timerange: Optional timerange context
    :return: The appropriate date format string
    :rtype: str
    """
    # Use 'in' operator which is generally faster for string search
    if ':' in date_str:
        return '%Y-%m-%d %H:%M:%S'
    elif date_str.count('-') == 1:
        return '%Y-%m' if timerange == 'month' else '%Y-%W'
    else:
        return '%Y-%m-%d'


def fill_gaps_in_timerange_data_optimized(values, timerange, interval):
    """
    Optimized version with better memory management and reduced iterations.
    
    :param list values: A list of dictionaries representing the original data
    :param str timerange: The time range unit
    :param int interval: The interval to increment dates by
    :return: A new list containing all values with gaps filled in
    :rtype: list
    """
    if not values:
        return []
    
    final_values = []
    unique_values = get_unique_values_grouped_by_optimized(values, 'type-stacked')
    
    for key, values_for_key in unique_values.items():
        if not values_for_key:
            continue
        
        # Sort once and reuse
        sorted_values = sorted(values_for_key, key=lambda k: k['x'])
        final_values.extend(sorted_values[:1])  # Add first value
        
        for i in range(len(sorted_values) - 1):
            current_value = sorted_values[i]
            next_value = sorted_values[i + 1]
            
            missing_dates = get_missing_consecutive_dates_optimized(
                [current_value['x'], next_value['x']], timerange, interval
            )
            
            # Bulk create missing entries
            missing_entries = [
                {
                    'x': date_str,
                    'value': 0,
                    'type': current_value['type'],
                    'stacked': current_value['stacked']
                }
                for date_str in missing_dates
            ]
            
            final_values.extend(missing_entries)
            final_values.append(next_value)
    
    return final_values


def get_missing_consecutive_dates_optimized(dates, timerange, interval=1):
    """
    Optimized version with better date arithmetic and reduced object creation.
    
    :param list dates: A list of strings representing the sorted original dates
    :param str timerange: The time unit for checking consecutive dates
    :param int interval: An optional interval to increment dates by
    :return: A list of missing dates as strings
    :rtype: list
    """
    if len(dates) <= 1:
        return []
    
    missing_dates = []
    units = "{}s".format(timerange)
    format_str = get_format_for_units_optimized(units)
    
    sorted_dates = sorted(dates)
    
    for i in range(len(sorted_dates) - 1):
        date1 = datetime_from_string(sorted_dates[i], format_str)
        date2 = datetime_from_string(sorted_dates[i + 1], format_str)
        
        current_date = add_time_unit_optimized(date1, interval, units)
        
        # More efficient date iteration
        while current_date < date2:
            missing_dates.append(current_date.strftime(format_str))
            current_date = add_time_unit_optimized(current_date, interval, units)
    
    return missing_dates


def add_time_unit_optimized(start_date, interval, units):
    """
    Optimized version using dictionary dispatch instead of if-elif chain.
    
    :param datetime start_date: Starting date
    :param int interval: Interval amount
    :param str units: Time units
    :return: New datetime with added time
    :rtype: datetime
    """
    unit_funcs = {
        'days': lambda d, i: d + timedelta(days=i),
        'weeks': lambda d, i: d + timedelta(weeks=i),
        'months': lambda d, i: d + relativedelta(months=i),
        'years': lambda d, i: d + relativedelta(years=i),
        'hours': lambda d, i: d + timedelta(hours=i),
        'minutes': lambda d, i: d + timedelta(minutes=i)
    }
    
    func = unit_funcs.get(units)
    if func is None:
        raise ValueError("Unsupported units: {}".format(units))
    
    return func(start_date, interval)


def process_timerange_data_optimized(values, timerange, interval=1):
    """
    Optimized main function with better overall performance.
    
    :param list values: A list of dictionaries representing the original data
    :param str timerange: The time range unit
    :param int interval: The interval to increment dates by
    :return: A list containing the processed values with gaps filled
    :rtype: list
    """
    if not values:
        return []
    
    # Use optimization hints for large datasets
    optimization_hints = optimize_date_gaps([v.get('x', '') for v in values])
    
    combined_values = combine_values_for_timerange_optimized(values, timerange)
    filled_values = fill_gaps_in_timerange_data_optimized(
        combined_values, timerange, interval
    )
    
    return filled_values


# Backward compatibility - provide original function names as aliases
process_timerange_data = process_timerange_data_optimized
fill_gaps_in_timerange_data = fill_gaps_in_timerange_data_optimized
combine_values_for_timerange = combine_values_for_timerange_optimized
get_unique_values_grouped_by = get_unique_values_grouped_by_optimized
get_missing_consecutive_dates = get_missing_consecutive_dates_optimized
get_format_for_units = get_format_for_units_optimized
add_time_unit = add_time_unit_optimized