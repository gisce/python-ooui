from __future__ import division
from ooui.graph.base import Graph
from ooui.helpers import (
    parse_bool_attribute, replace_entities, ConditionParser, Domain
)
from ooui.graph.fields import get_value_for_operator, round_number


class GraphIndicator(Graph):
    def __init__(self, graph_type, element):
        # Inicia la classe base Graph
        super(GraphIndicator, self).__init__(element)

        self._type = graph_type
        self._color = ConditionParser(replace_entities(element.get('color'))) if element.get(
            'color') else None
        self._icon = ConditionParser(replace_entities(element.get('icon'))) if element.get(
            'icon') else None
        self._suffix = element.get('suffix') if element.get('suffix') else None
        self._total_domain = Domain(replace_entities(
            element.get('totalDomain')) if element.get('totalDomain') else None)
        self._total_domain = element.get('totalDomain') and Domain(
            replace_entities(element.get('totalDomain'))
        ) or None
        self._show_percent = parse_bool_attribute(
            element.get('showPercent')) if element.get('showPercent') else False
        self.domain_parse_values = {}

    @property
    def color(self):
        return self._color

    @property
    def icon(self):
        return self._icon

    @property
    def total_domain(self):
        return self._total_domain

    @property
    def show_percent(self):
        return self._show_percent

    @property
    def suffix(self):
        return self._suffix

    def process(self, value, total=0):
        res = {
            'value': value,
            'total': total,
            'type': self.type,
            'percent': 0,
        }
        if total:
            res['percent'] = round_number(value / total * 100)
        if self.suffix:
            res['suffix'] = self.suffix
        if self.color:
            res['color'] = self.color.eval(res)
        if self.icon:
            res['icon'] = self.icon.eval(res)
        if not self.show_percent:
            res.pop('percent', None)
        return res


class GraphIndicatorField(GraphIndicator):

    def __init__(self, graph_type, element):
        super(GraphIndicatorField, self).__init__(graph_type, element)
        self._fields = [f for f in element if f.tag == 'field']

    @property
    def fields(self):
        return [f.get('name') for f in self._fields]

    def process(self, values, fields, total_values=None):
        if total_values is None:
            total_values = []
        value = 0
        total = 0
        for field in self._fields:
            data = [v[field.get('name')] for v in values]
            value += get_value_for_operator(field.get('operator'), data)
            total_data = [v[field.get('name')] for v in total_values]
            total += get_value_for_operator(field.get('operator'), total_data)
        return super(GraphIndicatorField, self).process(value, total)
