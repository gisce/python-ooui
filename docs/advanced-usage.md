# Advanced Usage

This guide covers advanced features and complex usage scenarios of Python OOUI.

## Advanced Graph Processing

### Custom Graph Types and Extensions

While Python OOUI comes with built-in graph types, you can understand and work with the underlying system:

```python
from ooui.graph import GRAPH_TYPES, parse_graph
from ooui.graph.base import Graph

# Check available graph types
print("Available graph types:", list(GRAPH_TYPES.keys()))

# Understand the graph type mapping
for graph_type, graph_class in GRAPH_TYPES.items():
    print(f"{graph_type} -> {graph_class.__name__}")
```

### Complex Multi-Axis Charts

```python
# Advanced chart with multiple Y-axes and grouping
complex_chart_xml = '''
<graph type="line" string="Sales Performance Analysis">
    <field name="date" type="date"/>
    <field name="revenue" type="float" operator="sum" group="financial"/>
    <field name="profit_margin" type="float" operator="avg" group="financial"/>
    <field name="customer_count" type="integer" operator="count" group="metrics"/>
    <field name="sales_rep" type="char" group="dimensions"/>
</graph>
'''

chart = parse_graph(complex_chart_xml)

# Advanced data with multiple dimensions
complex_data = [
    {
        'date': '2023-01-01', 'revenue': 10000, 'profit_margin': 0.15, 
        'customer_count': 50, 'sales_rep': 'Alice', 'region': 'North'
    },
    {
        'date': '2023-01-01', 'revenue': 8000, 'profit_margin': 0.18, 
        'customer_count': 35, 'sales_rep': 'Bob', 'region': 'South'
    },
    # ... more data
]

# Process with advanced options
options = {
    'group_by_date': True,
    'aggregate_function': 'sum',
    'time_granularity': 'month'
}

result = chart.process(complex_data, {
    'date': {'type': 'date'},
    'revenue': {'type': 'float'},
    'profit_margin': {'type': 'float'},
    'customer_count': {'type': 'integer'},
    'sales_rep': {'type': 'char'}
}, options)
```

### Dynamic Graph Configuration

```python
class DynamicGraphBuilder:
    """Build graphs dynamically based on configuration."""
    
    def __init__(self):
        self.graph_templates = {
            'time_series': '''
                <graph type="line" string="{title}">
                    <field name="{time_field}" type="date"/>
                    <field name="{value_field}" type="float" operator="{operator}"/>
                </graph>
            ''',
            'comparison': '''
                <graph type="bar" string="{title}">
                    <field name="{category_field}" type="char"/>
                    <field name="{value_field}" type="float" operator="{operator}"/>
                </graph>
            ''',
            'distribution': '''
                <graph type="pie" string="{title}">
                    <field name="{category_field}" type="char"/>
                    <field name="{value_field}" type="float" operator="{operator}"/>
                </graph>
            '''
        }
    
    def build_graph(self, graph_type, config):
        """Build a graph from configuration."""
        if graph_type not in self.graph_templates:
            raise ValueError(f"Unknown graph type: {graph_type}")
        
        template = self.graph_templates[graph_type]
        xml = template.format(**config)
        
        return parse_graph(xml)
    
    def build_dashboard(self, dashboard_config):
        """Build multiple graphs for a dashboard."""
        graphs = {}
        
        for graph_name, graph_spec in dashboard_config.items():
            graph_type = graph_spec.pop('type')
            graphs[graph_name] = self.build_graph(graph_type, graph_spec)
        
        return graphs

# Usage
builder = DynamicGraphBuilder()

dashboard_config = {
    'sales_trend': {
        'type': 'time_series',
        'title': 'Sales Trend',
        'time_field': 'date',
        'value_field': 'amount',
        'operator': 'sum'
    },
    'product_comparison': {
        'type': 'comparison',
        'title': 'Product Performance',
        'category_field': 'product',
        'value_field': 'revenue',
        'operator': 'sum'
    },
    'regional_distribution': {
        'type': 'distribution',
        'title': 'Regional Sales Distribution',
        'category_field': 'region',
        'value_field': 'sales',
        'operator': 'sum'
    }
}

dashboard_graphs = builder.build_dashboard(dashboard_config)
```

