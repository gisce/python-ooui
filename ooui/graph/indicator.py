from ooui.graph.base import Graph
from ooui.helpers import parse_bool_attribute, replace_entities
from ooui.helpers.conditions import ConditionParser
from ooui.graph.fields import get_value_for_operator


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
        self._total_domain = replace_entities(
            element.get('totalDomain')) if element.get('totalDomain') else None
        self._show_percent = parse_bool_attribute(
            element.get('showPercent')) if element.get('showPercent') else False

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


class GraphIndicatorField(GraphIndicator):

    def __init__(self, graph_type, element):
        super(GraphIndicatorField, self).__init__(graph_type, element)
        self._fields = [f for f in element if f.tag == 'field']

    @property
    def fields(self):
        return [f.get('name') for f in self._fields]

    def process(self, values, fields, options=None):
        result = 0
        for field in self._fields:
            data = [v[field.get('name')] for v in values]
            result += get_value_for_operator(field.get('operator'), data)
        return {
            'value': result,
        }
