from mamba import *
from expects import *
from ooui.helpers import Aggregator


with description('Aggregator class'):
    with context('processing aggregate functions'):
        with it('calculates sum, avg, max, and min correctly'):
            data = [{'value': 10}, {'value': 20}, {'value': 30}]
            field_definitions = {'value': ['sum', 'avg', 'max', 'min']}
            aggregator = Aggregator(data, field_definitions)
            results = aggregator.process()

            expect(results['value']['sum']).to(equal(60))
            expect(results['value']['avg']).to(equal(20))
            expect(results['value']['max']).to(equal(30))
            expect(results['value']['min']).to(equal(10))

        with it('handles fields with missing data'):
            data = [{'value': 10}, {'value': 20}, {}]
            field_definitions = {'value': ['sum', 'avg', 'max', 'min']}
            aggregator = Aggregator(data, field_definitions)
            results = aggregator.process()

            expect(results['value']['sum']).to(equal(30))
            expect(results['value']['avg']).to(equal(15))
            expect(results['value']['max']).to(equal(20))
            expect(results['value']['min']).to(equal(10))