## Advanced Tree Processing

### Dynamic Tree Configuration with Complex Conditions

```python
class AdvancedTreeProcessor:
    """Advanced tree processing with dynamic conditions."""
    
    def __init__(self):
        self.condition_builders = {
            'status_colors': self._build_status_colors,
            'priority_colors': self._build_priority_colors,
            'threshold_colors': self._build_threshold_colors,
            'multi_condition': self._build_multi_condition
        }
    
    def _build_status_colors(self, config):
        """Build status-based color conditions."""
        status_map = config.get('status_map', {})
        conditions = []
        
        for status, color in status_map.items():
            conditions.append(f"{color}:status=='{status}'")
        
        return ';'.join(conditions)
    
    def _build_priority_colors(self, config):
        """Build priority-based color conditions."""
        priority_colors = config.get('priority_colors', {})
        conditions = []
        
        for priority, color in priority_colors.items():
            conditions.append(f"{color}:priority=='{priority}'")
        
        return ';'.join(conditions)
    
    def _build_threshold_colors(self, config):
        """Build threshold-based color conditions."""
        field = config.get('field')
        thresholds = config.get('thresholds', [])
        
        conditions = []
        for threshold in thresholds:
            operator = threshold.get('operator', '>=')
            value = threshold['value']
            color = threshold['color']
            conditions.append(f"{color}:{field} {operator} {value}")
        
        return ';'.join(conditions)
    
    def _build_multi_condition(self, config):
        """Build complex multi-field conditions."""
        rules = config.get('rules', [])
        conditions = []
        
        for rule in rules:
            result = rule['result']
            condition_parts = []
            
            for condition in rule['conditions']:
                field = condition['field']
                operator = condition['operator']
                value = condition['value']
                
                if isinstance(value, str):
                    condition_parts.append(f"{field} {operator} '{value}'")
                else:
                    condition_parts.append(f"{field} {operator} {value}")
            
            logical_op = rule.get('logical_operator', 'and')
            full_condition = f" {logical_op} ".join(condition_parts)
            conditions.append(f"{result}:{full_condition}")
        
        return ';'.join(conditions)
    
    def build_tree(self, fields, condition_config=None):
        """Build a tree with dynamic conditions."""
        field_elements = []
        for field in fields:
            if isinstance(field, str):
                field_elements.append(f'<field name="{field}"/>')
            else:
                field_elements.append(f'<field name="{field["name"]}" {field.get("attrs", "")}"/>')
        
        fields_xml = '\n    '.join(field_elements)
        
        tree_attrs = ['string="Dynamic Tree"']
        
        if condition_config:
            for condition_type, config in condition_config.items():
                if condition_type in self.condition_builders:
                    condition_string = self.condition_builders[condition_type](config)
                    tree_attrs.append(f'{condition_type}="{condition_string}"')
        
        attrs_str = ' '.join(tree_attrs)
        
        xml = f'''
        <tree {attrs_str}>
            {fields_xml}
        </tree>
        '''
        
        return parse_tree(xml)

# Usage
processor = AdvancedTreeProcessor()

# Complex condition configuration
condition_config = {
    'colors': {
        'rules': [
            {
                'result': 'red',
                'conditions': [
                    {'field': 'status', 'operator': '==', 'value': 'overdue'},
                    {'field': 'amount', 'operator': '>', 'value': 1000}
                ],
                'logical_operator': 'and'
            },
            {
                'result': 'orange', 
                'conditions': [
                    {'field': 'priority', 'operator': '==', 'value': 'high'},
                    {'field': 'days_remaining', 'operator': '<=', 'value': 3}
                ],
                'logical_operator': 'and'
            }
        ]
    }
}

fields = [
    'name',
    'status', 
    'priority',
    'amount',
    'days_remaining'
]

advanced_tree = processor.build_tree(fields, {'colors': condition_config['colors']})
```

