# Python OOUI

Python OOUI (Open Object User Interface) is a Python port of ooui.js, providing powerful tools for data visualization and processing.

## Features

- **Graph Processing**: Create line charts, bar charts, pie charts, and indicators
- **Tree Views**: Handle structured data with advanced filtering and conditional formatting  
- **Data Helpers**: Utilities for domain parsing, condition evaluation, and data aggregation
- **XML Parsing**: Parse XML-based graph and tree definitions
- **Cross-Platform**: Compatible with Python 2.7+ and Python 3.x

## Quick Start

### Installation

```bash
pip install ooui
```

### Basic Usage

```python
from ooui.graph import parse_graph
from ooui.tree import parse_tree

# Create a line chart
graph_xml = '''
<graph type="line" string="Sales Trend">
    <field name="date" type="date"/>
    <field name="amount" type="float" operator="sum"/>
</graph>
'''
graph = parse_graph(graph_xml)

# Create a tree view
tree_xml = '''
<tree string="Customer List" editable="top">
    <field name="name"/>
    <field name="email"/>
    <field name="status"/>
</tree>
'''
tree = parse_tree(tree_xml)
```

## Documentation

📚 **[Complete Documentation](docs/index.md)** - Start here for comprehensive guides and examples

### Quick Links

- **[Installation Guide](docs/installation.md)** - Detailed setup instructions
- **[Usage Guide](docs/usage.md)** - Core concepts and basic usage
- **[API Reference](docs/api-reference.md)** - Complete API documentation  
- **[Examples](docs/examples.md)** - Practical code examples
- **[Advanced Usage](docs/advanced-usage.md)** - Complex scenarios and advanced features

## Key Components

### Graph Processing
```python
from ooui.graph import parse_graph

# Support for multiple chart types
graph = parse_graph(xml_definition)
result = graph.process(data, fields)
```

### Tree Views
```python
from ooui.tree import parse_tree

# Structured data with conditional formatting
tree = parse_tree(xml_definition)
conditional_fields = tree.fields_in_conditions
```

### Condition Evaluation
```python
from ooui.helpers import ConditionParser

parser = ConditionParser("red:amount < 100;green:amount >= 100")
result = parser.eval({'amount': 150})  # Returns "green"
```

### Domain Parsing
```python
from ooui.helpers import Domain

domain = Domain("[('active', '=', True), ('age', '>', 18)]")
parsed = domain.parse({'user_id': 42})
```

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/gisce/python-ooui.git
cd python-ooui

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Run all tests
mamba

# Tests use mamba (BDD testing framework)
# See spec/ directory for test specifications
```

### Project Structure

```
ooui/
├── graph/           # Graph processing (charts, indicators)  
├── tree/            # Tree view processing
└── helpers/         # Utilities (conditions, domain, dates, etc.)
```

## Contributing

Contributions are welcome! Please:

1. Check the [documentation](docs/) to understand the project
2. Review existing [examples](docs/examples.md) and [API reference](docs/api-reference.md)
3. Follow the existing code style and patterns
4. Add tests for new functionality
5. Update documentation as needed

## License

MIT License - see LICENSE file for details.

## About

Developed by [GISCE](https://gisce.net) for the GISCE-ERP project.

For more information, visit the [complete documentation](docs/index.md).
