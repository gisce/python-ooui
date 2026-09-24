# API Reference

Complete API documentation for Python OOUI.

## Module Structure

```
ooui/
├── graph/           # Graph processing components
│   ├── __init__.py  # parse_graph()
│   ├── base.py      # Graph base class
│   ├── chart.py     # GraphChart class
│   ├── indicator.py # GraphIndicator classes
│   ├── axis.py      # Axis processing
│   ├── fields.py    # Field operations
│   ├── processor.py # Data processing utilities
│   └── timerange.py # Time range handling
├── tree/            # Tree view components  
│   ├── __init__.py  # parse_tree()
│   └── base.py      # Tree class
└── helpers/         # Utility modules
    ├── __init__.py  # Common utilities
    ├── conditions.py # ConditionParser
    ├── domain.py    # Domain class
    ├── aggregated.py # Aggregator class
    ├── dates.py     # Date utilities
    └── features.py  # Feature detection
```

## Graph Module (`ooui.graph`)

### parse_graph(xml)

Parse a graph definition from XML string.

**Parameters:**
- `xml` (str): XML string containing graph definition

**Returns:** 
- Graph object (GraphChart, GraphIndicator, or GraphIndicatorField)

**Raises:**
- `ValueError`: If graph type is invalid or unsupported

**Example:**
```python
from ooui.graph import parse_graph

xml = '''
<graph type="line" string="Sales Chart">
    <field name="date" type="date"/>
    <field name="amount" type="float" operator="sum"/>
</graph>
'''
graph = parse_graph(xml)
```

### Graph Base Class

Base class for all graph types.

#### Properties

- `string`: Graph title/label
- `type`: Graph type (line, bar, pie, indicator, indicatorField)
- `fields`: List of field names used in the graph

#### Methods

##### process(values, fields, options=None)

Process data for the graph.

**Parameters:**
- `values` (list): List of data dictionaries
- `fields` (dict): Field definitions
- `options` (dict, optional): Processing options

**Returns:** 
- Processed data structure ready for visualization

### GraphChart Class

Chart-type graphs (line, bar, pie).

#### Properties

- `x`: X-axis configuration
- `y`: Y-axis configuration (list of axis objects)

#### Methods

Same as Graph base class plus chart-specific processing.

**Example:**
```python
# Sample data processing
data = [
    {'date': '2023-01-01', 'sales': 1000},
    {'date': '2023-01-02', 'sales': 1200}
]
fields = {
    'date': {'type': 'date'},
    'sales': {'type': 'float'}
}
result = chart.process(data, fields)
```

### GraphIndicator Class

Single-value indicator graphs.

#### Properties

- `field`: Main field configuration
- `compare_field`: Optional comparison field
- `progressbar`: Whether to display as a progress bar (boolean)
- `show_percent`: Whether to display the percentage value (boolean)
- `suffix`: Optional suffix to append to the value (e.g., '%', 'kW')
- `color`: Conditional color expression
- `icon`: Conditional icon expression
- `total_domain`: Domain for calculating the total value

#### Methods

##### process(value, total=0)

Process indicator data and return formatted result.

**Parameters:**
- `value`: The indicator value
- `total` (optional): The total value for percentage calculation

**Returns:**
- Dictionary containing:
  - `value`: The indicator value
  - `total`: The total value (if provided)
  - `type`: Graph type ('indicator')
  - `percent`: Calculated percentage (if progressbar or show_percent is True)
  - `progressbar`: True if progressbar attribute is set
  - `showPercent`: True if showPercent attribute is set
  - `suffix`: Value suffix (if set)
  - `color`: Evaluated color (if color condition is set)
  - `icon`: Evaluated icon (if icon condition is set)