## Advanced Condition Processing

### Custom Condition Evaluators

```python
from ooui.helpers.conditions import ConditionParser
import re
from datetime import datetime, timedelta

class AdvancedConditionParser(ConditionParser):
    """Extended condition parser with custom functions."""
    
    def __init__(self, condition):
        super().__init__(condition)
        
        # Add custom functions
        self.functions.update({
            'days_ago': self._days_ago,
            'in_range': self._in_range,
            'matches': self._matches_regex,
            'calculate_age': self._calculate_age,
        })
    
    def _days_ago(self, days):
        """Calculate date N days ago."""
        return (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    def _in_range(self, value, min_val, max_val):
        """Check if value is in range."""
        return min_val <= value <= max_val
    
    def _matches_regex(self, text, pattern):
        """Check if text matches regex pattern."""
        return bool(re.match(pattern, str(text)))
    
    def _calculate_age(self, birth_date):
        """Calculate age from birth date."""
        if isinstance(birth_date, str):
            birth = datetime.strptime(birth_date, '%Y-%m-%d')
        else:
            birth = birth_date
        
        today = datetime.now()
        return (today - birth).days // 365

# Usage
advanced_conditions = """
urgent:days_remaining <= 1 and priority == 'high';
warning:in_range(score, 60, 79) and department == 'sales';
elderly:calculate_age(birth_date) >= 65;
valid_email:matches(email, r'^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$');
recent:created_date >= days_ago(30)
"""

parser = AdvancedConditionParser(advanced_conditions)

# Test data
test_data = {
    'days_remaining': 0,
    'priority': 'high',
    'score': 75,
    'department': 'sales',
    'birth_date': '1950-01-01',
    'email': 'user@example.com',
    'created_date': '2023-10-01'
}

result = parser.eval(test_data)
print(f"Condition result: {result}")
```

### Condition Caching and Performance

```python
from functools import lru_cache
from ooui.helpers.conditions import ConditionParser

class CachedConditionParser:
    """Condition parser with caching for better performance."""
    
    def __init__(self, max_cache_size=1000):
        self.max_cache_size = max_cache_size
        self._parsers = {}
    
    @lru_cache(maxsize=1000)
    def _get_parser(self, condition_string):
        """Get cached parser for condition string."""
        return ConditionParser(condition_string)
    
    def eval_condition(self, condition_string, values):
        """Evaluate condition with caching."""
        parser = self._get_parser(condition_string)
        return parser.eval(values)
    
    def bulk_evaluate(self, condition_string, value_list):
        """Evaluate condition against multiple value sets."""
        parser = self._get_parser(condition_string)
        results = []
        
        for values in value_list:
            result = parser.eval(values)
            results.append(result)
        
        return results
    
    def clear_cache(self):
        """Clear the condition parser cache."""
        self._get_parser.cache_clear()

# Usage for high-performance scenarios
cached_parser = CachedConditionParser()

# Evaluate same condition against many records
condition = "red:amount < 1000;orange:amount < 5000;green:amount >= 5000"
records = [
    {'amount': 500},
    {'amount': 2500}, 
    {'amount': 7500},
    # ... thousands more records
]

results = cached_parser.bulk_evaluate(condition, records)
print(f"Processed {len(results)} records")
```

## Advanced Domain Processing

### Complex Domain Builder

