from mamba import *
from expects import *
from ooui.graph import parse_graph


with description('Graph Y-axis slider'):
    with it('leaves old line and bar payloads unchanged without a slider'):
        fields = {'name': {'type': 'char'}, 'amount': {'type': 'integer'}}
        values = [{'name': 'January', 'amount': 10}]
        for graph_type in ('line', 'bar'):
            xml = ('<graph type="{}"><field name="name" axis="x"/>'
                   '<field name="amount" axis="y" operator="+"/>'
                   '</graph>').format(graph_type)
            result = parse_graph(xml).process(values, fields)
            expect(result).not_to(have_key('yAxisOpts'))

    with it('returns slider metadata for line and bar without removing legacy axis props'):
        fields = {'name': {'type': 'char'}, 'amount': {'type': 'integer', 'string': 'Amount'}}
        values = [{'name': 'January', 'amount': 10}]
        for graph_type in ('line', 'bar'):
            xml = ('<graph type="{}" y_range="slider">'
                   '<field name="name" axis="x"/>'
                   '<field name="amount" axis="y" operator="+"/>'
                   '</graph>').format(graph_type)
            result = parse_graph(xml).process(values, fields)
            expect(result['yAxisOpts']).to(equal({'mode': 'slider'}))
            if graph_type == 'line':
                expect(result['yAxisProps']).to(equal({'mode': 'slider'}))
