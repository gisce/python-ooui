from mamba import description, context, it
from expects import *
import time
from datetime import datetime, timedelta
import random

from ooui.graph.timerange import (
    process_timerange_data, fill_gaps_in_timerange_data,
    combine_values_for_timerange, get_unique_values_grouped_by,
    get_missing_consecutive_dates
)
from ooui.graph.processor import get_values_grouped_by_field, get_min_max
from ooui.graph.chart import GraphChart
from ooui.graph.fields import get_value_and_label_for_field


def generate_large_dataset(size=1000):
    """Generate a large dataset for performance testing."""
    data = []
    start_date = datetime(2024, 1, 1)
    
    types = ['Revenue', 'Profit', 'Cost', 'Sales']
    stacked_vals = ['A', 'B', 'C', None]
    operators = ['+', '-', '*', 'avg', 'min', 'max', 'count']
    
    for i in range(size):
        date = start_date + timedelta(days=i % 365)
        data.append({
            'x': date.strftime('%Y-%m-%d'),
            'type': random.choice(types),
            'stacked': random.choice(stacked_vals),
            'value': random.randint(10, 1000),
            'operator': random.choice(operators)
        })
    return data


def benchmark_function(func, *args, **kwargs):
    """Benchmark a function and return execution time."""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return end_time - start_time, result


with description('Performance Benchmarks') as self:
    
    with context('timerange processing performance'):
        with it('should benchmark process_timerange_data with large dataset'):
            large_dataset = generate_large_dataset(1000)
            
            execution_time, result = benchmark_function(
                process_timerange_data, large_dataset, 'day', 1
            )
            
            print(f"\nprocess_timerange_data (1000 items): {execution_time:.4f} seconds")
            expect(execution_time).to(be_below(5.0))  # Should complete in under 5 seconds
            expect(result).to(be_a(list))
            expect(len(result)).to(be_above(0))

        with it('should benchmark fill_gaps_in_timerange_data'):
            test_data = generate_large_dataset(500)
            
            execution_time, result = benchmark_function(
                fill_gaps_in_timerange_data, test_data, 'day', 1
            )
            
            print(f"\nfill_gaps_in_timerange_data (500 items): {execution_time:.4f} seconds")
            expect(execution_time).to(be_below(3.0))
            expect(result).to(be_a(list))
            
        with it('should benchmark combine_values_for_timerange'):
            test_data = generate_large_dataset(800)
            
            execution_time, result = benchmark_function(
                combine_values_for_timerange, test_data, 'month'
            )
            
            print(f"\ncombine_values_for_timerange (800 items): {execution_time:.4f} seconds")
            expect(execution_time).to(be_below(2.0))
            expect(result).to(be_a(list))

        with it('should benchmark get_unique_values_grouped_by'):
            test_data = generate_large_dataset(1000)
            
            execution_time, result = benchmark_function(
                get_unique_values_grouped_by, test_data, 'all'
            )
            
            print(f"\nget_unique_values_grouped_by (1000 items): {execution_time:.4f} seconds")
            expect(execution_time).to(be_below(1.0))
            expect(result).to(be_a(dict))

    with context('processor performance'):
        with it('should benchmark get_values_grouped_by_field'):
            test_data = generate_large_dataset(1000)
            fields = {'type': {'type': 'char'}}
            
            execution_time, result = benchmark_function(
                get_values_grouped_by_field, 'type', fields, test_data
            )
            
            print(f"\nget_values_grouped_by_field (1000 items): {execution_time:.4f} seconds")
            expect(execution_time).to(be_below(2.0))
            expect(result).to(be_a(dict))

        with it('should benchmark get_min_max'):
            test_data = [{'value': random.randint(1, 1000)} for _ in range(10000)]
            
            execution_time, result = benchmark_function(
                get_min_max, test_data
            )
            
            print(f"\nget_min_max (10000 items): {execution_time:.4f} seconds")
            expect(execution_time).to(be_below(0.1))
            expect(result).to(have_keys('min', 'max'))

    with context('date processing performance'):
        with it('should benchmark get_missing_consecutive_dates'):
            # Generate sparse date range
            dates = []
            start_date = datetime(2024, 1, 1)
            for i in range(0, 100, 3):  # Every 3rd day
                dates.append((start_date + timedelta(days=i)).strftime('%Y-%m-%d'))
            
            execution_time, result = benchmark_function(
                get_missing_consecutive_dates, dates, 'day'
            )
            
            print(f"\nget_missing_consecutive_dates (sparse 100 days): {execution_time:.4f} seconds")
            expect(execution_time).to(be_below(1.0))
            expect(result).to(be_a(list))


# Utility function for testing optimized vs unoptimized versions
def compare_performance(original_func, optimized_func, *args, **kwargs):
    """Compare performance between original and optimized functions."""
    original_time, original_result = benchmark_function(original_func, *args, **kwargs)
    optimized_time, optimized_result = benchmark_function(optimized_func, *args, **kwargs)
    
    speedup = original_time / optimized_time if optimized_time > 0 else float('inf')
    
    return {
        'original_time': original_time,
        'optimized_time': optimized_time,
        'speedup': speedup,
        'original_result': original_result,
        'optimized_result': optimized_result
    }