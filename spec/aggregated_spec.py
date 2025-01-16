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

    with context('Using precision in aggregation'):

        with it('should use the precision for the field'):
            data = [{'value': 10.1235}, {'value': 20.1233}, {'value': 30.1238}]
            field_definitions = {'value': ['sum']}
            precisions = {'value': 3}
            aggregator = Aggregator(data, field_definitions, precisions)
            results = aggregator.process()

            expect(results['value']['sum']).to(equal(60.371))


        with it('not should round if is an integer'):
            data = [{'value': 10}, {'value': 20}, {'value': 30}]
            field_definitions = {'value': ['sum']}
            aggregator = Aggregator(data, field_definitions)
            results = aggregator.process()

            expect(str(results['value']['sum'])).to(equal(str(60)))
