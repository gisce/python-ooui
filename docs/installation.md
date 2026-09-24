# Installation Guide

This guide covers the installation and setup of Python OOUI.

## Requirements

Python OOUI requires:

- Python 2.7 or Python 3.x
- lxml
- python-dateutil
- six
- simpleeval < 0.9.12

## Installation Methods

### Using pip (Recommended)

Install the latest stable version from PyPI:

```bash
pip install ooui
```

### Development Installation

For development or to get the latest features:

```bash
# Clone the repository
git clone https://github.com/gisce/python-ooui.git
cd python-ooui

# Install in development mode
pip install -e .

# Install development dependencies for testing
pip install -r requirements-dev.txt
```

## Verifying Installation

To verify your installation is working correctly:

```python
import ooui
from ooui.graph import parse_graph
from ooui.tree import parse_tree
from ooui.helpers import ConditionParser, Domain

# Test basic imports
print("Python OOUI installed successfully!")
```

## Dependencies Explained

### Core Dependencies

- **lxml**: Used for XML parsing and manipulation of graph and tree definitions
- **python-dateutil**: Provides enhanced date/time parsing and manipulation
- **six**: Ensures Python 2/3 compatibility
- **simpleeval**: Safe evaluation of Python expressions in conditions and domains

### Development Dependencies

- **mamba**: Testing framework for behavior-driven development
- **expects**: Assertion library for testing

## Troubleshooting

### Common Installation Issues

#### lxml Installation Problems

If you encounter issues installing lxml:

**On Ubuntu/Debian:**
```bash
sudo apt-get install libxml2-dev libxslt-dev python-dev
pip install lxml
```

**On CentOS/RHEL:**
```bash
sudo yum install libxml2-devel libxslt-devel python-devel
pip install lxml
```

**On macOS:**
```bash
# Using Homebrew
brew install libxml2 libxslt
pip install lxml

# Or using conda
conda install lxml
```

#### Permission Issues

If you encounter permission errors:

```bash
# Install for current user only
pip install --user ooui

# Or use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install ooui
```

### Virtual Environment Setup (Recommended)

Using a virtual environment is the recommended approach:

```bash
# Create virtual environment
python -m venv ooui-env

# Activate it
source ooui-env/bin/activate  # On Windows: ooui-env\Scripts\activate

# Install ooui
pip install ooui

# When done, deactivate
deactivate
```

## Next Steps

Once installed, check out:

- [Usage Guide](usage.md) to learn the basic concepts
- [Examples](examples.md) for practical code samples
- [API Reference](api-reference.md) for detailed documentation