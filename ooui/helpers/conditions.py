import time
import ast
import operator
from datetime import datetime
from simpleeval import EvalWithCompoundTypes, DEFAULT_OPERATORS, DEFAULT_NAMES


class GetFieldsDict(dict):

    def __init__(self, *args, **kwargs):
        super(GetFieldsDict, self).__init__(*args, **kwargs)
        self.fields = set()

    def __getitem__(self, key):
        if key not in self:
            self.fields.add(key)
        return dict.get(self, key, key)


class ConditionParser(object):
    def __init__(self, condition):
        self.raw_condition = condition
        self.conditions = self.parse_condition(condition)
        self.functions = {'time': time, 'bool': bool}
        self.operators = DEFAULT_OPERATORS.copy()
        self.operators[ast.BitAnd] = operator.and_
        self.values = {'current_date': datetime.now().strftime('%Y-%m-%d')}

    @property
    def involved_fields(self):
        magic_dict = GetFieldsDict()
        magic_dict.update(self.values)
        magic_dict.update(DEFAULT_NAMES)
        for key, condition in self.conditions:
            s = EvalWithCompoundTypes(
                names=magic_dict, functions=self.functions, operators=self.operators
            )
            s.eval(condition)
        return magic_dict.fields

    def eval(self, values):
        if not self.conditions:
            return self.raw_condition
        names = self.values.copy()
        names.update(values)
        names.update(DEFAULT_NAMES)
        for key, condition in self.conditions:
            s = EvalWithCompoundTypes(
                names=names, functions=self.functions, operators=self.operators
            )
            if s.eval(condition):
                return key

    def __str__(self):
        return self.raw_condition

    @staticmethod
    def parse_condition(condition):
        conditions = []
        if ':' not in condition:
            return []
        for sentence in condition.strip().split(';'):
            if sentence:
                key, condition = [x.strip() for x in sentence.split(':')]
                conditions.append((key, condition))
        return conditions
