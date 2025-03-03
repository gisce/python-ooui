from mamba import description, context, it
from expects import expect, equal
from ooui.tree import parse_tree

with description('Tree') as self:
    with context('when initialized with an element'):
        with it('should set the string attribute'):
            xml = '<tree string="Test String"/>'
            tree = parse_tree(xml)
            expect(tree.string).to(equal('Test String'))

        with it('should set the infinite attribute'):
            xml = '<tree infinite="True"/>'
            tree = parse_tree(xml)
            expect(tree.infinite).to(equal('True'))

        with it('should set the colors attribute'):
            xml = '''<tree colors="red:state=='error'"/>'''
            tree = parse_tree(xml)
            expect(tree._colors).to(equal("red:state=='error'"))

        with it('should set the status attribute'):
            xml = '<tree status="active"/>'
            tree = parse_tree(xml)
            expect(tree._status).to(equal('active'))

        with it('should set the editable attribute'):
            xml = '<tree editable="yes"/>'
            tree = parse_tree(xml)
            expect(tree._editable).to(equal('yes'))

        with it('should return the fields'):
            xml = '<tree><field name="field1"/><field name="field2"/></tree>'
            tree = parse_tree(xml)
            fields = tree.fields
            expect(len(fields)).to(equal(2))
            expect(fields[0].get('name')).to(equal('field1'))
            expect(fields[1].get('name')).to(equal('field2'))

        with it('should return fields in conditions'):
            xml = '''<tree colors="red:state=='error';blue:state=='done';green:state=='draft';"
                            status="green:active==True"/>'''
            tree = parse_tree(xml)
            fields = tree.fields_in_conditions
            expect(fields['colors']).to(equal(['state']))
            expect(fields['status']).to(equal(['active']))
