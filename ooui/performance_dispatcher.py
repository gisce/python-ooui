# -*- coding: utf-8 -*-
"""
Smart optimization dispatcher that chooses the best implementation based on data size and characteristics.
"""
from __future__ import absolute_import, unicode_literals

from ooui.helpers.numpy_utils import has_numpy

# Original implementations
from ooui.graph.timerange import (
    process_timerange_data as _process_timerange_data_original,
    fill_gaps_in_timerange_data as _fill_gaps_in_timerange_data_original,
    combine_values_for_timerange as _combine_values_for_timerange_original,
    get_unique_values_grouped_by as _get_unique_values_grouped_by_original,
    get_missing_consecutive_dates as _get_missing_consecutive_dates_original
)
from ooui.graph.processor import (
    get_values_grouped_by_field as _get_values_grouped_by_field_original,
    get_min_max as _get_min_max_original
)

# Optimized implementations
from ooui.graph.timerange_optimized import (
    process_timerange_data_optimized,
    fill_gaps_in_timerange_data_optimized,
    combine_values_for_timerange_optimized,
    get_unique_values_grouped_by_optimized,
    get_missing_consecutive_dates_optimized
)
from ooui.graph.processor_optimized import (
    get_values_grouped_by_field_optimized,
    get_min_max_optimized
)

# Performance thresholds - determined from benchmarking
PROCESS_TIMERANGE_THRESHOLD = 500
FILL_GAPS_THRESHOLD = 300
COMBINE_VALUES_THRESHOLD = 400
GROUP_VALUES_THRESHOLD = 800
MIN_MAX_THRESHOLD = 5000
GROUPED_FIELD_THRESHOLD = 600


def smart_process_timerange_data(values, timerange, interval=1):
    """
    Smart dispatcher for process_timerange_data that chooses optimal implementation.
    
    :param list values: A list of dictionaries representing the original data
    :param str timerange: The time range unit
    :param int interval: The interval to increment dates by
    :return: A list containing the processed values with gaps filled
    :rtype: list
    """
    if len(values) >= PROCESS_TIMERANGE_THRESHOLD:
        return process_timerange_data_optimized(values, timerange, interval)
    else:
        return _process_timerange_data_original(values, timerange, interval)


def smart_fill_gaps_in_timerange_data(values, timerange, interval):
    """
    Smart dispatcher for fill_gaps_in_timerange_data.
    
    :param list values: A list of dictionaries representing the original data
    :param str timerange: The time range unit
    :param int interval: The interval to increment dates by
    :return: A new list containing all values with gaps filled in
    :rtype: list
    """
    if len(values) >= FILL_GAPS_THRESHOLD:
        return fill_gaps_in_timerange_data_optimized(values, timerange, interval)
    else:
        return _fill_gaps_in_timerange_data_original(values, timerange, interval)


def smart_combine_values_for_timerange(values, timerange):
    """
    Smart dispatcher for combine_values_for_timerange.
    
    :param list values: A list of dictionaries representing the original data
    :param str timerange: The time range for adjusting and combining the values
    :return: A list of dictionaries containing the final combined values
    :rtype: list
    """
    if len(values) >= COMBINE_VALUES_THRESHOLD:
        return combine_values_for_timerange_optimized(values, timerange)
    else:
        return _combine_values_for_timerange_original(values, timerange)


def smart_get_unique_values_grouped_by(values, group_by):
    """
    Smart dispatcher for get_unique_values_grouped_by.
    
    :param list values: A list of dictionaries representing the values
    :param str group_by: Grouping criteria
    :return: A dictionary where keys are unique identifiers
    :rtype: dict
    """
    if len(values) >= GROUP_VALUES_THRESHOLD:
        return get_unique_values_grouped_by_optimized(values, group_by)
    else:
        return _get_unique_values_grouped_by_original(values, group_by)


def smart_get_min_max(values, margin=0.1):
    """
    Smart dispatcher for get_min_max that uses numpy for large datasets.
    
    :param list values: List of dictionaries with 'value' key
    :param float margin: Margin to add to min/max values
    :return: Dictionary with 'min' and 'max' keys
    :rtype: dict
    """
    if len(values) >= MIN_MAX_THRESHOLD and has_numpy():
        return get_min_max_optimized(values, margin)
    else:
        return _get_min_max_original(values, margin)


def smart_get_values_grouped_by_field(field_name, fields, values):
    """
    Smart dispatcher for get_values_grouped_by_field.
    
    :param str field_name: The name of the field by which to group values
    :param dict fields: A dictionary containing field definitions
    :param list values: A list of dictionaries representing values to be grouped
    :return: A dictionary where keys are field values
    :rtype: dict
    """
    if len(values) >= GROUPED_FIELD_THRESHOLD:
        return get_values_grouped_by_field_optimized(field_name, fields, values)
    else:
        return _get_values_grouped_by_field_original(field_name, fields, values)


def smart_get_missing_consecutive_dates(dates, timerange, interval=1):
    """
    Smart dispatcher for get_missing_consecutive_dates.
    
    :param list dates: A list of strings representing the sorted original dates
    :param str timerange: The time unit for checking consecutive dates
    :param int interval: An optional interval to increment dates by
    :return: A list of missing dates as strings
    :rtype: list
    """
    # For date processing, optimization shows benefit mainly with larger datasets
    if len(dates) >= 50:
        return get_missing_consecutive_dates_optimized(dates, timerange, interval)
    else:
        return _get_missing_consecutive_dates_original(dates, timerange, interval)


def get_optimization_info():
    """
    Get information about available optimizations and thresholds.
    
    :return: Dictionary with optimization information
    :rtype: dict
    """
    return {
        'numpy_available': has_numpy(),
        'numpy_version': None if not has_numpy() else __import__('numpy').__version__,
        'thresholds': {
            'process_timerange': PROCESS_TIMERANGE_THRESHOLD,
            'fill_gaps': FILL_GAPS_THRESHOLD,
            'combine_values': COMBINE_VALUES_THRESHOLD,
            'group_values': GROUP_VALUES_THRESHOLD,
            'min_max': MIN_MAX_THRESHOLD,
            'grouped_field': GROUPED_FIELD_THRESHOLD
        }
    }


# Export the smart functions as the main API
process_timerange_data = smart_process_timerange_data
fill_gaps_in_timerange_data = smart_fill_gaps_in_timerange_data
combine_values_for_timerange = smart_combine_values_for_timerange
get_unique_values_grouped_by = smart_get_unique_values_grouped_by
get_min_max = smart_get_min_max
get_values_grouped_by_field = smart_get_values_grouped_by_field
get_missing_consecutive_dates = smart_get_missing_consecutive_dates