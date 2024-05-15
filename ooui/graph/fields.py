from functools import reduce


def get_fields_to_retrieve(ooui):
    """
    Returns a list of fields to retrieve from the ooui
    :param ooui: Graph instance
    :type ooui: ooui.graph.chart.GraphChart
    :return: list of fields to retrieve
    :rtype: list[str]
    """
    return ooui.fields


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


def get_value_for_operator(operator, values):
    """
    Retrieve the result of applying an operator on a list of values.

    :param str operator: The operator to be applied.
        Possible values include "count", "+", "-", "*", "avg", "min", "max".
    :param list values: A list of numerical values on which to apply the
        operator.

    :rtype: float or int
    :returns: The result of applying the operator to the values.

    :raises ValueError: If an unsupported operator is provided or if the
        values list is empty for certain operators.
    """
    if operator == "count":
        return len(values)
    elif operator == "+":
        return round_number(sum(values))
    elif operator == "-":
        return round_number(reduce(lambda x, y: x - y, values))
    elif operator == "*":
        return round_number(reduce(lambda x, y: x * y, values))
    elif operator == "avg":
        if not values:
            return 0
        total_sum = sum(values)
        avg = total_sum / len(values)
        return round_number(avg)
    elif operator == "min":
        if not values:
            return 0
        return min(values)
    elif operator == "max":
        if not values:
            return 0
        return max(values)
    else:
        raise ValueError("Unsupported operator: {}".format(operator))


def round_number(num):
    """
    Round a number to two decimal places.

    :param float or int num: The number to be rounded.

    :rtype: float
    :returns: The number rounded to two decimal places.
    """
    return round(num * 100) / 100