**Example:**
```python
# Basic indicator
xml = '''
<graph type="indicator" string="Total Sales">
    <field name="total" type="float" operator="sum"/>
</graph>
'''
indicator = parse_graph(xml)

# Indicator with progress bar
xml = '''
<graph type="indicator" string="Completion" progressbar="1">
    <field name="completed" type="integer" operator="sum"/>
</graph>
'''
indicator = parse_graph(xml)
result = indicator.process(75, 100)
# result: {'value': 75, 'total': 100, 'type': 'indicator', 'percent': 75.0, 'progressbar': True}

# Indicator with percentage display
xml = '''
<graph type="indicator" string="Success Rate" showPercent="1" suffix="%">
    <field name="success" type="integer" operator="sum"/>
</graph>
'''
indicator = parse_graph(xml)
result = indicator.process(85, 100)
# result: {'value': 85, 'total': 100, 'type': 'indicator', 'percent': 85.0, 'suffix': '%', 'showPercent': True}
```

### GraphIndicatorField Class

Field-based indicators with multiple values.

Similar to GraphIndicator but handles multiple field indicators.

## Tree Module (`ooui.tree`)

### parse_tree(xml)

Parse a tree view definition from XML.

**Parameters:**
- `xml` (str): XML string containing tree definition

**Returns:**
- Tree object

**Example:**
```python
from ooui.tree import parse_tree

xml = '''
<tree string="Customer List" editable="top">
    <field name="name"/>
    <field name="email"/>
</tree>
'''
tree = parse_tree(xml)
```

### Tree Class

Represents a tree view configuration.

#### Properties

- `string`: Tree title/label
- `infinite`: Whether tree supports infinite scrolling
- `colors`: Color condition string
- `status`: Status condition string
- `editable`: Edit mode (top, bottom, etc.)
- `fields`: List of field elements
- `fields_in_conditions`: Dict of fields used in color/status conditions

#### Methods

Tree objects are primarily data containers. Field processing is handled by the parsing system.

**Example:**
```python
# Access tree properties
print(tree.string)           # "Customer List"
print(tree.editable)         # "top"
print(len(tree.fields))      # 2

# Check conditional fields
if tree.colors:
    conditional = tree.fields_in_conditions
    print(conditional.get('colors', []))  # Fields used in color conditions
```

## Helpers Module (`ooui.helpers`)

### Utility Functions

#### parse_bool_attribute(attribute)

Parse boolean values from string representations.

**Parameters:**
- `attribute`: Value to parse (string, int, or bool)

**Returns:**
- `True` for "1", "true" (case-insensitive)
- `False` otherwise

**Example:**
```python
from ooui.helpers import parse_bool_attribute

print(parse_bool_attribute('1'))     # True
print(parse_bool_attribute('True'))  # True
print(parse_bool_attribute('0'))     # False
```

#### replace_entities(text)

Replace HTML entities with Unicode characters.

**Parameters:**
- `text` (str): Text containing HTML entities

**Returns:**
- Cleaned text string

**Example:**
```python
from ooui.helpers import replace_entities

text = "Price &gt; $100 &amp; &lt; $200"
clean = replace_entities(text)
print(clean)  # "Price > $100 & < $200"
```

### ConditionParser Class (`ooui.helpers.conditions`)

Parse and evaluate conditional expressions.

#### Constructor

```python
ConditionParser(condition)
```

**Parameters:**
- `condition` (str): Condition string in format "result1:condition1;result2:condition2"

#### Properties

- `involved_fields`: Set of field names used in conditions
- `raw_condition`: Original condition string

#### Methods

##### eval(values)

Evaluate conditions against provided values.

**Parameters:**
- `values` (dict): Field values to evaluate against

**Returns:**
- Result value if condition matches, None otherwise

**Example:**
```python
from ooui.helpers import ConditionParser

parser = ConditionParser("red:amount < 100;green:amount >= 100")
print(parser.involved_fields)  # {'amount'}

result = parser.eval({'amount': 50})
print(result)  # "red"

result = parser.eval({'amount': 150})  
print(result)  # "green"
```

### Domain Class (`ooui.helpers.domain`)

Parse and evaluate domain expressions (query filters).

#### Constructor

```python
Domain(domain)
```

**Parameters:**
- `domain` (str): Domain expression string

#### Methods

