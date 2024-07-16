from __future__ import absolute_import, unicode_literals
from ooui.graph.base import Graph
from ooui.graph.axis import parse_xy_axis
from ooui.graph.fields import get_value_for_operator
from ooui.graph.axis import get_y_axis_fieldname
from ooui.graph.timerange import process_timerange_data
from ooui.graph.processor import (
    get_values_grouped_by_field, get_values_for_y_field, get_min_max
)


class GraphChart(Graph):
    def __init__(self, graph_type, element):
        super(GraphChart, self).__init__(element)

        self._type = graph_type
        xy_axis = parse_xy_axis(element)
        self._x = xy_axis['x']
        self._y = xy_axis['y']

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def fields(self):
        x_field = self.x.name
        fields = [x_field]

        if not self.y:
            return []

        for y in self.y:
            if y.operator != 'count' and y.name not in fields:
                fields.append(y.name)

            if y.label and y.label not in fields:
                fields.append(y.label)

        return fields

    def process(self, values, fields, options=None):
        """
        Process graph data by grouping and sorting the values according to the
        specified X and Y axes.

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
            self.x.name, fields, values
        )

        data = []

        # Iterate through the y-axis items
        for y_field in self.y:
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
        is_group = any(y.label is not None for y in self.y)
        is_stack = any(y.stacked is not None for y in self.y)

        # Sort the data by the x-axis
        sorted_data = sorted(data, key=lambda x: x['x'] or "")

        adjusted_stacked_data = sorted_data[:]
        if is_stack and len([y for y in self.y if y.stacked is not None]) > 1:
            adjusted_stacked_data = [
                dict(
                    entry,
                    type="{} - {}".format(entry['type'], entry['stacked'])
                ) for entry in sorted_data
            ]

        adjusted_uninformed_data = adjusted_stacked_data[:]
        if self.type == 'pie' and any(
                entry['x'] is False for entry in adjusted_stacked_data):
            adjusted_uninformed_data = [
                dict(
                    entry,
                    x=options.get('uninformedString', 'Not informed') if entry['x'] is False else
                    entry['x']
                ) for entry in adjusted_stacked_data
            ]
        else:
            adjusted_uninformed_data = [
                entry for entry in adjusted_stacked_data if
                entry['x'] is not False
            ]

        # Fill gaps if a timerange is defined
        final_data = adjusted_uninformed_data
        if self.timerange:
            final_data = process_timerange_data(
                final_data, self.timerange, self.interval
            )
        if self.type == 'pie':
            final_data = sorted(
                final_data, key=lambda x: x['value'], reverse=True
            )
        else:
            final_data = sorted(
                final_data, key=lambda x: '{x}-{type}'.format(**x)
            )

        result = {
            'data': final_data,
            'isGroup': is_stack or is_group,
            'isStack': is_stack,
            'type': self.type,
            'num_items': len(values),
        }

        if self.type == "line" and self.y_range:
            y_axis_props = {'mode': self.y_range}
            if self.y_range == "auto":
                y_axis_props['valueOpts'] = get_min_max(final_data)
            result['yAxisProps'] = y_axis_props

        return result
