from mamba import description, context, it
from expects import *

from ooui.graph.timerange import (
    get_unique_values_grouped_by, get_format_for_units, check_dates_consecutive,
    get_date_format, convert_date_to_time_range_adjusted,
    adjust_x_values_for_time_range, combine_values_for_timerange,
    get_missing_consecutive_dates, fill_gaps_in_timerange_data,
    process_timerange_data
)


with description('Testing get_unique_values_grouped_by') as self:
    with context('when grouping values by "all"'):
        with it('should return unique values grouped by x, type, and stacked'):
            values_data = [
                {'x': 'Jan', 'type': 'Revenue', 'stacked': 'A'},
                {'x': 'Jan', 'type': 'Revenue', 'stacked': 'A'},
                {'x': 'Feb', 'type': 'Revenue', 'stacked': 'B'},
                {'x': 'Mar', 'type': 'Profit', 'stacked': 'A'}
            ]

            grouped_values = get_unique_values_grouped_by(values_data, 'all')
            expect(grouped_values).to(equal({
                'Jan-Revenue-A': [
                    {'x': 'Jan', 'type': 'Revenue', 'stacked': 'A'},
                    {'x': 'Jan', 'type': 'Revenue', 'stacked': 'A'}
                ],
                'Feb-Revenue-B': [
                    {'x': 'Feb', 'type': 'Revenue', 'stacked': 'B'}
                ],
                'Mar-Profit-A': [
                    {'x': 'Mar', 'type': 'Profit', 'stacked': 'A'}
                ]
            }))

    with context('when grouping values by "type-stacked"'):
        with it('should return unique values grouped by type and stacked only'):
            values_data = [
                {'x': 'Jan', 'type': 'Revenue', 'stacked': 'A'},
                {'x': 'Jan', 'type': 'Revenue', 'stacked': 'A'},
                {'x': 'Feb', 'type': 'Revenue', 'stacked': 'B'},
                {'x': 'Mar', 'type': 'Profit', 'stacked': 'A'}
            ]

            grouped_values = get_unique_values_grouped_by(values_data, 'type-stacked')
            expect(grouped_values).to(equal({
                'Revenue-A': [{'x': 'Jan', 'type': 'Revenue', 'stacked': 'A'}, {'x': 'Jan', 'type': 'Revenue', 'stacked': 'A'}],
                'Revenue-B': [{'x': 'Feb', 'type': 'Revenue', 'stacked': 'B'}],
                'Profit-A': [{'x': 'Mar', 'type': 'Profit', 'stacked': 'A'}]
            }))


with description('Testing get_format_for_units') as self:
    with context('when units is "days"'):
        with it('should return the date format "YYYY-MM-DD"'):
            result = get_format_for_units('days')
            expect(result).to(equal('%Y-%m-%d'))

    with context('when units is "weeks"'):
        with it('should return the date format "YYYY-WW"'):
            result = get_format_for_units('weeks')
            expect(result).to(equal('%Y-%W'))

    with context('when units is "months"'):
        with it('should return the date format "YYYY-MM"'):
            result = get_format_for_units('months')
            expect(result).to(equal('%Y-%m'))

    with context('when units is "years"'):
        with it('should return the date format "YYYY"'):
            result = get_format_for_units('years')
            expect(result).to(equal('%Y'))

    with context('when units is "hours" or default'):
        with it('should return the default date format "YYYY-MM-DD HH:mm"'):
            result = get_format_for_units('hours')
            expect(result).to(equal('%Y-%m-%d %H:%M'))

        with it('should return the default format for an unknown unit'):
            result = get_format_for_units('minutes')
            expect(result).to(equal('%Y-%m-%d %H:%M'))