##### parse(values=None)

Parse domain with optional variable substitution.

**Parameters:**
- `values` (dict, optional): Variable values for substitution

**Returns:**
- Parsed domain structure

**Example:**
```python
from ooui.helpers import Domain

# Simple domain
domain = Domain("[('active', '=', True)]")
result = domain.parse()

# Domain with variables
domain = Domain("[('user_id', '=', user)]")
result = domain.parse({'user': 42})
```

### Aggregator Class (`ooui.helpers.aggregated`)

Aggregate data with various operations.

#### Constructor

```python
Aggregator(rules)
```

**Parameters:**
- `rules` (dict): Aggregation rules mapping

#### Methods

##### aggregate(data, group_by=None)

Aggregate data according to rules.

**Parameters:**
- `data` (list): List of data dictionaries
- `group_by` (str, optional): Field name to group by

**Returns:**
- Aggregated data structure

**Example:**
```python
from ooui.helpers.aggregated import Aggregator

aggregator = Aggregator({
    'total': {'operator': 'sum', 'field': 'amount'},
    'count': {'operator': 'count', 'field': 'id'}
})

data = [
    {'amount': 100, 'id': 1, 'category': 'A'},
    {'amount': 200, 'id': 2, 'category': 'A'},
    {'amount': 150, 'id': 3, 'category': 'B'}
]

result = aggregator.aggregate(data, group_by='category')
# Result: {'A': {'total': 300, 'count': 2}, 'B': {'total': 150, 'count': 1}}
```

## Field Processing (`ooui.graph.fields`)

### get_value_for_operator(values, operator)

Apply aggregation operator to list of values.

**Parameters:**
- `values` (list): Numeric values
- `operator` (str): Operation ('sum', 'avg', 'max', 'min', 'count')

**Returns:**
- Aggregated result

**Example:**
```python
from ooui.graph.fields import get_value_for_operator

values = [10, 20, 30, 40, 50]
print(get_value_for_operator(values, 'sum'))    # 150
print(get_value_for_operator(values, 'avg'))    # 30
print(get_value_for_operator(values, 'max'))    # 50
print(get_value_for_operator(values, 'count'))  # 5
```

## Date Processing (`ooui.helpers.dates`)

### DateRange Class

Represents a date range with start and end dates.

#### Constructor

```python
DateRange(start, end)
```

**Parameters:**
- `start`: Start date (string or datetime)
- `end`: End date (string or datetime)

#### Properties

- `start`: Start datetime object
- `end`: End datetime object

### get_date_range(period)

Get predefined date ranges.

**Parameters:**
- `period` (str): Period identifier ('today', 'this_week', 'this_month', etc.)

**Returns:**
- DateRange object

**Example:**
```python
from ooui.helpers.dates import get_date_range, DateRange

# Predefined ranges
this_month = get_date_range('this_month')
print(this_month.start)
print(this_month.end)

# Custom range
custom = DateRange('2023-01-01', '2023-12-31')
```

## Error Handling

### Common Exceptions

- `ValueError`: Invalid graph types, malformed conditions
- `AttributeError`: Missing required attributes
- `KeyError`: Missing field references
- `XMLSyntaxError`: Malformed XML (from lxml)

### Error Handling Example

```python
try:
    graph = parse_graph(xml_string)
    result = graph.process(data, fields)
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Processing error: {e}")
```

## Type Annotations

Python OOUI supports both Python 2 and 3, so type annotations are not used in the source code. However, for modern development, expected types are:

```python
# Function signatures (for reference)
def parse_graph(xml: str) -> Graph
def parse_tree(xml: str) -> Tree
def parse_bool_attribute(attribute: Union[str, int, bool]) -> bool
def replace_entities(text: str) -> str

class ConditionParser:
    def __init__(self, condition: str) -> None
    def eval(self, values: Dict[str, Any]) -> Optional[str]
    
class Domain:
    def __init__(self, domain: str) -> None
    def parse(self, values: Optional[Dict[str, Any]] = None) -> Any
```