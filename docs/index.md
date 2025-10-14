# Python OOUI Documentation

Welcome to the Python OOUI documentation! This package is a Python port of ooui.js, providing Object-Oriented User Interface components for data visualization and processing.

## What is Python OOUI?

Python OOUI (Open Object User Interface) is a Python library that provides tools for:

- **Graph Processing**: Create and manipulate various types of charts (line, bar, pie, indicators)
- **Tree Views**: Parse and process tree-structured data with advanced filtering
- **Data Helpers**: Utilities for domain parsing, condition evaluation, date handling, and data aggregation
- **Field Processing**: Handle complex field definitions and relationships

## Key Features

- **Graph Types**: Support for line charts, bar charts, pie charts, and indicator displays
- **XML Parsing**: Parse XML-based graph and tree definitions
- **Condition Evaluation**: Advanced condition parsing and evaluation system
- **Data Aggregation**: Built-in aggregation functions for data analysis
- **Domain Handling**: Powerful domain parsing with support for complex expressions
- **Date Utilities**: Comprehensive date and time range processing

## Quick Start

### Installation

```bash
pip install ooui
```

### Basic Usage

```python
from ooui.graph import parse_graph
from ooui.tree import parse_tree

# Parse a graph from XML
xml_graph = '''
<graph type="line">
    <field name="date" type="date"/>
    <field name="value" type="float" operator="sum"/>
</graph>
'''
graph = parse_graph(xml_graph)

# Parse a tree view
xml_tree = '''
<tree string="My Tree">
    <field name="name"/>
    <field name="value"/>
</tree>
'''
tree = parse_tree(xml_tree)
```

## Documentation Structure

- **[Installation](installation.md)** - Detailed installation and setup instructions
- **[Usage Guide](usage.md)** - Core concepts and basic usage patterns
- **[API Reference](api-reference.md)** - Complete API documentation
- **[Examples](examples.md)** - Practical code examples and use cases
- **[Advanced Usage](advanced-usage.md)** - Complex scenarios and advanced features

## Getting Help

If you encounter issues or have questions:

1. Check the [Usage Guide](usage.md) for common patterns
2. Browse the [Examples](examples.md) for practical code samples
3. Consult the [API Reference](api-reference.md) for detailed method documentation
4. Review the source code on [GitHub](https://github.com/gisce/python-ooui)

## Contributing

Python OOUI is developed by GISCE. Contributions are welcome! Please visit the [GitHub repository](https://github.com/gisce/python-ooui) for more information.