with description('Testing check_dates_consecutive') as self:
    with context('when the dates list is empty'):
        with it('should return False'):
            result = check_dates_consecutive([], 'days')
            expect(result).to(equal(False))

    with context('when the dates list has a single date'):
        with it('should return True'):
            result = check_dates_consecutive(['2024-05-01'], 'days')
            expect(result).to(equal(True))

    with context('when the dates are consecutive by days'):
        with it('should return True'):
            result = check_dates_consecutive(['2024-05-01', '2024-05-02', '2024-05-03'], 'days')
            expect(result).to(equal(True))

    with context('when the dates are not consecutive by days'):
        with it('should return False'):
            result = check_dates_consecutive(['2024-05-01', '2024-05-03'], 'days')
            expect(result).to(equal(False))

    with context('when the dates are consecutive by months'):
        with it('should return True'):
            result = check_dates_consecutive(['2024-01', '2024-02', '2024-03'], 'months')
            expect(result).to(equal(True))

    with context('when the dates are not consecutive by months'):
        with it('should return False'):
            result = check_dates_consecutive(['2024-01', '2024-03'], 'months')
            expect(result).to(equal(False))


with description('Testing get_date_format') as self:
    with context('when the date string contains a colon'):
        with it('should return the format "YYYY-MM-DD HH:mm:ss"'):
            result = get_date_format('2024-05-01 12:34:56')
            expect(result).to(equal('%Y-%m-%d %H:%M:%S'))

    with context('when the date string does not contain a colon'):
        with it('should return the format "YYYY-MM-DD"'):
            result = get_date_format('2024-05-01')
            expect(result).to(equal('%Y-%m-%d'))


with description('Testing convert_date_to_time_range_adjusted') as self:
    with context('when the timerange is "hour"'):
        with it('should return the adjusted date with hour precision'):
            result = convert_date_to_time_range_adjusted('2024-05-01 14:35:00', 'hour')
            expect(result).to(equal('2024-05-01 14:00'))

    with context('when the timerange is "day"'):
        with it('should return the adjusted date with day precision'):
            result = convert_date_to_time_range_adjusted('2024-05-01 14:35:00', 'day')
            expect(result).to(equal('2024-05-01'))

    with context('when the timerange is "week"'):
        with it('should return the adjusted date with week precision'):
            result = convert_date_to_time_range_adjusted('2024-05-01', 'week')
            expect(result).to(equal('2024-18'))

    with context('when the timerange is "month"'):
        with it('should return the adjusted date with month precision'):
            result = convert_date_to_time_range_adjusted('2024-05-01', 'month')
            expect(result).to(equal('2024-05'))

    with context('when the timerange is "year"'):
        with it('should return the adjusted date with year precision'):
            result = convert_date_to_time_range_adjusted('2024-05-01', 'year')
            expect(result).to(equal('2024'))

    with context('when an unsupported timerange is provided'):
        with it('should raise a ValueError'):
            expect(lambda: convert_date_to_time_range_adjusted('2024-05-01', 'decade')).to(
                raise_error(ValueError, 'Unsupported timerange: decade')
            )


with description('Testing adjust_x_values_for_time_range') as self:
    with context('when adjusting "x" values to the "hour" timerange'):
        with it('should correctly adjust the "x" values to hour precision'):
            values_data = [
                {'id': 1, 'x': '2024-05-01 12:45:00', 'y': 100},
                {'id': 2, 'x': '2024-05-02 08:30:00', 'y': 200}
            ]

            result = adjust_x_values_for_time_range(
                values_data, 'hour',
            )

            expect(result).to(equal([
                {'id': 1, 'x': '2024-05-01 12:00', 'y': 100},
                {'id': 2, 'x': '2024-05-02 08:00', 'y': 200}
            ]))

    with context('when adjusting "x" values to the "day" timerange'):
        with it('should correctly adjust the "x" values to day precision'):
            values_data = [
                {'id': 1, 'x': '2024-05-01 12:45:00', 'y': 100},
                {'id': 2, 'x': '2024-05-02 08:30:00', 'y': 200}
            ]

            result = adjust_x_values_for_time_range(values_data, 'day')

            expect(result).to(equal([
                {'id': 1, 'x': '2024-05-01', 'y': 100},
                {'id': 2, 'x': '2024-05-02', 'y': 200}
            ]))


