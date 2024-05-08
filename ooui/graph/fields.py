from ooui.graph.chart import GraphChart


def get_fields_to_retrieve(ooui):
    """
    Returns a list of fields to retrieve from the ooui
    :param ooui: Graph instance
    :type ooui: ooui.graph.chart.GraphChart
    :return: list of fields to retrieve
    :rtype: list[str]
    """
    x_field = ooui.x.name
    fields = [x_field]

    if not ooui.y:
        return []

    for y in ooui.y:
        if y.operator != 'count' and y.name not in fields:
            fields.append(y.name)

        if y.label and y.label not in fields:
            fields.append(y.label)

    return fields


def get_value_and_label_for_field(fields, values, field_name):
    """
    Retrieve the value and label for a specific field.

    :param dict fields: A dictionary containing the field definitions.
        The keys are field names and the values are their details.
    :param dict values: A dictionary containing the field values.
        The keys are field names, and the values are the associated values.
    :param str field_name: The name of the field for which to obtain the value
        and label.

    :rtype: dict
    :returns: A dictionary with the keys `value` and `label`:
        - `value`: The field value or `False` if not found.
        - `label`: The field label or `None` if not found.

    :raises ValueError: If the specified field is not found in the `fields`
        dictionary.
    """
    x_field_data = fields.get(field_name)
    value = values.get(field_name)

    if not x_field_data:
        raise ValueError("Field {} not found".format(field_name))

    if x_field_data['type'] == 'many2one':
        if not value:
            return {'value': False, 'label': None}
        return {'value': value[0], 'label': value[1]}

    elif x_field_data['type'] == 'selection':
        selection_values = x_field_data['selection']
        value_pair = next((pair for pair in selection_values if pair[0] == value), None)

        if not value_pair:
            return {'value': False, 'label': None}

        return {'value': value, 'label': value_pair[1]}

    return {'value': value, 'label': value}