```python
from ooui.helpers.domain import Domain
import json

class DomainBuilder:
    """Build complex domains programmatically."""
    
    def __init__(self):
        self.operators = {
            'eq': '=',
            'ne': '!=', 
            'gt': '>',
            'gte': '>=',
            'lt': '<',
            'lte': '<=',
            'like': 'like',
            'ilike': 'ilike',
            'in': 'in',
            'not_in': 'not in'
        }
    
    def build_filter(self, field, operator, value):
        """Build a single filter clause."""
        op = self.operators.get(operator, operator)
        return (field, op, value)
    
    def build_and_domain(self, filters):
        """Build AND domain from filter list."""
        domain = []
        for filter_spec in filters:
            if isinstance(filter_spec, dict):
                filter_clause = self.build_filter(
                    filter_spec['field'],
                    filter_spec['operator'], 
                    filter_spec['value']
                )
            else:
                filter_clause = filter_spec
            domain.append(filter_clause)
        return domain
    
    def build_or_domain(self, filter_groups):
        """Build OR domain from filter groups."""
        domain = []
        
        for i, group in enumerate(filter_groups):
            if i > 0:
                domain.append('|')
            
            if isinstance(group, list):
                domain.extend(self.build_and_domain(group))
            else:
                domain.append(group)
        
        return domain
    
    def build_complex_domain(self, domain_spec):
        """Build complex nested domain."""
        if domain_spec['type'] == 'and':
            return self.build_and_domain(domain_spec['filters'])
        elif domain_spec['type'] == 'or':
            return self.build_or_domain(domain_spec['groups'])
        else:
            raise ValueError(f"Unknown domain type: {domain_spec['type']}")

# Usage
builder = DomainBuilder()

# Complex search criteria
search_criteria = {
    'type': 'and',
    'filters': [
        {'field': 'active', 'operator': 'eq', 'value': True},
        {'field': 'created_date', 'operator': 'gte', 'value': '2023-01-01'},
        {
            'type': 'or',
            'groups': [
                [
                    {'field': 'type', 'operator': 'eq', 'value': 'premium'},
                    {'field': 'amount', 'operator': 'gte', 'value': 1000}
                ],
                [
                    {'field': 'priority', 'operator': 'eq', 'value': 'high'}
                ]
            ]
        }
    ]
}

complex_domain = builder.build_complex_domain(search_criteria)
domain_obj = Domain(str(complex_domain))
parsed = domain_obj.parse()
print("Complex domain:", json.dumps(parsed, indent=2))
```

### Dynamic Domain Evaluation

