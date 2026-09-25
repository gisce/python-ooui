from mamba import *
from expects import *
from ooui.graph import parse_graph


with description('Graph axis sliders'):
    with it('keeps existing line and bar data without a slider'):
        fields = {'name': {'type': 'char'}, 'amount': {'type': 'integer'}}
        values = [{'name': 'January', 'amount': 10}]
        for graph_type in ('line', 'bar'):
            xml = ('<graph type="{}"><field name="name" axis="x"/>'
                   '<field name="amount" axis="y" operator="+"/>'
                   '</graph>').format(graph_type)
            result = parse_graph(xml).process(values, fields)
            expect(result['data'][0]['x']).to(equal('January'))
            expect(result['data'][0]['value']).to(equal(10))
            expect(result['num_items']).to(equal(1))
            if graph_type == 'line':
                expect(result['yAxisOpts']).to(equal({'mode': 'default'}))
            else:
                expect(result).not_to(have_key('yAxisOpts'))
            expect(result).not_to(have_key('xAxisOpts'))
            expect(result).not_to(have_key('yAxisProps'))

    with it('returns slider metadata for line and bar under one key'):
        fields = {'name': {'type': 'char'}, 'amount': {'type': 'integer', 'string': 'Amount'}}
        values = [{'name': 'January', 'amount': 10}]
        for graph_type in ('line', 'bar'):
            xml = ('<graph type="{}" y_range="slider">'
                   '<field name="name" axis="x"/>'
                   '<field name="amount" axis="y" operator="+"/>'
                   '</graph>').format(graph_type)
            result = parse_graph(xml).process(values, fields)
            expect(result['yAxisOpts']).to(equal({'mode': 'slider'}))
            expect(result).not_to(have_key('xAxisOpts'))
            expect(result).not_to(have_key('yAxisProps'))

    with it('returns an X-axis slider for line and bar independently of Y'):
        fields = {'name': {'type': 'char'}, 'amount': {'type': 'integer'}}
        values = [{'name': 'January', 'amount': 10}]
        for graph_type in ('line', 'bar'):
            xml = ('<graph type="{}" x_range="slider">'
                   '<field name="name" axis="x"/>'
                   '<field name="amount" axis="y" operator="+"/>'
                   '</graph>').format(graph_type)
            result = parse_graph(xml).process(values, fields)
            expect(result['xAxisOpts']).to(equal({'mode': 'slider'}))
            if graph_type == 'line':
                expect(result['yAxisOpts']).to(equal({'mode': 'default'}))
            else:
                expect(result).not_to(have_key('yAxisOpts'))

    with it('returns independent X and Y slider metadata together'):
        fields = {'name': {'type': 'char'}, 'amount': {'type': 'integer'}}
        values = [{'name': 'January', 'amount': 10}]
        xml = ('<graph type="line" x_range="slider" y_range="slider">'
               '<field name="name" axis="x"/>'
               '<field name="amount" axis="y" operator="+"/>'
               '</graph>')
        result = parse_graph(xml).process(values, fields)
        expect(result['xAxisOpts']).to(equal({'mode': 'slider'}))
        expect(result['yAxisOpts']).to(equal({'mode': 'slider'}))
