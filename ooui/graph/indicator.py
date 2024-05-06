from ooui.graph.base import Graph
from ooui.helpers import parse_bool_attribute, replace_entities


class GraphIndicator(Graph):
    def __init__(self, graph_type, element):
        # Inicia la classe base Graph
        super(GraphIndicator, self).__init__(element)

        self._type = graph_type
        self._color = replace_entities(element.get('color')) if element.get(
            'color') else None
        self._icon = replace_entities(element.get('icon')) if element.get(
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
