from __future__ import absolute_import, unicode_literals
from lxml import etree
from ooui.graph.indicator import GraphIndicator
from ooui.graph.chart import GraphChart


GRAPH_TYPES = {
    'indicator': GraphIndicator,
    'line': GraphChart,
}


def parse_graph(xml):
    """
    Parse a graph from an XML string.
    :param xml:
    :return:
    """
    tree = etree.fromstring(xml)
    graph = tree.xpath('//graph')[0]

    graph_type = graph.get("type")

    if not graph_type or graph_type not in GRAPH_TYPES:
        raise ValueError("{} is not a valid graph".format(graph_type))

    return GRAPH_TYPES[graph_type](graph_type, graph)
