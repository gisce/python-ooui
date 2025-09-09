# -*- coding: utf-8 -*-
"""
Optimized processor functions with numpy support.
"""
from __future__ import absolute_import, unicode_literals
from collections import defaultdict

from ooui.graph.fields import get_value_and_label_for_field
from ooui.helpers.numpy_utils import array_min_max, fast_groupby_key, has_numpy


def get_min_max_optimized(values, margin=0.1):
    """
    Optimized version of get_min_max using numpy if available.
    
    :param list values: List of dictionaries with 'value' key
    :param float margin: Margin to add to min/max values  
    :return: Dictionary with 'min' and 'max' keys
    :rtype: dict
    """
    if not values:
        raise ValueError("The values array cannot be empty.")
    
    # Extract values efficiently
    value_list = [d['value'] for d in values]
    
    # Use optimized min/max calculation
    return array_min_max(value_list, margin)


def get_values_grouped_by_field_optimized(field_name, fields, values):
    """
    Optimized version of get_values_grouped_by_field using better data structures.
    
    :param str field_name: The name of the field by which to group values
    :param dict fields: A dictionary containing field definitions
    :param list values: A list of dictionaries representing the values to be grouped
    :return: A dictionary where keys are field values and values are dictionaries
    :rtype: dict
    """
    if not values:
        return {}
    
    # Use defaultdict for more efficient grouping
    grouped_values = defaultdict(lambda: {'label': None, 'entries': []})
    
    for entry in values:
        result = get_value_and_label_for_field(fields, entry, field_name)
        value, label = result['value'], result['label']
        
        # Set label only once per group
        if grouped_values[value]['label'] is None:
            grouped_values[value]['label'] = label
            
        grouped_values[value]['entries'].append(entry)
    
    # Convert back to regular dict for compatibility
    return dict(grouped_values)


def get_values_for_y_field_optimized(entries, field_name, fields):
    """
    Optimized version using list comprehension.
    
    :param list entries: A list of dictionaries representing the entries
    :param str field_name: The name of the field for which to retrieve labels
    :param dict fields: A dictionary containing the field definitions
    :return: A list containing the labels corresponding to the specified field
    :rtype: list
    """
    # Pre-compile the field lookup if possible
    field_info = fields.get(field_name)
    if not field_info:
        raise ValueError("Field {} not found".format(field_name))
    
    # Optimized list comprehension
    return [
        get_value_and_label_for_field(fields, entry, field_name)['label']
        for entry in entries
    ]


def get_all_objects_in_grouped_values_optimized(grouped):
    """
    Optimized version using list comprehension and reduce overhead.
    
    :param dict grouped: A dictionary where keys are group identifiers
    :return: A list containing all objects from each group's "entries"
    :rtype: list
    """
    if not grouped:
        return []
    
    # Use list comprehension for better performance
    return [
        obj 
        for group in grouped.values() 
        for obj in group['entries']
    ]


def fast_sort_by_key(items, key_func):
    """
    Fast sorting using optimized key extraction.
    
    :param list items: Items to sort
    :param function key_func: Key extraction function
    :return: Sorted list
    :rtype: list
    """
    if not items:
        return []
    
    # Pre-calculate keys to avoid multiple function calls during sort
    if len(items) > 100:
        keyed_items = [(key_func(item), item) for item in items]
        keyed_items.sort(key=lambda x: x[0])
        return [item for _, item in keyed_items]
    else:
        # For smaller lists, standard sort is fine
        return sorted(items, key=key_func)


# Backward compatibility - provide original function names as aliases
get_min_max = get_min_max_optimized
get_values_grouped_by_field = get_values_grouped_by_field_optimized
get_values_for_y_field = get_values_for_y_field_optimized
get_all_objects_in_grouped_values = get_all_objects_in_grouped_values_optimized