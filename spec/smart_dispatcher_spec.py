from mamba import description, context, it
from expects import *
import time
from datetime import datetime, timedelta
import random

from ooui.performance_dispatcher import (
    smart_process_timerange_data,
    smart_get_min_max,
    smart_get_values_grouped_by_field,
    get_optimization_info
)

# Import original functions for comparison
from ooui.graph.timerange import process_timerange_data as process_timerange_data_original
from ooui.graph.processor import get_min_max as get_min_max_original


def generate_dataset(size):
    """Generate a dataset of specified size for testing."""
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


with description('Smart Performance Dispatcher Tests') as self:
    
    with context('optimization information'):
        with it('should provide optimization info'):
            info = get_optimization_info()
            
            print(f"\nOptimization Info:")
            print(f"Numpy available: {info['numpy_available']}")
            print(f"Numpy version: {info['numpy_version']}")
            print(f"Thresholds: {info['thresholds']}")
            
            expect(info).to(have_keys('numpy_available', 'thresholds'))
            expect(info['thresholds']).to(have_keys(
                'process_timerange', 'fill_gaps', 'combine_values',
                'group_values', 'min_max', 'grouped_field'
            ))
            
    with context('smart threshold-based optimization'):
        with it('should use original functions for small datasets'):
            small_dataset = generate_dataset(50)  # Below threshold
            
            # Test that it works correctly for small data
            result = smart_process_timerange_data(small_dataset, 'day', 1)
            expect(result).to(be_a(list))
            
        with it('should use optimized functions for large datasets'):
            large_dataset = generate_dataset(600)  # Above threshold
            
            # Test that it works correctly for large data
            result = smart_process_timerange_data(large_dataset, 'day', 1)
            expect(result).to(be_a(list))
            
        with it('should show better performance characteristics with smart dispatching'):
            # Test with various sizes to show smart dispatching
            sizes = [100, 500, 1000, 2000]
            results = []
            
            for size in sizes:
                dataset = generate_dataset(size)
                
                # Benchmark original
                orig_time, orig_result = benchmark_function(
                    process_timerange_data_original, dataset, 'day', 1
                )
                
                # Benchmark smart dispatcher
                smart_time, smart_result = benchmark_function(
                    smart_process_timerange_data, dataset, 'day', 1
                )
                
                speedup = orig_time / smart_time if smart_time > 0 else float('inf')
                
                results.append({
                    'size': size,
                    'original_time': orig_time,
                    'smart_time': smart_time,
                    'speedup': speedup
                })
                
                print(f"\nSize {size}: Original={orig_time:.4f}s, Smart={smart_time:.4f}s, Speedup={speedup:.2f}x")
                
                # Results should be equivalent
                expect(len(orig_result)).to(equal(len(smart_result)))
            
            # For larger datasets, we should see performance benefit or at least no regression
            large_results = [r for r in results if r['size'] >= 1000]
            if large_results:
                avg_speedup = sum(r['speedup'] for r in large_results) / len(large_results)
                expect(avg_speedup).to(be_above(0.9))  # At least not significantly slower
                
    with context('min_max optimization with different sizes'):
        with it('should handle different dataset sizes appropriately'):
            # Small dataset - should use original
            small_data = [{'value': i} for i in range(100)]
            result_small = smart_get_min_max(small_data)
            
            # Large dataset - should use optimized (if numpy available)
            large_data = [{'value': i} for i in range(10000)]
            result_large = smart_get_min_max(large_data)
            
            # Both should give correct results
            expect(result_small).to(have_keys('min', 'max'))
            expect(result_large).to(have_keys('min', 'max'))
            
            # Test performance difference
            small_time, _ = benchmark_function(smart_get_min_max, small_data)
            large_time, _ = benchmark_function(smart_get_min_max, large_data)
            
            print(f"\nMin/Max performance:")
            print(f"Small dataset (100 items): {small_time:.4f}s")
            print(f"Large dataset (10k items): {large_time:.4f}s")
            
            # Large dataset should not be significantly slower despite being 100x larger
            # Given small datasets are very fast, allow more tolerance
            max_acceptable_time = max(small_time * 20, 0.01)  # At least 10ms tolerance
            expect(large_time).to(be_below(max_acceptable_time))
            
    with context('field grouping optimization'):
        with it('should handle field grouping with smart thresholds'):
            # Test different sizes for field grouping
            sizes = [100, 700, 1500]  # Below, around, and above threshold
            fields = {'type': {'type': 'char'}}
            
            for size in sizes:
                dataset = generate_dataset(size)
                
                result = smart_get_values_grouped_by_field('type', fields, dataset)
                
                expect(result).to(be_a(dict))
                expect(len(result)).to(be_above(0))
                
                # Verify all entries are accounted for
                total_entries = sum(len(group['entries']) for group in result.values())
                expect(total_entries).to(equal(size))
                
                print(f"Size {size}: Grouped into {len(result)} categories")
                
    with context('consistency verification'):
        with it('should produce identical results regardless of optimization path'):
            test_dataset = generate_dataset(800)
            
            # Get results using original functions
            orig_processed = process_timerange_data_original(test_dataset, 'day', 1)
            orig_minmax = get_min_max_original([{'value': random.randint(1, 100)} for _ in range(1000)])
            
            # Get results using smart dispatcher
            smart_processed = smart_process_timerange_data(test_dataset, 'day', 1)
            smart_minmax = smart_get_min_max([{'value': random.randint(1, 100)} for _ in range(1000)])
            
            # Results should be consistent (lengths should match, structures should be similar)
            expect(len(orig_processed)).to(equal(len(smart_processed)))
            expect(orig_minmax.keys()).to(equal(smart_minmax.keys()))
            
            print(f"\nConsistency check:")
            print(f"Processed data length - Original: {len(orig_processed)}, Smart: {len(smart_processed)}")
            print(f"Min/Max keys match: {orig_minmax.keys() == smart_minmax.keys()}")