```python
class DynamicDomainEvaluator:
    """Evaluate domains against data sets."""
    
    def __init__(self):
        self.type_converters = {
            'date': self._convert_date,
            'datetime': self._convert_datetime,
            'int': int,
            'float': float,
            'bool': bool,
            'str': str
        }
    
    def _convert_date(self, value):
        """Convert string to date."""
        if isinstance(value, str):
            return datetime.strptime(value, '%Y-%m-%d').date()
        return value
    
    def _convert_datetime(self, value):
        """Convert string to datetime.""" 
        if isinstance(value, str):
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return value
    
    def evaluate_record(self, record, domain_filters, field_types=None):
        """Check if record matches domain filters."""
        if field_types is None:
            field_types = {}
        
        for domain_filter in domain_filters:
            if isinstance(domain_filter, str):
                continue  # Skip logical operators
            
            field, operator, expected = domain_filter
            
            if field not in record:
                return False
            
            actual = record[field]
            
            # Type conversion if needed
            if field in field_types:
                field_type = field_types[field]
                if field_type in self.type_converters:
                    converter = self.type_converters[field_type]
                    try:
                        actual = converter(actual)
                        if not isinstance(expected, type(actual)):
                            expected = converter(expected)
                    except (ValueError, TypeError):
                        return False
            
            # Evaluate condition
            if not self._evaluate_condition(actual, operator, expected):
                return False
        
        return True
    
    def _evaluate_condition(self, actual, operator, expected):
        """Evaluate single condition."""
        try:
            if operator == '=':
                return actual == expected
            elif operator == '!=':
                return actual != expected
            elif operator == '>':
                return actual > expected
            elif operator == '>=':
                return actual >= expected
            elif operator == '<':
                return actual < expected
            elif operator == '<=':
                return actual <= expected
            elif operator == 'like':
                return str(expected).lower() in str(actual).lower()
            elif operator == 'ilike':
                return str(expected).lower() in str(actual).lower()
            elif operator == 'in':
                return actual in expected
            elif operator == 'not in':
                return actual not in expected
            else:
                return False
        except (TypeError, ValueError):
            return False
    
    def filter_dataset(self, dataset, domain_string, field_types=None):
        """Filter entire dataset using domain."""
        domain = Domain(domain_string)
        domain_filters = domain.parse()
        
        filtered = []
        for record in dataset:
            if self.evaluate_record(record, domain_filters, field_types):
                filtered.append(record)
        
        return filtered

# Usage
evaluator = DynamicDomainEvaluator()

# Sample dataset
dataset = [
    {'id': 1, 'name': 'Alice', 'age': 30, 'active': True, 'created': '2023-01-15'},
    {'id': 2, 'name': 'Bob', 'age': 25, 'active': False, 'created': '2023-02-20'}, 
    {'id': 3, 'name': 'Charlie', 'age': 35, 'active': True, 'created': '2023-03-10'},
]

# Complex filter
domain_string = "[('active', '=', True), ('age', '>', 28), ('created', '>=', '2023-02-01')]"
field_types = {
    'age': 'int',
    'active': 'bool',
    'created': 'date'
}

filtered_data = evaluator.filter_dataset(dataset, domain_string, field_types)
print("Filtered data:", filtered_data)
```

## Performance Optimization

### Batch Processing

```python
class BatchProcessor:
    """Process large datasets in batches."""
    
    def __init__(self, batch_size=1000):
        self.batch_size = batch_size
    
    def process_graphs_in_batches(self, graph, dataset, fields):
        """Process graph data in batches for memory efficiency."""
        results = []
        
        for i in range(0, len(dataset), self.batch_size):
            batch = dataset[i:i + self.batch_size]
            batch_result = graph.process(batch, fields)
            results.append(batch_result)
        
        # Combine results
        return self._combine_graph_results(results)
    
    def _combine_graph_results(self, results):
        """Combine batch results into single result."""
        if not results:
            return None
        
        # Implementation depends on graph type and result structure
        combined = results[0]
        
        for result in results[1:]:
            # Merge logic here - depends on specific result format
            pass
        
        return combined
    
    def process_conditions_in_batches(self, condition_parser, dataset):
        """Evaluate conditions in batches."""
        results = []
        
        for i in range(0, len(dataset), self.batch_size):
            batch = dataset[i:i + self.batch_size]
            batch_results = []
            
            for record in batch:
                result = condition_parser.eval(record)
                batch_results.append(result)
            
            results.extend(batch_results)
        
        return results

# Memory-efficient processing
processor = BatchProcessor(batch_size=500)

# Large dataset processing
large_dataset = [{'value': i, 'category': f'cat_{i%10}'} for i in range(10000)]

# Process in batches to manage memory
batch_results = processor.process_conditions_in_batches(
    ConditionParser("high:value > 5000;low:value <= 5000"),
    large_dataset
)
```

### Caching Strategies

