from mamba import *
from expects import *
from ooui.graph import parse_graph


with description('Gantt graph'):
    with it('preserves every Gantt interval and labels selection zero separately from false'):
        xml = ('<graph type="gantt">'
               '<field name="name" axis="x"/>'
               '<field name="start" axis="y" role="start" label="group"/>'
               '<field name="end" axis="y" role="end"/>'
               '</graph>')
        graph = parse_graph(xml)
        expect(graph.fields).to(equal(['name', 'start', 'group', 'end']))
        fields = {
            'name': {'type': 'char'},
            'start': {'type': 'datetime', 'string': 'Start'},
            'end': {'type': 'datetime'},
            'group': {'type': 'selection', 'selection': [(0, 'Zero'), (1, 'One')]},
        }
        values = [
            {'id': 1, 'name': 'Task', 'start': '2026-09-22 08:00:00',
             'end': '2026-09-22 10:00:00', 'group': 0},
            {'id': 2, 'name': 'Task', 'start': '2026-09-22 11:00:00',
             'end': '2026-09-22 12:00:00', 'group': False},
        ]
        result = graph.process(values, fields, {'uninformedString': 'Sense informar'})
        expect(result['type']).to(equal('gantt'))
        expect(result['num_items']).to(equal(2))
        expect(result['isGroup']).to(be_true)
        expect(result['isStack']).to(be_false)
        expect([item['type'] for item in result['data']]).to(equal(['Zero', 'Sense informar']))
        expect([item['id'] for item in result['data']]).to(equal([1, 2]))
        expect([item['record'] for item in result['data']]).to(equal(values))

    with it('uses relational group labels and leaves repeated task names separate'):
        xml = ('<graph type="gantt">'
               '<field name="name" axis="x"/>'
               '<field name="start" axis="y" role="start"/>'
               '<field name="end" axis="y" role="end" label="project"/>'
               '</graph>')
        graph = parse_graph(xml)
        expect(graph.fields).to(equal(['name', 'start', 'end', 'project']))
        fields = {
            'name': {'type': 'char'},
            'start': {'type': 'date', 'string': 'Start'},
            'end': {'type': 'date'},
            'project': {'type': 'many2one'},
        }
        values = [
            {'id': 1, 'name': 'Task', 'start': '2026-09-22',
             'end': '2026-09-23', 'project': [5, 'North']},
            {'id': 2, 'name': 'Task', 'start': '2026-09-24',
             'end': '2026-09-25', 'project': [6, 'South']},
        ]
        result = graph.process(values, fields)
        expect([item['type'] for item in result['data']]).to(equal(['North', 'South']))
        expect([item['id'] for item in result['data']]).to(equal([1, 2]))

    with it('keeps ungrouped and empty Gantt results valid'):
        xml = ('<graph type="gantt">'
               '<field name="name" axis="x"/>'
               '<field name="start" axis="y" role="start"/>'
               '<field name="end" axis="y" role="end"/>'
               '</graph>')
        graph = parse_graph(xml)
        fields = {'name': {'type': 'char'},
                  'start': {'type': 'date', 'string': 'Start'},
                  'end': {'type': 'date'}}
        expect(graph.process([], fields)['data']).to(equal([]))
        result = graph.process([{'id': 1, 'name': 'Task'}], fields)
        expect(result['isGroup']).to(be_false)
        expect(result['data'][0]['type']).to(equal('Start'))

    with it('rejects Gantt without one start and one end'):
        xml = ('<graph type="gantt"><field name="name" axis="x"/>'
               '<field name="start" axis="y" role="start"/>'
               '<field name="end" axis="y" role="start"/></graph>')
        expect(lambda: parse_graph(xml)).to(raise_error(ValueError))