with description('Testing combine_values_for_timerange') as self:

    with context('when combining values for a specific timerange'):
        with it('should return the final combined values'):
            values_data = [
                {'x': '2024-01-01', 'type': 'Revenue', 'stacked': 'A', 'value': 100,
                 'operator': '+'},
                {'x': '2024-01-02', 'type': 'Revenue', 'stacked': 'A', 'value': 150,
                 'operator': '+'},
                {'x': '2024-02-01', 'type': 'Revenue', 'stacked': 'A', 'value': 200,
                 'operator': '+'},
                {'x': '2024-02-02', 'type': 'Revenue', 'stacked': 'A', 'value': 250,
                 'operator': '+'},
                {'x': '2024-03-01', 'type': 'Profit', 'stacked': 'A', 'value': 300,
                 'operator': '-'}
            ]

            result = combine_values_for_timerange(values_data, 'month')

            expect(result).to(contain_only(
                {'x': '2024-01', 'type': 'Revenue', 'stacked': 'A', 'value': 250,
                 'operator': '+'},
                {'x': '2024-02', 'type': 'Revenue', 'stacked': 'A', 'value': 450,
                 'operator': '+'},
                {'x': '2024-03', 'type': 'Profit', 'stacked': 'A', 'value': 300,
                 'operator': '-'})
            )


with description('Testing get_missing_consecutive_dates') as self:
    with context('when no dates are missing'):
        with it('should return an empty list'):
            dates_data = ['2024-05-01', '2024-05-02', '2024-05-03']
            result = get_missing_consecutive_dates(dates_data, 'day')
            expect(result).to(equal([]))

    with context('when some dates are missing'):
        with it('should return a list of missing dates'):
            dates_data = ['2024-05-01', '2024-05-03', '2024-05-06']
            result = get_missing_consecutive_dates(dates_data, 'day')
            expect(result).to(equal(['2024-05-02', '2024-05-04', '2024-05-05']))

    with context('when checking for missing months'):
        with it('should return a list of missing months'):
            dates_data = ['2024-01', '2024-03', '2024-05']
            result = get_missing_consecutive_dates(dates_data, 'month')
            expect(result).to(equal(['2024-02', '2024-04']))


with description('Testing fill_gaps_in_timerange_data') as self:

    with context('when filling gaps in time range data'):
        with it('should return the final values with gaps filled'):
            values_data = [
                {'x': '2024-05-01', 'type': 'Revenue', 'stacked': 'A', 'value': 100},
                {'x': '2024-05-05', 'type': 'Revenue', 'stacked': 'A', 'value': 200},
                {'x': '2024-06-01', 'type': 'Profit', 'stacked': 'B', 'value': 300}
            ]

            result = fill_gaps_in_timerange_data(values_data, 'day', 1)

            expect(result).to(contain_only(
                {'x': '2024-05-01', 'type': 'Revenue', 'stacked': 'A', 'value': 100},
                {'x': '2024-05-02', 'type': 'Revenue', 'stacked': 'A', 'value': 0},
                {'x': '2024-05-03', 'type': 'Revenue', 'stacked': 'A', 'value': 0},
                {'x': '2024-05-04', 'type': 'Revenue', 'stacked': 'A', 'value': 0},
                {'x': '2024-05-05', 'type': 'Revenue', 'stacked': 'A', 'value': 200},
                {'x': '2024-06-01', 'type': 'Profit', 'stacked': 'B', 'value': 300}
            ))


