# Usage Guide

This guide covers the core concepts and basic usage patterns of Python OOUI.

## Core Concepts

Python OOUI is built around three main components:

1. **Graph Processing** - For creating and manipulating charts and indicators
2. **Tree Views** - For handling structured data displays
3. **Helper Utilities** - For data processing, conditions, and domain handling

## Graph Processing

### Graph Types

Python OOUI supports several graph types:

- **line**: Line charts for trend visualization
- **bar**: Bar charts for comparative data
- **pie**: Pie charts for proportional data
- **indicator**: Single-value indicators
- **indicatorField**: Field-based indicators

### Basic Graph Usage

```python
from ooui.graph import parse_graph

# Define a line chart
xml_definition = '''
<graph type="line" string="Sales Over Time">
    <field name="date" type="date"/>
    <field name="sales" type="float" operator="sum"/>
</graph>
'''

# Parse the graph
graph = parse_graph(xml_definition)

# Access graph properties
print(graph.string)  # "Sales Over Time"
print(graph.type)    # "line"
print(graph.fields)  # ['date', 'sales']
```

### Processing Graph Data

```python
# Sample data
data = [
    {'date': '2023-01-01', 'sales': 1000.0},
    {'date': '2023-01-02', 'sales': 1200.0},
    {'date': '2023-01-03', 'sales': 950.0},
]

# Fields definition (typically from your data model)
fields = {
    'date': {'type': 'date'},
    'sales': {'type': 'float'}
}

# Process the data
result = graph.process(data, fields)
print(result)  # Processed graph data ready for visualization
```

### Indicator Graphs

Indicators display single KPI values and support several display modes:

```python
# Simple indicator
indicator_xml = '''
<graph type="indicator" string="Total Sales">
    <field name="total_sales" type="float" operator="sum"/>
</graph>
'''
indicator = parse_graph(indicator_xml)

# Indicator with progress bar
progress_xml = '''
<graph type="indicator" string="Task Completion" progressbar="1">
    <field name="completed" type="integer" operator="sum"/>
</graph>
'''
progress_indicator = parse_graph(progress_xml)
result = progress_indicator.process(75, 100)
# result: {'value': 75, 'total': 100, 'percent': 75.0, 'progressbar': True}

# Indicator with percentage display
percent_xml = '''
<graph type="indicator" string="Success Rate" showPercent="1" suffix="%">
    <field name="success" type="integer" operator="sum"/>
</graph>
'''
percent_indicator = parse_graph(percent_xml)
result = percent_indicator.process(85, 100)
# result: {'value': 85, 'total': 100, 'percent': 85.0, 'showPercent': True, 'suffix': '%'}
```

**Indicator Attributes:**
- `progressbar`: Display as a progress bar with percentage (set to "1" or "true")
- `showPercent`: Display the percentage value as text (set to "1" or "true")
- `suffix`: Add a suffix to the value (e.g., "%", "kW", "users")
- `color`: Conditional color expression (e.g., "red:value<50;green:value>=50")
- `icon`: Conditional icon expression

## Tree Views

Tree views handle structured data displays with filtering capabilities.

### Basic Tree Usage

```python
from ooui.tree import parse_tree

# Define a tree view
tree_xml = '''
<tree string="Customer List" editable="top">
    <field name="name"/>
    <field name="email"/>
    <field name="city"/>
</tree>
'''

# Parse the tree
tree = parse_tree(tree_xml)

# Access tree properties
print(tree.string)    # "Customer List"
print(tree.editable)  # "top"
print(len(tree.fields))  # 3
```

### Tree with Conditional Formatting

```python
# Tree with colors based on conditions
tree_with_colors = '''
<tree string="Orders" colors="red:state=='cancelled';blue:state=='pending'">
    <field name="order_number"/>
    <field name="customer"/>
    <field name="state"/>
    <field name="amount"/>
</tree>
'''

tree = parse_tree(tree_with_colors)

# Get fields used in conditions
conditional_fields = tree.fields_in_conditions
print(conditional_fields)  # {'colors': ['state']}
```

## Helper Utilities

### Condition Parser

The `ConditionParser` evaluates conditional expressions:

