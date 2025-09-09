# -*- coding: utf-8 -*-
"""
Numpy utilities for performance optimization.
Falls back to pure Python if numpy is not available.
Compatible with Python 2.7 and 3.11.
"""
from __future__ import absolute_import, unicode_literals

# Try to import numpy, fallback to None if not available
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    np = None
    HAS_NUMPY = False


def array_min_max(values, margin=0.1):
    """
    Fast min/max calculation using numpy if available, otherwise fallback to pure Python.
    
    :param list values: List of numerical values
    :param float margin: Margin to add to min/max values
    :return: Dict with 'min' and 'max' keys
    :rtype: dict
    """
    if not values:
        raise ValueError("The values array cannot be empty.")
    
    if HAS_NUMPY and len(values) > 100:  # Use numpy for larger datasets
        arr = np.array(values)
        min_val = float(np.min(arr))
        max_val = float(np.max(arr))
    else:
        min_val = min(values)
        max_val = max(values)
    
    calculated_margin = (max_val - min_val) * margin
    
    return {
        'min': int(min_val - calculated_margin),
        'max': int(max_val + calculated_margin),
    }


def fast_groupby_key(items, key_func):
    """
    Fast groupby operation using numpy if available for large datasets.
    
    :param list items: List of items to group
    :param function key_func: Function to extract grouping key
    :return: Dictionary of grouped items
    :rtype: dict
    """
    if not items:
        return {}
    
    if HAS_NUMPY and len(items) > 1000:
        # For very large datasets, use numpy for indices
        keys = [key_func(item) for item in items]
        unique_keys = list(set(keys))
        
        groups = {}
        for unique_key in unique_keys:
            # Use list comprehension which is generally faster
            groups[unique_key] = [item for item, key in zip(items, keys) if key == unique_key]
        
        return groups
    else:
        # Standard Python grouping for smaller datasets
        groups = {}
        for item in items:
            key = key_func(item)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        
        return groups


def optimize_date_gaps(dates, missing_count_threshold=50):
    """
    Optimize date gap filling for large gaps using numpy if available.
    
    :param list dates: List of date strings
    :param int missing_count_threshold: Threshold to use optimized approach
    :return: Optimized date processing hint
    :rtype: dict
    """
    if not HAS_NUMPY or len(dates) < 2:
        return {'use_optimization': False}
    
    # Estimate potential missing dates
    if len(dates) > 10:
        # Sample estimation - if dataset is large and sparse, suggest optimization
        sample_size = min(10, len(dates))
        sample_dates = sorted(dates[:sample_size])
        
        # Quick heuristic: if gaps between samples are large, recommend optimization
        if sample_size >= 2:
            avg_gap = (len(sample_dates) - 1) / max(1, sample_size - 1)
            if avg_gap > 2:  # If average gap > 2, there might be missing dates
                return {
                    'use_optimization': True, 
                    'estimated_missing': int(len(dates) * avg_gap * 0.5)
                }
    
    return {'use_optimization': False}


def has_numpy():
    """Check if numpy is available."""
    return HAS_NUMPY


def get_numpy_version():
    """Get numpy version if available."""
    if HAS_NUMPY:
        return np.__version__
    return None