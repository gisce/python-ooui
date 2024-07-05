from __future__ import absolute_import, unicode_literals


class Aggregator:
    def __init__(self, data, field_definitions):
        self.data = data
        self.field_definitions = field_definitions

    def process(self):
        results = {}
        for field, functions in self.field_definitions.items():
            values = [item[field] for item in self.data if field in item]
            results[field] = {}
            if 'sum' in functions:
                results[field]['sum'] = sum(values)
            if 'count' in functions:
                results[field]['count'] = len(values)
            if 'avg' in functions:
                results[field]['avg'] = sum(values) / float(len(values)) if values else 0
            if 'max' in functions:
                results[field]['max'] = max(values)
            if 'min' in functions:
                results[field]['min'] = min(values)
        return results