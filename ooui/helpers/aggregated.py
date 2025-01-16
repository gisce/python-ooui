from __future__ import absolute_import, unicode_literals


class Aggregator:
    def __init__(self, data, field_definitions, precisions=None):
        self.data = data
        self.field_definitions = field_definitions
        self.precisions = precisions or {}

    def process(self):
        results = {}
        for field, functions in self.field_definitions.items():
            precision = self.precisions.get(field)
            values = [item[field] for item in self.data if field in item]
            results[field] = {}
            if 'sum' in functions:
                result = sum(values)
                results[field]['sum'] = precision and round(result, precision) or result
            if 'count' in functions:
                results[field]['count'] = round(len(values), precision)
            if 'avg' in functions:
                result = sum(values) / float(len(values)) if values else 0
                results[field]['avg'] = precision and round(result, precision) or result
            if 'max' in functions:
                result = max(values) if values else 0
                results[field]['max'] = precision and round(result, precision) or result
            if 'min' in functions:
                result = min(values) if values else 0
                results[field]['min'] = precision and round(result, precision) or result
        return results
