from ooui.graph.base import Graph
from ooui.graph.axis import parse_xy_axis


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