with description('Testing process_timerange_data') as self:

    with context('when processing time range data'):
        with it('should return the final combined and filled values by day'):
            values_data = [
                {'x': '2024-05-01', 'type': 'Revenue', 'stacked': 'A',
                 'value': 100, 'operator': '+'},
                {'x': '2024-05-01', 'type': 'Revenue', 'stacked': 'A',
                 'value': 200, 'operator': '+'},
                {'x': '2024-05-05', 'type': 'Revenue', 'stacked': 'A',
                 'value': 200, 'operator': '+'},
                {'x': '2024-06-01', 'type': 'Profit', 'stacked': 'B',
                 'value': 300, 'operator': '+'}
            ]

            result = process_timerange_data(
                values_data, 'day', 1,
            )

            expect(result).to(contain_only(
                {'x': '2024-05-01', 'type': 'Revenue', 'stacked': 'A', 'value': 300, 'operator': '+'},
                {'x': '2024-05-02', 'type': 'Revenue', 'stacked': 'A', 'value': 0},
                {'x': '2024-05-03', 'type': 'Revenue', 'stacked': 'A', 'value': 0},
                {'x': '2024-05-04', 'type': 'Revenue', 'stacked': 'A', 'value': 0},
                {'x': '2024-05-05', 'type': 'Revenue', 'stacked': 'A', 'value': 200, 'operator': '+'},
                {'x': '2024-06-01', 'type': 'Profit', 'stacked': 'B', 'value': 300, 'operator': '+'}
            ))

        with it('should return the final combined and filled values by month'):
            values_data = [
                {'x': '2024-01', 'type': 'Revenue', 'stacked': None,
                 'value': 100, 'operator': '+'},
                {'x': '2024-01', 'type': 'Profit', 'stacked': None,
                 'value': 50, 'operator': '+'},
                {'x': '2024-02', 'type': 'Revenue', 'stacked': None,
                 'value': 200, 'operator': '+'},
                {'x': '2024-02', 'type': 'Profit', 'stacked': None,
                 'value': 100, 'operator': '+'},
                {'x': '2024-03', 'type': 'Revenue', 'stacked': None,
                 'value': 300, 'operator': '+'},
                {'x': '2024-03', 'type': 'Profit', 'stacked': None,
                 'value': 150, 'operator': '+'},
                {'x': '2024-04', 'type': 'Profit', 'stacked': None,
                 'value': 400, 'operator': '+'},
                {'x': '2024-05', 'type': 'Profit', 'stacked': None,
                 'value': 500, 'operator': '+'},
                {'x': '2024-06', 'type': 'Profit', 'stacked': None,
                 'value': 600, 'operator': '+'},
                {'x': '2024-06', 'type': 'Revenue', 'stacked': None,
                 'value': 300, 'operator': '+'},
            ]

            result = process_timerange_data(values_data, 'month')

            expect(result).to(contain_only(
                {'stacked': None, 'operator': '+', 'x': '2024-01',
                 'type': 'Profit', 'value': 50.0},
            {'stacked': None, 'operator': '+', 'x': '2024-01',
             'type': 'Revenue', 'value': 100.0},
            {'stacked': None, 'operator': '+', 'x': '2024-02', 'type': 'Profit',
             'value': 100.0},
            {'stacked': None, 'operator': '+', 'x': '2024-02',
             'type': 'Revenue', 'value': 200.0},
            {'stacked': None, 'operator': '+', 'x': '2024-03', 'type': 'Profit',
             'value': 150.0},
            {'stacked': None, 'operator': '+', 'x': '2024-03',
             'type': 'Revenue', 'value': 300.0},
            {'stacked': None, 'operator': '+', 'x': '2024-04', 'type': 'Profit',
             'value': 400.0},
            {'x': '2024-04', 'type': 'Revenue', 'stacked': None, 'value': 0},
            {'stacked': None, 'operator': '+', 'x': '2024-05', 'type': 'Profit',
             'value': 500.0},
            {'x': '2024-05', 'type': 'Revenue', 'stacked': None, 'value': 0},
            {'stacked': None, 'operator': '+', 'x': '2024-06', 'type': 'Profit',
             'value': 600.0},
            {'stacked': None, 'operator': '+', 'x': '2024-06',
             'type': 'Revenue', 'value': 300.0},
            ))
