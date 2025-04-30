import six
import ast
import operator
import time
import datetime
import dateutil
from simpleeval import EvalWithCompoundTypes, DEFAULT_OPERATORS, DEFAULT_NAMES


EVAL_FUNCTIONS = {
    'time': time,
    'bool': bool,
    'datetime': datetime,
    'eval': ast.literal_eval,
    'dateutil': dateutil,
}


class DotDict(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError("object has no attribute '{}'".format(name))


def make_dotdict(obj):
    if isinstance(obj, dict):
        return DotDict({k: make_dotdict(v) for k, v in obj.items()})
    return obj


class Domain(object):
    def __init__(self, domain):
        if not isinstance(domain, six.string_types):
            domain = six.text_type(domain)
        self.domain = domain

    def parse(self, values=None):
        if values is None:
            values = {}
        # Hack to allow JSON domains
        values.update({'true': True, 'false': False, 'null': None})

        operators = DEFAULT_OPERATORS.copy()
        operators[ast.BitAnd] = operator.and_
        values = make_dotdict(values)
        values.update(DEFAULT_NAMES.copy())
        s = EvalWithCompoundTypes(
            names=values, functions=EVAL_FUNCTIONS, operators=operators
        )
        return s.eval(self.domain)

    def __str__(self):
        return self.domain

    def __bool__(self):
        return bool(self.domain)

    def __nonzero__(self):
        return self.__bool__()
