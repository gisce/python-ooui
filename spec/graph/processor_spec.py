# coding: utf-8
from mamba import description, context, it
from expects import *
import os
import sys

from ooui.graph import parse_graph
from ooui.graph.processor import (
    get_values_grouped_by_field, get_all_objects_in_grouped_values,
    get_values_for_y_field, process_graph_data
)

current_dir = os.path.dirname(os.path.abspath(__file__))
mock_data_dir = os.path.join(current_dir, 'mock')
if mock_data_dir not in sys.path:
    sys.path.insert(0, mock_data_dir)

from lectura import Lectura  # NOQA
from polissa import Polissa  # NOQA

models = {'polissa': Polissa, 'lectura': Lectura}


def get_graph_data(xml, model):
    """
    Util to prosses graph test from an xml and model name
    :param str xml: xml content
    :param str model: model name 'lectura' or 'polissa'
    :return: result of ooui.graph.processor.process_graph_data
    :rtype: dict
    """
    g = parse_graph(xml)
    return process_graph_data(g, models[model].data, models[model].fields)


with description('When process a graph'):

    with it('should process indicatorField graph'):
        xml = """<?xml version="1.0"?>
        <graph string="My indicator" type="indicatorField" color="red:value>0;green:value==0" icon="slack">
            <field name="potencia" operator="+" />
        </graph>
        """
        result = get_graph_data(xml, 'polissa')
        expect(result).to(have_keys(
            value=275.72, color='red'
        ))

    with it('should process indicatorField graph'):
        xml = """<?xml version="1.0"?>
        <graph string="My indicator" showPercent="1" type="indicatorField" color="red:value>0;green:value==0" totalDomain="[]" icon="slack">
            <field name="potencia" operator="+" />
        </graph>
        """
        total_values = models['polissa'].data
        t20A_values = [v for v in total_values if v['tarifa'][1] == "2.0A"]
        g = parse_graph(xml)
        result = g.process(
            t20A_values,
            fields=models['polissa'].fields,
            total_values=total_values
        )
        expect(result).to(have_keys(
            value=77.72,
            percent=28.19,
            total=275.72,
            color='red',
            icon='slack',
        ))

    with it('should do basic test with one y axis'):
        xml = """<?xml version="1.0"?>
        <graph type="pie">
          <field name="llista_preu" axis="x"/>
          <field name="llista_preu" operator="count" axis="y"/>
        </graph>
        """
        result = get_graph_data(xml, 'polissa')
        expect(result['data']).to(not_(be_empty))
        expect(result['isGroup']).to(be_false)
        expect(result['isStack']).to(be_false)

        data = result['data']

        expect(data).to(have_length(6))
        expect(data).to(contain_only(
            {
                'x': 'TARIFAS ELECTRICIDAD (EUR)',
                'value': 8,
                'type': 'Tarifa Comercialitzadora',
                'stacked': None,
                'operator': 'count'
            },
            {
                'x': 'Adeu (CHF)',
                'value': 4,
                'type': 'Tarifa Comercialitzadora',
                'stacked': None,
                'operator': 'count'
            },
            {
                'x': 'Hola bipartit (EUR)',
                'value': 5,
                'type': 'Tarifa Comercialitzadora',
                'stacked': None,
                'operator': 'count'
            },
            {
                'x': 'Mucha potencia (EUR)',
                'value': 1,
                'type': 'Tarifa Comercialitzadora',
                'stacked': None,
                'operator': 'count'
            },
            {
                'x': 'Hola (EUR)',
                'value': 13,
                'type': 'Tarifa Comercialitzadora',
                'stacked': None,
                'operator': 'count'
            },
            {
                'x': 'Not informed',
                'value': 2,
                'type': 'Tarifa Comercialitzadora',
                'stacked': None,
                'operator': 'count'
            }

        ))
    with it('should correctly process a graph with one y axis (line)'):
        xml_data = '''<?xml version="1.0"?>
        <graph type="line">
            <field name="data_alta" axis="x"/>
            <field name="data_alta" operator="count" axis="y"/>
        </graph>'''

        result = get_graph_data(xml_data, 'polissa')
        data = result['data']
        is_group = result['isGroup']
        is_stack = result['isStack']

        expect(is_group).to(be_false)
        expect(is_stack).to(be_false)

        expect(len(data)).to(equal(13))
        expect(any(entry['x'] is False for entry in data)).to(be_false)

    with it('should do basic test with one y axis with label'):
        xml_data = '''<?xml version="1.0"?>
        <graph type="bar">
            <field name="name" axis="x" />
            <field name="consum" operator="+" label="periode" axis="y"/>
        </graph>'''

        result = get_graph_data(xml_data, 'lectura')
        data = result['data']
        is_group = result['isGroup']
        is_stack = result['isStack']

        expect(is_group).to(be_true)
        expect(is_stack).to(be_false)

        expect(len(data)).to(equal(15))
        obj1 = next((d for d in data if d['x'] == "2020-09-30"), None)
        expect(obj1).to(not_(be_none))
        expect(obj1['value']).to(equal(0))
        expect(obj1['type']).to(equal("2.0A (P1)"))

        obj2 = [d for d in data if d['x'] == "2020-07-31"]
        expect(obj2).to(not_(be_none))
        expect(len(obj2)).to(equal(3))
        expect([e['type'] for e in obj2]).to(
            equal(["2.0A (P1)", "2.0DHA (P1)", "2.0DHA (P2)"]))

    with it('should do basic test with two y axis'):
        xml_data = '''<?xml version="1.0"?>
        <graph type="bar">
            <field name="name" axis="x"/>
            <field name="consum" operator="+" axis="y"/>
            <field name="ajust" operator="+" axis="y"/>
        </graph>'''

        result = get_graph_data(xml_data, 'lectura')
        data = result['data']
        is_group = result['isGroup']
        is_stack = result['isStack']

        expect(is_group).to(be_false)
        expect(is_stack).to(be_false)

        expect(len(data)).to(equal(24))

        obj1 = next((d for d in data if
                     d['x'] == "2015-10-31" and d['type'] == "Consum"), None)
        expect(obj1).to(not_(be_none))
        expect(obj1['value']).to(equal(0))

        obj2 = next((d for d in data if
                     d['x'] == "2015-10-31" and d['type'] == "Ajust"), None)
        expect(obj2).to(not_(be_none))
        expect(obj2['value']).to(equal(15))

        obj3 = next((d for d in data if
                     d['x'] == "2020-07-31" and d['type'] == "Consum"), None)
        expect(obj3).to(not_(be_none))
        expect(obj3['value']).to(equal(400))

        obj4 = next((d for d in data if
                     d['x'] == "2020-09-30" and d['type'] == "Consum"), None)
        expect(obj4).to(not_(be_none))
        expect(obj4['value']).to(equal(0))

    with it('should do basic test with 4 y axis, stacked but without labels'):
        xml_data = '''<?xml version="1.0"?>
        <graph type="bar">
            <field name="name" axis="x"/>
            <field name="consum" operator="+" axis="y" stacked="entrada" />
            <field name="ajust" operator="+" axis="y" stacked="entrada" />
            <field name="generacio" operator="+" axis="y" stacked="sortida" />
            <field name="ajust_exporta" operator="+" axis="y" stacked="sortida" />
        </graph>'''

        result = get_graph_data(xml_data, 'lectura')
        data = result['data']
        is_group = result['isGroup']
        is_stack = result['isStack']

        expect(is_group).to(be_true)
        expect(is_stack).to(be_true)

        expect(len(data)).to(equal(48))

        obj1 = next((d for d in data if d['x'] == "2015-10-31" and d[
            'type'] == "Consum - entrada"), None)
        expect(obj1).to(not_(be_none))
        expect(obj1['value']).to(equal(0))
        expect(obj1['stacked']).to(equal("entrada"))

        obj2 = next((d for d in data if
                     d['x'] == "2015-10-31" and d['type'] == "Ajust - entrada"),
                    None)
        expect(obj2).to(not_(be_none))
        expect(obj2['value']).to(equal(15))
        expect(obj2['stacked']).to(equal("entrada"))

        obj3 = next((d for d in data if d['x'] == "2015-10-31" and d[
            'type'] == u"Generació - sortida"), None)
        expect(obj3).to(not_(be_none))
        expect(obj3['value']).to(equal(0))
        expect(obj3['stacked']).to(equal("sortida"))

        obj4 = next((d for d in data if d['x'] == "2015-10-31" and d[
            'type'] == "Ajust Exporta - sortida"), None)
        expect(obj4).to(not_(be_none))
        expect(obj4['value']).to(equal(0))
        expect(obj4['stacked']).to(equal("sortida"))
    with it('should do basic test with 2 y axis, stacked and label'):
        xml_data = '''<?xml version="1.0"?>
        <graph type="bar">
            <field name="name" axis="x"/>
            <field name="consum" operator="+" label="periode" axis="y" stacked="entrada" />
            <field name="generacio" operator="+" label="periode" axis="y" stacked="sortida" />
        </graph>'''

        result = get_graph_data(xml_data, 'lectura')
        data = result['data']
        is_group = result['isGroup']
        is_stack = result['isStack']

        expect(is_group).to(be_true)
        expect(is_stack).to(be_true)

        expect(len(data)).to(equal(30))

        obj1 = next((d for d in data if
                     d['x'] == u"2015-10-31" and d['stacked'] == u"entrada"),
                    None)
        expect(obj1).to(not_(be_none))
        expect(obj1['value']).to(equal(0))
        expect(obj1['type']).to(equal(u"2.0A (P1) - entrada"))

        obj2 = next((d for d in data if d['x'] == u"2015-10-31" and d['stacked'] == u"sortida"), None)
        expect(obj2).to(not_(be_none))
        expect(obj2['value']).to(equal(0))
        expect(obj2['type']).to(equal(u"2.0A (P1) - sortida"))

    with it('should do basic test with 2 y axis, stacked, 1 label, 1 without label'):
        xml_data = '''<?xml version="1.0"?>
        <graph type="bar">
            <field name="name" axis="x"/>
            <field name="consum" operator="+" label="periode" axis="y" stacked="entrada" />
            <field name="generacio" operator="+" axis="y" stacked="sortida" />
        </graph>'''

        result = get_graph_data(xml_data, 'lectura')
        data = result['data']
        is_group = result['isGroup']
        is_stack = result['isStack']

        expect(is_group).to(be_true)
        expect(is_stack).to(be_true)

        expect(len(data)).to(equal(27))

        obj1 = next((d for d in data if
                     d['x'] == u"2015-10-31" and d['stacked'] == u"entrada"),
                    None)
        expect(obj1).to(not_(be_none))
        expect(obj1['value']).to(equal(0))
        expect(obj1['type']).to(equal(u"2.0A (P1) - entrada"))

        obj2 = next((d for d in data if
                     d['x'] == u"2015-10-31" and d['stacked'] == u"sortida"),
                    None)
        expect(obj2).to(not_(be_none))
        expect(obj2['value']).to(equal(0))
        expect(obj2['type']).to(equal(u"Generació - sortida"))

    with it('should do basic test with a timerange for days'):
        xml_data = '''<?xml version="1.0"?>
        <graph type="line" timerange="day">
            <field name="data_alta" axis="x"/>
            <field name="data_alta" operator="count" axis="y"/>
        </graph>'''

        result = get_graph_data(xml_data, 'polissa')
        data = result['data']
        is_group = result['isGroup']
        is_stack = result['isStack']

        expect(is_group).to(be_false)
        expect(is_stack).to(be_false)

        expect(data).to(not_(be_none))
        # 13 is only data with gaps
        expect(len(data)).not_to(equal(13))

        obj1 = next((d for d in data if d['x'] == u"2019-01-01"), None)
        expect(obj1).to(not_(be_none))
        expect(obj1['value']).to(equal(3))

        expect(any(entry['x'] is False for entry in data)).to(be_false)


