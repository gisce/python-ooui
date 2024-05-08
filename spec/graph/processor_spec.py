from mamba import description, context, it
from expects import expect, equal, raise_error

from ooui.graph.processor import (
    get_values_grouped_by_field, get_all_objects_in_grouped_values,
    get_values_for_y_field
)


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
