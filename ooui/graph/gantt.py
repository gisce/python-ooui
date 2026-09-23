from __future__ import absolute_import, unicode_literals

from ooui.graph.base import Graph


class GraphGantt(Graph):
    def __init__(self, graph_type, element):
        super(GraphGantt, self).__init__(element)
        self._type = graph_type

        graph_fields = element.findall('field')
        if any(not field.get('name') or not field.get('axis')
               for field in graph_fields):
            raise ValueError('A Gantt field requires name and axis attributes')

        x_fields = [field for field in graph_fields if field.get('axis') == 'x']
        y_fields = [field for field in graph_fields if field.get('axis') == 'y']
        start_fields = [field for field in y_fields
                        if field.get('role') == 'start']
        end_fields = [field for field in y_fields
                      if field.get('role') == 'end']
        if (len(x_fields) != 1 or len(y_fields) != 2
                or len(start_fields) != 1 or len(end_fields) != 1):
            raise ValueError('A Gantt chart requires one x, start and end field')

        self.x = x_fields[0].get('name')
        self.start = start_fields[0].get('name')
        self.end = end_fields[0].get('name')
        self.group = start_fields[0].get('label') or end_fields[0].get('label')
        self._fields = [self.x]
        for field in y_fields:
            for name in (field.get('name'), field.get('label')):
                if name and name not in self._fields:
                    self._fields.append(name)

    @property
    def fields(self):
        return self._fields

    def _label(self, record, fields, name, uninformed_string):
        field = fields[name]
        value = record.get(name)
        if field.get('type') == 'many2one':
            value = value[1] if value else None
        elif field.get('type') == 'selection':
            value = next((
                label for key, label in field.get('selection', [])
                if key == value and isinstance(key, bool) == isinstance(value, bool)
            ), None)
        return value or uninformed_string

    def process(self, values, fields, options=None):
        options = options or {}
        uninformed_string = options.get('uninformedString', 'Not informed')
        data = []
        for record in values:
            if self.group:
                label = self._label(record, fields, self.group,
                                    uninformed_string)
            else:
                label = fields[self.start].get('string') or self.start
            data.append({
                'id': record.get('id'),
                'x': self._label(record, fields, self.x, uninformed_string),
                'start': record.get(self.start),
                'end': record.get(self.end),
                'type': label,
                'record': record,
            })
        return {
            'type': self.type,
            'data': data,
            'num_items': len(values),
            'isGroup': bool(self.group),
            'isStack': False,
        }
