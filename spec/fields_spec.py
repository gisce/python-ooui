from mamba import *
from expects import *
from ooui.graph.fields import get_fields_to_retrieve, get_value_and_label_for_field
from ooui.graph import parse_graph

with description('Graph fields utils'):
    with describe('Testing get_fields_to_retrieve'):
        with it('should get all the fields to retrieve from a view'):
            xml = """<?xml version="1.0"?>
            <graph type="line">
              <field name="data_alta" axis="x"/>
              <field name="consum" operator="+" axis="y"/>
            </graph>
            """
            g = parse_graph(xml)
            fields = get_fields_to_retrieve(g)
            expect(fields).to(equal(['data_alta', 'consum']))

    with description('Testing get_value_and_label_for_field') as self:
        with context('when field type is many2one'):
            with it('should return the value and label if value is present'):
                fields_data = {'field1': {'type': 'many2one'}}
                values_data = {'field1': [1, 'Label1']}

                result = get_value_and_label_for_field(fields_data, values_data, 'field1')
                expect(result).to(equal({'value': 1, 'label': 'Label1'}))

            with it('should return false and None if value is missing'):
                fields_data = {'field1': {'type': 'many2one'}}
                values_data = {'field1': None}

                result = get_value_and_label_for_field(fields_data, values_data, 'field1')
                expect(result).to(equal({'value': False, 'label': None}))

        with context('when field type is selection'):
            with it('should return the value and label pair if value exists in selection'):
                fields_data = {
                    'field2': {'type': 'selection', 'selection': [(1, 'Option 1'), (2, 'Option 2')]}
                }
                values_data = {'field2': 2}

                result = get_value_and_label_for_field(fields_data, values_data, 'field2')
                expect(result).to(equal({'value': 2, 'label': 'Option 2'}))

            with it('should return false and None if value is not found in selection'):
                fields_data = {
                    'field2': {'type': 'selection', 'selection': [(1, 'Option 1'), (2, 'Option 2')]}
                }
                values_data = {'field2': 3}  # Valor no existent a la selecció

                result = get_value_and_label_for_field(fields_data, values_data, 'field2')
                expect(result).to(equal({'value': False, 'label': None}))

        with context('when field is not found'):
            with it('should raise a ValueError'):
                fields_data = {'field1': {'type': 'many2one'}}
                values_data = {'field1': [1, 'Label1']}

                expect(lambda: get_value_and_label_for_field(fields_data, values_data, 'unknown_field')).to(
                    raise_error(ValueError, 'Field unknown_field not found')
                )