```python
import pickle
import hashlib
from functools import wraps

class ResultCache:
    """Cache processing results for better performance."""
    
    def __init__(self, cache_dir=None):
        self.cache_dir = cache_dir or '/tmp/ooui_cache'
        self.memory_cache = {}
        self.max_memory_items = 100
    
    def _generate_key(self, *args, **kwargs):
        """Generate cache key from arguments."""
        content = str(args) + str(sorted(kwargs.items()))
        return hashlib.md5(content.encode()).hexdigest()
    
    def cache_result(self, key, result):
        """Cache result in memory."""
        if len(self.memory_cache) >= self.max_memory_items:
            # Remove oldest item
            oldest_key = next(iter(self.memory_cache))
            del self.memory_cache[oldest_key]
        
        self.memory_cache[key] = result
    
    def get_cached_result(self, key):
        """Get cached result."""
        return self.memory_cache.get(key)
    
    def cached_process(self, func):
        """Decorator for caching function results."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = self._generate_key(*args, **kwargs)
            
            # Check memory cache
            result = self.get_cached_result(key)
            if result is not None:
                return result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            self.cache_result(key, result)
            
            return result
        
        return wrapper

# Usage
cache = ResultCache()

@cache.cached_process
def expensive_graph_processing(graph, data, fields):
    """Expensive processing that benefits from caching."""
    return graph.process(data, fields)

# Subsequent calls with same parameters will use cache
result1 = expensive_graph_processing(my_graph, my_data, my_fields)
result2 = expensive_graph_processing(my_graph, my_data, my_fields)  # From cache
```

## Integration Patterns

### Plugin Architecture

```python
class OOUIPlugin:
    """Base class for OOUI plugins."""
    
    def __init__(self, name):
        self.name = name
    
    def process_graph_data(self, graph, data, fields):
        """Override to add custom graph processing."""
        return graph.process(data, fields)
    
    def process_tree_data(self, tree, data):
        """Override to add custom tree processing."""
        return data
    
    def enhance_conditions(self, condition_string):
        """Override to add custom condition enhancements."""
        return condition_string

class ExportPlugin(OOUIPlugin):
    """Plugin for data export functionality."""
    
    def __init__(self):
        super().__init__('export')
        self.formats = ['csv', 'json', 'xlsx']
    
    def export_graph_data(self, graph_data, format='json'):
        """Export graph data to various formats."""
        if format == 'json':
            return json.dumps(graph_data, indent=2)
        elif format == 'csv':
            return self._to_csv(graph_data)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _to_csv(self, data):
        """Convert data to CSV format."""
        # Implementation depends on data structure
        return "CSV data here"

class ValidationPlugin(OOUIPlugin):
    """Plugin for data validation."""
    
    def __init__(self):
        super().__init__('validation')
        self.rules = {}
    
    def add_validation_rule(self, field, rule):
        """Add validation rule for field."""
        self.rules[field] = rule
    
    def validate_data(self, data):
        """Validate data against rules."""
        errors = []
        
        for record in data:
            for field, rule in self.rules.items():
                if field in record:
                    if not rule(record[field]):
                        errors.append(f"Validation failed for {field}: {record[field]}")
        
        return errors

class PluginManager:
    """Manager for OOUI plugins."""
    
    def __init__(self):
        self.plugins = {}
    
    def register_plugin(self, plugin):
        """Register a plugin."""
        self.plugins[plugin.name] = plugin
    
    def get_plugin(self, name):
        """Get plugin by name."""
        return self.plugins.get(name)
    
    def process_with_plugins(self, operation, *args, **kwargs):
        """Process operation through relevant plugins."""
        results = {}
        
        for name, plugin in self.plugins.items():
            if hasattr(plugin, operation):
                method = getattr(plugin, operation)
                results[name] = method(*args, **kwargs)
        
        return results

# Usage
manager = PluginManager()
manager.register_plugin(ExportPlugin())
manager.register_plugin(ValidationPlugin())

# Use plugins
export_plugin = manager.get_plugin('export')
validation_plugin = manager.get_plugin('validation')

# Add validation rules
validation_plugin.add_validation_rule('age', lambda x: 0 <= x <= 150)
validation_plugin.add_validation_rule('email', lambda x: '@' in x)
```

This advanced usage guide demonstrates sophisticated patterns and techniques for working with Python OOUI in complex scenarios, including performance optimization, extensibility, and integration patterns.