with description('Testing get_values_grouped_by_field') as self:
    with context('when grouping values by a specific field'):
        with it('should correctly group the values'):
            fields_data = {
                'category': {'type': 'selection', 'selection': [
                    (1, 'Fruit'), (2, 'Vegetable')
                ]},
                'name': {'type': 'string'}
            }
            values_data = [
                {'category': 1, 'name': 'Apple'},
                {'category': 1, 'name': 'Banana'},
                {'category': 2, 'name': 'Carrot'},
                {'category': 2, 'name': 'Lettuce'}
            ]

            grouped_values = get_values_grouped_by_field(
                'category', fields_data, values_data
            )

            expect(grouped_values).to(equal({
                1: {'label': 'Fruit', 'entries': [
                    {'category': 1, 'name': 'Apple'},
                    {'category': 1, 'name': 'Banana'}
                ]},
                2: {'label': 'Vegetable', 'entries': [
                    {'category': 2, 'name': 'Carrot'},
                    {'category': 2, 'name': 'Lettuce'}
                ]}
            }))


with description('Testing get_all_objects_in_grouped_values') as self:
    with context('when retrieving all objects from grouped values'):
        with it('should return a single list containing all objects'):
            grouped_values = {
                1: {'label': 'Group 1', 'entries': [
                    {'id': 1, 'name': 'Item A'},
                    {'id': 2, 'name': 'Item B'}
                ]},
                2: {'label': 'Group 2', 'entries': [
                    {'id': 3, 'name': 'Item C'},
                    {'id': 4, 'name': 'Item D'}
                ]},
                3: {'label': 'Group 3', 'entries': [
                    {'id': 5, 'name': 'Item E'}
                ]}
            }

            total_objects = get_all_objects_in_grouped_values(grouped_values)

            expect(total_objects).to(equal([
                {'id': 1, 'name': 'Item A'},
                {'id': 2, 'name': 'Item B'},
                {'id': 3, 'name': 'Item C'},
                {'id': 4, 'name': 'Item D'},
                {'id': 5, 'name': 'Item E'}
            ]))


with description('Testing get_values_for_y_field') as self:
    with context('when retrieving labels for a specific field'):
        with it('should return a list of labels for the provided field'):
            fields_data = {
                'category': {'type': 'selection', 'selection': [
                    (1, 'Fruit'), (2, 'Vegetable')
                ]},
                'name': {'type': 'string'}
            }
            entries_data = [
                {'category': 1, 'name': 'Apple'},
                {'category': 2, 'name': 'Carrot'},
                {'category': 1, 'name': 'Banana'}
            ]

            labels = get_values_for_y_field(
                entries_data, 'category', fields_data
            )
            expect(labels).to(equal(['Fruit', 'Vegetable', 'Fruit']))
