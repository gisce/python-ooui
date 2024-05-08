from mamba import *
from expects import *
from ooui.graph.fields import (
    get_fields_to_retrieve, get_value_and_label_for_field,
    get_value_for_operator, round_number
)
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


with description('Testing get_value_for_operator') as self:
    with context('when operator is "count"'):
        with it('should return the count of values'):
            values = [1, 2, 3, 4, 5]
            result = get_value_for_operator('count', values)
            expect(result).to(equal(5))

    with context('when operator is "+"'):
        with it('should return the sum of values'):
            values = [1, 2, 3, 4, 5]
            result = get_value_for_operator('+', values)
            expect(result).to(equal(15))

    with context('when operator is "-"'):
        with it('should return the difference when subtracting sequentially'):
            values = [10, 3, 2]
            result = get_value_for_operator('-', values)
            expect(result).to(equal(5))

    with context('when operator is "*"'):
        with it('should return the product of all values'):
            values = [2, 3, 4]
            result = get_value_for_operator('*', values)
            expect(result).to(equal(24))

    with context('when operator is "avg"'):
        with it('should return the average of values'):
            values = [10, 20, 30, 40]
            result = get_value_for_operator('avg', values)
            expect(result).to(equal(25.0))

        with it('should return 0 if no values are provided'):
            values = []
            result = get_value_for_operator('avg', values)
            expect(result).to(equal(0))

    with context('when operator is "min"'):
        with it('should return the minimum value'):
            values = [10, 3, 45, 7]
            result = get_value_for_operator('min', values)
            expect(result).to(equal(3))

    with context('when operator is "max"'):
        with it('should return the maximum value'):
            values = [10, 3, 45, 7]
            result = get_value_for_operator('max', values)
            expect(result).to(equal(45))

    with context('when an unsupported operator is provided'):
        with it('should raise a ValueError'):
            values = [10, 20, 30]
            expect(lambda: get_value_for_operator('unsupported', values)).to(
                raise_error(ValueError, 'Unsupported operator: unsupported')
            )


with description('Testing round_number function') as self:
    with context('when rounding positive numbers'):
        with it('should round up to two decimal places'):
            result = round_number(1.23456)
            expect(result).to(equal(1.23))

        with it('should round down to two decimal places'):
            result = round_number(1.22999)
            expect(result).to(equal(1.23))

    with context('when rounding negative numbers'):
        with it('should round up to two decimal places'):
            result = round_number(-1.23456)
            expect(result).to(equal(-1.23))

        with it('should round down to two decimal places'):
            result = round_number(-1.22999)
            expect(result).to(equal(-1.23))

    with context('when rounding integers'):
        with it('should keep integers as they are'):
            result = round_number(5)
            expect(result).to(equal(5.0))

    with context('when rounding zero'):
        with it('should return zero'):
            result = round_number(0)
            expect(result).to(equal(0.0))
