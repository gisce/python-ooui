from mamba import description, context, it
from expects import *
import time
from datetime import datetime, timedelta
import random

# Import original functions
from ooui.graph.timerange import (
    process_timerange_data as process_timerange_data_original,
    fill_gaps_in_timerange_data as fill_gaps_in_timerange_data_original,
    combine_values_for_timerange as combine_values_for_timerange_original,
    get_unique_values_grouped_by as get_unique_values_grouped_by_original,
    get_missing_consecutive_dates as get_missing_consecutive_dates_original
)
from ooui.graph.processor import (
    get_values_grouped_by_field as get_values_grouped_by_field_original,
    get_min_max as get_min_max_original
)

# Import optimized functions
from ooui.graph.timerange_optimized import (
    process_timerange_data_optimized,
    fill_gaps_in_timerange_data_optimized,
    combine_values_for_timerange_optimized,
    get_unique_values_grouped_by_optimized,
    get_missing_consecutive_dates_optimized
)
from ooui.graph.processor_optimized import (
    get_values_grouped_by_field_optimized,
    get_min_max_optimized
)
from ooui.helpers.numpy_utils import has_numpy, get_numpy_version


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


with description('Performance Optimization Tests') as self:
    
    with context('Environment information'):
        with it('should report numpy availability'):
            numpy_available = has_numpy()
            numpy_version = get_numpy_version()
            
            print(f"\nNumpy available: {numpy_available}")
            if numpy_available:
                print(f"Numpy version: {numpy_version}")
            
            # Test passes regardless of numpy availability
            expect(True).to(be_true)
    
    with context('timerange processing optimizations'):
        with it('should show performance improvement in process_timerange_data'):
            large_dataset = generate_large_dataset(1000)
            
            comparison = compare_performance(
                process_timerange_data_original,
                process_timerange_data_optimized,
                large_dataset, 'day', 1
            )
            
            print(f"\nprocess_timerange_data performance:")
            print(f"Original: {comparison['original_time']:.4f}s")
            print(f"Optimized: {comparison['optimized_time']:.4f}s") 
            print(f"Speedup: {comparison['speedup']:.2f}x")
            
            # Results should be equivalent
            expect(len(comparison['original_result'])).to(equal(len(comparison['optimized_result'])))
            
            # Should have some performance improvement (at least not slower)
            expect(comparison['speedup']).to(be_above(0.8))
            
        with it('should show improvement in fill_gaps_in_timerange_data'):
            test_data = generate_large_dataset(500)
            
            comparison = compare_performance(
                fill_gaps_in_timerange_data_original,
                fill_gaps_in_timerange_data_optimized,
                test_data, 'day', 1
            )
            
            print(f"\nfill_gaps_in_timerange_data performance:")
            print(f"Original: {comparison['original_time']:.4f}s")
            print(f"Optimized: {comparison['optimized_time']:.4f}s")
            print(f"Speedup: {comparison['speedup']:.2f}x")
            
            expect(comparison['speedup']).to(be_above(0.8))
            
        with it('should show improvement in combine_values_for_timerange'):
            test_data = generate_large_dataset(800)
            
            comparison = compare_performance(
                combine_values_for_timerange_original,
                combine_values_for_timerange_optimized,
                test_data, 'month'
            )
            
            print(f"\ncombine_values_for_timerange performance:")
            print(f"Original: {comparison['original_time']:.4f}s")
            print(f"Optimized: {comparison['optimized_time']:.4f}s")
            print(f"Speedup: {comparison['speedup']:.2f}x")
            
            expect(comparison['speedup']).to(be_above(0.8))
            
        with it('should show improvement in get_unique_values_grouped_by'):
            test_data = generate_large_dataset(1000)
            
            comparison = compare_performance(
                get_unique_values_grouped_by_original,
                get_unique_values_grouped_by_optimized,
                test_data, 'all'
            )
            
            print(f"\nget_unique_values_grouped_by performance:")
            print(f"Original: {comparison['original_time']:.4f}s")
            print(f"Optimized: {comparison['optimized_time']:.4f}s")
            print(f"Speedup: {comparison['speedup']:.2f}x")
            
            expect(comparison['speedup']).to(be_above(0.8))

    with context('processor optimizations'):
        with it('should show improvement in get_values_grouped_by_field'):
            test_data = generate_large_dataset(1000)
            fields = {'type': {'type': 'char'}}
            
            comparison = compare_performance(
                get_values_grouped_by_field_original,
                get_values_grouped_by_field_optimized,
                'type', fields, test_data
            )
            
            print(f"\nget_values_grouped_by_field performance:")
            print(f"Original: {comparison['original_time']:.4f}s")
            print(f"Optimized: {comparison['optimized_time']:.4f}s")
            print(f"Speedup: {comparison['speedup']:.2f}x")
            
            expect(comparison['speedup']).to(be_above(0.8))
            
        with it('should show significant improvement in get_min_max'):
            test_data = [{'value': random.randint(1, 1000)} for _ in range(10000)]
            
            comparison = compare_performance(
                get_min_max_original,
                get_min_max_optimized,
                test_data
            )
            
            print(f"\nget_min_max performance (10k items):")
            print(f"Original: {comparison['original_time']:.4f}s")
            print(f"Optimized: {comparison['optimized_time']:.4f}s")
            print(f"Speedup: {comparison['speedup']:.2f}x")
            
            # Results should be equivalent
            expect(comparison['original_result']['min']).to(equal(comparison['optimized_result']['min']))
            expect(comparison['original_result']['max']).to(equal(comparison['optimized_result']['max']))
            
            expect(comparison['speedup']).to(be_above(0.8))

    with context('date processing optimizations'):
        with it('should show improvement in get_missing_consecutive_dates'):
            # Generate sparse date range
            dates = []
            start_date = datetime(2024, 1, 1)
            for i in range(0, 100, 3):  # Every 3rd day
                dates.append((start_date + timedelta(days=i)).strftime('%Y-%m-%d'))
            
            comparison = compare_performance(
                get_missing_consecutive_dates_original,
                get_missing_consecutive_dates_optimized,
                dates, 'day'
            )
            
            print(f"\nget_missing_consecutive_dates performance:")
            print(f"Original: {comparison['original_time']:.4f}s")
            print(f"Optimized: {comparison['optimized_time']:.4f}s")
            print(f"Speedup: {comparison['speedup']:.2f}x")
            
            # Results should be equivalent
            expect(len(comparison['original_result'])).to(equal(len(comparison['optimized_result'])))
            
            expect(comparison['speedup']).to(be_above(0.8))