from __future__ import absolute_import, unicode_literals
from ooui.graph.fields import get_value_and_label_for_field


def process_graph_data(ooui, values, fields, options=None):
    """
    Process graph data by grouping and sorting the values according to the
    specified X and Y axes.

    :param ooui: A GraphChart-like object containing chart information.
    :type ooui: ooui.graph.GraphChart
    :param list values: A list of dictionaries representing the original data.
    :param dict fields: A dictionary of field definitions.
    :param dict options: Optional additional options for processing graph data.

    :rtype: dict
    :returns: A dictionary containing the final processed data and flags like
        isGroup and isStack.
    """
    if ooui.type == "indicatorField":
        return ooui.process(values, fields)
    else:
        return ooui.process(values, fields, options=options)


def get_values_for_y_field(entries, field_name, fields):
    """
    Retrieve labels for a specified field across multiple entries.

    :param list entries: A list of dictionaries representing the entries.
    :param str field_name: The name of the field for which to retrieve labels.
    :param dict fields: A dictionary containing the field definitions.
    :param func get_value_and_label_for_field: Function to retrieve value and
        label for a field.

    :rtype: list
    :returns: A list containing the labels corresponding to the specified field.
    """
    return [
        get_value_and_label_for_field(fields, entry, field_name)['label']
        for entry in entries
    ]


def get_values_grouped_by_field(field_name, fields, values):
    """
    Group values by a specific field.

    :param str field_name: The name of the field by which to group values.
    :param dict fields: A dictionary containing field definitions.
    :param list values: A list of dictionaries representing the values to be
        grouped.

    :rtype: dict
    :returns: A dictionary where keys are field values and values are
        dictionaries containing a label and an "entries" list.
    """
    grouped_values = {}

    for entry in values:
        result = get_value_and_label_for_field(fields, entry, field_name)
        value, label = result['value'], result['label']

        if value not in grouped_values:
            grouped_values[value] = {'label': label, 'entries': []}

        grouped_values[value]['entries'].append(entry)

    return grouped_values


def get_all_objects_in_grouped_values(grouped):
    """
    Retrieve all objects within grouped values.

    :param dict grouped: A dictionary where keys are group identifiers and
        values are dictionaries with a key "entries" containing lists of
        objects.

    :rtype: list
    :returns: A list containing all objects from each group's "entries".
    """
    total_objects = []

    for key in grouped:
        group = grouped[key]
        total_objects.extend(group['entries'])

    return total_objects


def get_min_max(values, margin=0.1):
    """
    Calculate the minimum and maximum values from a list of dictionaries.
    :param values: List of dictionaries.
    :param margin: Margin to add to the min and max values.
    :return: Dictionary with 'min' and 'max' keys.
    """
    if not values:
        raise ValueError("The values array cannot be empty.")

    value_list = [d['value'] for d in values]
    min_value = min(value_list)
    max_value = max(value_list)
    calculated_margin = (max_value - min_value) * margin

    return {
        'min': int(min_value - calculated_margin),
        'max': int(max_value + calculated_margin),
    }
