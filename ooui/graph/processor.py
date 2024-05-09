from __future__ import absolute_import, unicode_literals
from ooui.graph.fields import get_value_and_label_for_field, get_value_for_operator
from ooui.graph.axis import get_y_axis_fieldname
from ooui.graph.timerange import process_timerange_data


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
    if options is None:
        options = {}

    values_grouped_by_x = get_values_grouped_by_field(
        ooui.x.name, fields, values
    )

    data = []

    # Iterate through the y-axis items
    for y_field in ooui.y:
        for x_value, group in values_grouped_by_x.items():
            x_label = group['label']
            objects_for_x_value = group['entries']

            if not y_field.label:
                values_for_y_field = get_values_for_y_field(
                    objects_for_x_value, y_field.name, fields
                )
                final_value = get_value_for_operator(
                    y_field.operator, values_for_y_field
                )

                data.append({
                    'x': x_label or False,
                    'value': final_value,
                    'type': get_y_axis_fieldname(y_field, fields),
                    'operator': y_field.operator,
                    'stacked': y_field.stacked
                })
            else:
                values_grouped_by_y_label = get_values_grouped_by_field(
                    y_field.label, fields, objects_for_x_value
                )

                for y_unique_value, grouped_entries in values_grouped_by_y_label.items():
                    entries = grouped_entries['entries']
                    label = grouped_entries['label']

                    values_for_y_field = get_values_for_y_field(
                        entries, y_field.name, fields
                    )
                    final_value = get_value_for_operator(
                        y_field.operator, values_for_y_field
                    )

                    data.append({
                        'x': x_label or False,
                        'value': final_value,
                        'type': label,
                        'operator': y_field.operator,
                        'stacked': y_field.stacked
                    })

    # Check if data should be flagged as grouped or stacked
    is_group = any(y.label is not None for y in ooui.y)
    is_stack = any(y.stacked is not None for y in ooui.y)

    # Sort the data by the x-axis
    sorted_data = sorted(data, key=lambda x: x['x'] or "")

    adjusted_stacked_data = sorted_data[:]
    if is_stack and len([y for y in ooui.y if y.stacked is not None]) > 1:
        adjusted_stacked_data = [
            dict(
                entry,
                type="{} - {}".format(entry['type'], entry['stacked'])
            ) for entry in sorted_data
        ]

    adjusted_uninformed_data = adjusted_stacked_data[:]
    if ooui.type == 'pie' and any(entry['x'] is False for entry in adjusted_stacked_data):
        adjusted_uninformed_data = [
            dict(
                entry,
                x=options.get('uninformedString', 'Not informed') if entry['x'] is False else entry['x']
            ) for entry in adjusted_stacked_data
        ]
    else:
        adjusted_uninformed_data = [
            entry for entry in adjusted_stacked_data if entry['x'] is not False
        ]

    # Fill gaps if a timerange is defined
    final_data = adjusted_uninformed_data
    if ooui.timerange:
        final_data = process_timerange_data(
            final_data, ooui.timerange, ooui.interval
        )
    elif ooui.type == 'pie':
        final_data = sorted(
            adjusted_uninformed_data, key=lambda x: x['value'], reverse=True
        )

    return {
        'data': final_data,
        'isGroup': is_stack or is_group,
        'isStack': is_stack
    }


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