```python
from ooui.helpers import ConditionParser

# Define conditions
condition = "red:amount < 100;yellow:amount < 500;green:amount >= 500"
parser = ConditionParser(condition)

# Check which fields are involved
print(parser.involved_fields)  # ['amount']

# Evaluate conditions with data
result = parser.eval({'amount': 150})
print(result)  # "red"

result = parser.eval({'amount': 300})
print(result)  # "yellow"

result = parser.eval({'amount': 600})
print(result)  # "green"
```

### Domain Parsing

The `Domain` class handles complex query expressions:

```python
from ooui.helpers import Domain

# Simple domain
domain = Domain("[('active', '=', True), ('age', '>', 18)]")
parsed = domain.parse()
print(parsed)

# Domain with variables
domain_with_vars = Domain("[('date', '>=', start_date), ('user_id', '=', user)]")
values = {
    'start_date': '2023-01-01',
    'user': 42
}
parsed = domain_with_vars.parse(values)
```

### Date Utilities

```python
from ooui.helpers.dates import get_date_range, DateRange

# Create date ranges
date_range = DateRange('2023-01-01', '2023-12-31')
print(date_range.start)  # datetime object
print(date_range.end)    # datetime object

# Get relative date ranges
ranges = get_date_range('this_month')
print(ranges)  # Current month start and end dates
```

### Data Aggregation

```python
from ooui.helpers.aggregated import Aggregator

# Define aggregation rules
aggregator = Aggregator({
    'sales': {'operator': 'sum', 'field': 'amount'},
    'count': {'operator': 'count', 'field': 'id'},
    'avg_age': {'operator': 'avg', 'field': 'age'}
})

# Sample data
data = [
    {'amount': 100, 'id': 1, 'age': 25, 'region': 'north'},
    {'amount': 200, 'id': 2, 'age': 30, 'region': 'north'},
    {'amount': 150, 'id': 3, 'age': 28, 'region': 'south'},
]

# Aggregate data
result = aggregator.aggregate(data, group_by='region')
print(result)
# {
#   'north': {'sales': 300, 'count': 2, 'avg_age': 27.5},
#   'south': {'sales': 150, 'count': 1, 'avg_age': 28}
# }
```

## Advanced Features

### Custom Field Processing

```python
from ooui.graph.fields import get_value_for_operator

# Apply different operators to field values
values = [10, 20, 30, 40, 50]

sum_result = get_value_for_operator(values, 'sum')      # 150
avg_result = get_value_for_operator(values, 'avg')      # 30
max_result = get_value_for_operator(values, 'max')      # 50
min_result = get_value_for_operator(values, 'min')      # 10
count_result = get_value_for_operator(values, 'count')  # 5
```

### Boolean Attribute Parsing

```python
from ooui.helpers import parse_bool_attribute

# Parse various boolean representations
print(parse_bool_attribute('1'))      # True
print(parse_bool_attribute('true'))   # True  
print(parse_bool_attribute('True'))   # True
print(parse_bool_attribute('0'))      # False
print(parse_bool_attribute('false'))  # False
```

### HTML Entity Replacement

```python
from ooui.helpers import replace_entities

# Clean HTML entities
text = "Price &gt; $100 &amp; &lt; $200"
clean_text = replace_entities(text)
print(clean_text)  # "Price > $100 & < $200"
```

## Best Practices

1. **Always validate XML**: Ensure your XML definitions are well-formed
2. **Handle missing data**: Check for None values in your data processing
3. **Use appropriate operators**: Choose the right aggregation operator for your data type
4. **Test conditions**: Verify conditional expressions with sample data
5. **Cache parsed objects**: Reuse parsed graphs and trees when possible

## Error Handling

```python
from ooui.graph import parse_graph

try:
    # Invalid graph type
    invalid_xml = '<graph type="invalid_type"></graph>'
    graph = parse_graph(invalid_xml)
except ValueError as e:
    print(f"Error: {e}")  # "invalid_type is not a valid graph"

try:
    # Malformed XML
    malformed_xml = '<graph type="line">'  # Missing closing tag
    graph = parse_graph(malformed_xml)
except Exception as e:
    print(f"XML Error: {e}")
```

## Next Steps

- Check out [Examples](examples.md) for more practical use cases
- Explore the [API Reference](api-reference.md) for detailed method documentation
- Learn about [Advanced Usage](advanced-usage.md) for complex scenarios