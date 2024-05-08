class GraphAxis(object):
    AXIS_OPTIONS = ('x', 'y')

    def __init__(self, name, axis):
        if axis not in self.AXIS_OPTIONS:
            raise ValueError("Invalid axis value. Must be 'x' or 'y'.")

        self._name = name
        self._axis = axis

    @property
    def name(self):
        return self._name

    @property
    def axis(self):
        return self._axis


class GraphXAxis(GraphAxis):
    def __init__(self, name):
        # Crida el constructor de GraphAxis amb l'eix 'x' fixat
        super(GraphXAxis, self).__init__(name, 'x')


class GraphYAxis(GraphAxis):
    OPERATOR_OPTIONS = ('count', '+', '-', '*', 'min', 'max', 'avg')

    def __init__(self, name, operator, label=None, stacked=None):
        super(GraphYAxis, self).__init__(name, 'y')

        if operator not in self.OPERATOR_OPTIONS:
            raise ValueError("Invalid operator value.")

        self._operator = operator
        self._label = label
        self._stacked = stacked

    @property
    def operator(self):
        return self._operator

    @property
    def label(self):
        return self._label

    @property
    def stacked(self):
        return self._stacked


def parse_xy_axis(nodes):
    x_axis = None
    y_axes = []

    for child in nodes:
        if child.tag == "field":
            axis = child.get("axis")
            name = child.get("name")
            operator = child.get("operator")
            label = child.get("label")
            stacked = child.get("stacked")

            if not axis:
                raise ValueError("Field {} doesn't have an axis".format(name))

            if not name:
                raise ValueError("Missing name attribute for field")

            if axis == "x":
                x_axis = GraphXAxis(name)
            elif axis == "y":
                y_axes.append(GraphYAxis(name, operator, label, stacked))

    if not x_axis:
        raise ValueError("No x axis found")

    if not y_axes:
        raise ValueError("No y axis found. At least one y axis is required")

    return {"x": x_axis, "y": y_axes}


def get_y_axis_fieldname(y_axis, fields):
    """
    Retrieve the field name for a Y-axis based on the `GraphYAxis` object
    and field definitions.

    :param GraphYAxis y_axis: An object representing the Y-axis.
    :param dict fields: A dictionary containing the field definitions.

    :rtype: str
    :returns: The name of the Y-axis field.
    """
    field_props = fields.get(y_axis.name, {})

    if 'string' in field_props and field_props['string']:
        return field_props['string']

    return y_axis.name
