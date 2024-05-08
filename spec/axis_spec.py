# test_get_y_axis_fieldname.py
from mamba import description, context, it
from expects import expect, equal

from ooui.graph.axis import get_y_axis_fieldname, GraphYAxis


with description('Testing get_y_axis_fieldname') as self:
    with context('when the field has a string property'):
        with it('should return the string property value'):
            fields_data = {
                'sales': {'string': 'Sales Amount'},
                'profit': {'string': 'Profit Margin'}
            }
            y_axis = GraphYAxis('sales', '+')

            field_name = get_y_axis_fieldname(y_axis, fields_data)
            expect(field_name).to(equal('Sales Amount'))

    with context('when the field does not have a string property'):
        with it('should return the original field name'):
            fields_data = {
                'inventory': {'type': 'int'},
                'losses': {'type': 'float'}
            }
            y_axis = GraphYAxis('inventory', '-')

            field_name = get_y_axis_fieldname(y_axis, fields_data)
            expect(field_name).to(equal('inventory'))
