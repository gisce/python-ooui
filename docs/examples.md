# Examples

This page provides practical examples of using Python OOUI for various scenarios.

## Graph Examples

### Line Chart for Time Series Data

```python
from ooui.graph import parse_graph

# Define a line chart for sales over time
sales_chart_xml = '''
<graph type="line" string="Monthly Sales">
    <field name="month" type="date"/>
    <field name="revenue" type="float" operator="sum"/>
</graph>
'''

# Parse the graph
sales_graph = parse_graph(sales_chart_xml)

# Sample data
sales_data = [
    {'month': '2023-01-01', 'revenue': 15000.0, 'sales_rep': 'John'},
    {'month': '2023-01-01', 'revenue': 12000.0, 'sales_rep': 'Jane'},
    {'month': '2023-02-01', 'revenue': 18000.0, 'sales_rep': 'John'},
    {'month': '2023-02-01', 'revenue': 16000.0, 'sales_rep': 'Jane'},
    {'month': '2023-03-01', 'revenue': 21000.0, 'sales_rep': 'John'},
]

# Field definitions
fields = {
    'month': {'type': 'date', 'string': 'Month'},
    'revenue': {'type': 'float', 'string': 'Revenue'},
    'sales_rep': {'type': 'char', 'string': 'Sales Rep'}
}

# Process the data
chart_data = sales_graph.process(sales_data, fields)
print("Processed chart data:", chart_data)
```

### Bar Chart with Multiple Series

```python
# Bar chart comparing performance across categories
performance_xml = '''
<graph type="bar" string="Department Performance">
    <field name="department" type="char"/>
    <field name="target" type="float" operator="sum"/>
    <field name="actual" type="float" operator="sum"/>
</graph>
'''

performance_graph = parse_graph(performance_xml)

performance_data = [
    {'department': 'Sales', 'target': 100000, 'actual': 95000},
    {'department': 'Marketing', 'target': 50000, 'actual': 52000},
    {'department': 'Support', 'target': 30000, 'actual': 28000},
]

fields = {
    'department': {'type': 'char'},
    'target': {'type': 'float'},
    'actual': {'type': 'float'}
}

result = performance_graph.process(performance_data, fields)
```

### Pie Chart for Distribution Analysis

```python
# Pie chart showing market share
market_share_xml = '''
<graph type="pie" string="Market Share by Region">
    <field name="region" type="char"/>
    <field name="sales" type="float" operator="sum"/>
</graph>
'''

market_graph = parse_graph(market_share_xml)

market_data = [
    {'region': 'North America', 'sales': 450000},
    {'region': 'Europe', 'sales': 380000},
    {'region': 'Asia Pacific', 'sales': 290000},
    {'region': 'Latin America', 'sales': 125000},
    {'region': 'Africa', 'sales': 75000},
]

fields = {
    'region': {'type': 'char'},
    'sales': {'type': 'float'}
}

pie_data = market_graph.process(market_data, fields)
```

### Indicator for KPI Dashboard

```python
# Single KPI indicator
kpi_xml = '''
<graph type="indicator" string="Total Revenue">
    <field name="revenue" type="float" operator="sum"/>
</graph>
'''

kpi_graph = parse_graph(kpi_xml)

revenue_data = [
    {'revenue': 15000},
    {'revenue': 22000},
    {'revenue': 18500},
    {'revenue': 31000},
]

kpi_result = kpi_graph.process(revenue_data, {'revenue': {'type': 'float'}})
print(f"Total Revenue: {kpi_result}")
```

### Indicator with Progress Bar

```python
# Indicator with progress bar showing completion percentage
progress_xml = '''
<graph type="indicator" string="Project Completion" progressbar="1">
    <field name="completed_tasks" type="integer" operator="sum"/>
</graph>
'''

progress_graph = parse_graph(progress_xml)

# Process with value and total
result = progress_graph.process(75, 100)
print(f"Progress: {result}")
# Output: {'value': 75, 'total': 100, 'type': 'indicator', 'percent': 75.0, 'progressbar': True}
```

### Indicator with Percentage Display

```python
# Indicator showing percentage without progress bar
percent_xml = '''
<graph type="indicator" string="Success Rate" showPercent="1" suffix="%">
    <field name="successful" type="integer" operator="sum"/>
</graph>
'''

percent_graph = parse_graph(percent_xml)

result = percent_graph.process(85, 100)
print(f"Success Rate: {result}")
# Output: {'value': 85, 'total': 100, 'type': 'indicator', 'percent': 85.0, 'suffix': '%', 'showPercent': True}
```

## Tree View Examples

### Basic Employee List

```python
from ooui.tree import parse_tree

# Simple employee tree view
employee_tree_xml = '''
<tree string="Employee Directory" editable="top">
    <field name="name"/>
    <field name="department"/>
    <field name="email"/>
    <field name="hire_date"/>
</tree>
'''

employee_tree = parse_tree(employee_tree_xml)

print(f"Tree title: {employee_tree.string}")
print(f"Editable: {employee_tree.editable}")
print(f"Number of fields: {len(employee_tree.fields)}")
```

### Tree with Conditional Colors

```python
# Order list with status-based coloring
order_tree_xml = '''
<tree string="Order Management" 
      colors="red:status=='cancelled';orange:status=='pending';green:status=='completed'">
    <field name="order_id"/>
    <field name="customer"/>
    <field name="status"/>
    <field name="amount"/>
    <field name="order_date"/>
</tree>
'''

order_tree = parse_tree(order_tree_xml)

# Check which fields are used in conditions
conditional_fields = order_tree.fields_in_conditions
print(f"Fields in color conditions: {conditional_fields['colors']}")
# Output: ['status']
```

### Tree with Status Indicators

```python
# Project list with status indicators
project_tree_xml = '''
<tree string="Project Dashboard" 
      colors="blue:priority=='high';yellow:priority=='medium'"
      status="red:days_overdue > 0;green:progress >= 100">
    <field name="project_name"/>
    <field name="manager"/>
    <field name="priority"/>
    <field name="progress"/>
    <field name="days_overdue"/>
</tree>
'''

project_tree = parse_tree(project_tree_xml)

# Get all conditional fields
all_conditions = project_tree.fields_in_conditions
print("Color fields:", all_conditions.get('colors', []))
print("Status fields:", all_conditions.get('status', []))
```

## Condition Parser Examples

### Simple Status Conditions

```python
from ooui.helpers import ConditionParser

# Define status-based conditions
status_condition = "red:status=='error';yellow:status=='warning';green:status=='ok'"
parser = ConditionParser(status_condition)

# Test with different statuses
test_cases = [
    {'status': 'error'},
    {'status': 'warning'}, 
    {'status': 'ok'},
    {'status': 'unknown'}
]

for case in test_cases:
    result = parser.eval(case)
    print(f"Status {case['status']} -> Color {result}")

# Output:
# Status error -> Color red  
# Status warning -> Color yellow
# Status ok -> Color green
# Status unknown -> Color None
```

### Numeric Range Conditions

```python
# Score-based color coding
score_condition = "red:score < 60;yellow:score < 80;green:score >= 80"
score_parser = ConditionParser(score_condition)

scores = [45, 65, 72, 85, 92]
for score in scores:
    color = score_parser.eval({'score': score})
    print(f"Score {score} -> {color}")
```

### Complex Multi-Field Conditions

```python
# Complex business logic
complex_condition = """
urgent:priority=='high' and days_remaining <= 1;
warning:priority=='medium' and days_remaining <= 3;
normal:priority=='low' or days_remaining > 7
"""

complex_parser = ConditionParser(complex_condition)

test_scenarios = [
    {'priority': 'high', 'days_remaining': 0},
    {'priority': 'medium', 'days_remaining': 2},
    {'priority': 'low', 'days_remaining': 5},
    {'priority': 'medium', 'days_remaining': 10},
]

for scenario in test_scenarios:
    result = complex_parser.eval(scenario)
    print(f"{scenario} -> {result}")
```

## Domain Parser Examples

### Basic Query Filters

```python
from ooui.helpers import Domain

# Simple equality filter
basic_domain = Domain("[('active', '=', True), ('type', '=', 'customer')]")
result = basic_domain.parse()
print("Basic domain:", result)

# Range filter
range_domain = Domain("[('age', '>=', 18), ('age', '<=', 65)]")
result = range_domain.parse()
print("Range domain:", result)
```

### Dynamic Domains with Variables

```python
# Domain with user-provided values
user_domain = Domain("[('created_by', '=', user_id), ('date', '>=', start_date)]")

# Provide values at runtime
context = {
    'user_id': 42,
    'start_date': '2023-01-01'
}

parsed_domain = user_domain.parse(context)
print("User domain:", parsed_domain)
```

### Complex Logical Operations

```python
# OR conditions
or_domain = Domain("""
[
    '|', 
    ('state', '=', 'active'), 
    ('state', '=', 'pending'),
    ('priority', '=', 'high')
]
""")

result = or_domain.parse()
print("OR domain:", result)
```

## Data Aggregation Examples

### Sales Reporting

```python
from ooui.helpers.aggregated import Aggregator

# Sales aggregation rules
sales_aggregator = Aggregator({
    'total_sales': {'operator': 'sum', 'field': 'amount'},
    'avg_deal_size': {'operator': 'avg', 'field': 'amount'},
    'deal_count': {'operator': 'count', 'field': 'deal_id'},
    'largest_deal': {'operator': 'max', 'field': 'amount'},
    'smallest_deal': {'operator': 'min', 'field': 'amount'}
})

# Sample sales data
sales_data = [
    {'amount': 5000, 'deal_id': 1, 'rep': 'Alice', 'region': 'North'},
    {'amount': 7500, 'deal_id': 2, 'rep': 'Bob', 'region': 'North'},
    {'amount': 3200, 'deal_id': 3, 'rep': 'Charlie', 'region': 'South'},
    {'amount': 9800, 'deal_id': 4, 'rep': 'Diana', 'region': 'South'},
]

# Aggregate by region
regional_sales = sales_aggregator.aggregate(sales_data, group_by='region')
print("Regional Sales:", regional_sales)

# Aggregate by sales rep  
rep_sales = sales_aggregator.aggregate(sales_data, group_by='rep')
print("Rep Sales:", rep_sales)

# Overall aggregation (no grouping)
total_sales = sales_aggregator.aggregate(sales_data)
print("Total Sales:", total_sales)
```

### Performance Metrics

```python
# Website performance metrics
perf_aggregator = Aggregator({
    'total_visits': {'operator': 'sum', 'field': 'visits'},
    'avg_load_time': {'operator': 'avg', 'field': 'load_time'},
    'bounce_rate': {'operator': 'avg', 'field': 'bounce_rate'},
    'peak_concurrent': {'operator': 'max', 'field': 'concurrent_users'}
})

performance_data = [
    {'visits': 1200, 'load_time': 2.3, 'bounce_rate': 0.35, 'concurrent_users': 45, 'page': 'home'},
    {'visits': 800, 'load_time': 1.8, 'bounce_rate': 0.28, 'concurrent_users': 32, 'page': 'products'},
    {'visits': 600, 'load_time': 3.1, 'bounce_rate': 0.42, 'concurrent_users': 28, 'page': 'contact'},
]

page_metrics = perf_aggregator.aggregate(performance_data, group_by='page')
print("Page Performance:", page_metrics)
```

## Date Range Examples

### Time-based Analysis

```python
from ooui.helpers.dates import get_date_range, DateRange
from datetime import datetime

# Predefined ranges
today = get_date_range('today')
this_week = get_date_range('this_week')
this_month = get_date_range('this_month')

print(f"Today: {today.start} to {today.end}")
print(f"This week: {this_week.start} to {this_week.end}")
print(f"This month: {this_month.start} to {this_month.end}")

# Custom date range
quarter_start = DateRange('2023-01-01', '2023-03-31')
print(f"Q1 2023: {quarter_start.start} to {quarter_start.end}")
```

### Filtering Data by Date Range

```python
# Filter sales data by date range
def filter_by_date_range(data, date_field, date_range):
    """Filter data within a date range."""
    filtered = []
    for record in data:
        record_date = datetime.strptime(record[date_field], '%Y-%m-%d')
        if date_range.start <= record_date <= date_range.end:
            filtered.append(record)
    return filtered

# Sample sales data
sales_records = [
    {'date': '2023-01-15', 'amount': 1500},
    {'date': '2023-02-20', 'amount': 2200},
    {'date': '2023-03-10', 'amount': 1800},
    {'date': '2023-04-05', 'amount': 2500},
]

# Filter for Q1
q1_range = DateRange('2023-01-01', '2023-03-31')
q1_sales = filter_by_date_range(sales_records, 'date', q1_range)
print("Q1 Sales:", q1_sales)
```

## Field Operations Examples

### Data Transformation

```python
from ooui.graph.fields import get_value_for_operator

# Sample monthly sales figures
monthly_sales = [12000, 15000, 11000, 18000, 22000, 19000]

# Calculate various metrics
total = get_value_for_operator(monthly_sales, 'sum')
average = get_value_for_operator(monthly_sales, 'avg')
best_month = get_value_for_operator(monthly_sales, 'max')
worst_month = get_value_for_operator(monthly_sales, 'min')
months_count = get_value_for_operator(monthly_sales, 'count')

print(f"Total Sales: ${total:,.2f}")
print(f"Average Monthly: ${average:,.2f}")
print(f"Best Month: ${best_month:,.2f}")
print(f"Worst Month: ${worst_month:,.2f}")
print(f"Months Tracked: {months_count}")
```

## Utility Functions Examples

### Boolean Parsing

```python
from ooui.helpers import parse_bool_attribute

# Parse various boolean representations
config_values = ['1', '0', 'true', 'false', 'True', 'False', 'yes', 'no']

for value in config_values:
    parsed = parse_bool_attribute(value)
    print(f"'{value}' -> {parsed}")
```

### HTML Entity Cleanup

```python
from ooui.helpers import replace_entities

# Clean HTML entities from text
html_texts = [
    "Price &gt; $100",
    "Q&amp;A Section", 
    "&lt;tag&gt; content &lt;/tag&gt;",
    "R&amp;D Department",
    "50% &lt; target &lt; 75%"
]

for text in html_texts:
    clean = replace_entities(text)
    print(f"Original: {text}")
    print(f"Cleaned:  {clean}\n")
```

## Complete Integration Example

### Dashboard Data Processing

```python
from ooui.graph import parse_graph
from ooui.tree import parse_tree
from ooui.helpers import ConditionParser, Aggregator
from ooui.helpers.dates import get_date_range

# Complete dashboard setup
class SalesDashboard:
    def __init__(self):
        # Define graphs
        self.sales_trend = parse_graph('''
            <graph type="line" string="Sales Trend">
                <field name="date" type="date"/>
                <field name="amount" type="float" operator="sum"/>
            </graph>
        ''')
        
        self.top_products = parse_graph('''
            <graph type="bar" string="Top Products">
                <field name="product" type="char"/>
                <field name="revenue" type="float" operator="sum"/>
            </graph>
        ''')
        
        # Define tree view
        self.sales_list = parse_tree('''
            <tree string="Recent Sales" 
                  colors="green:amount>=1000;orange:amount>=500;red:amount<500">
                <field name="date"/>
                <field name="customer"/>
                <field name="product"/>
                <field name="amount"/>
            </tree>
        ''')
        
        # Setup aggregation
        self.aggregator = Aggregator({
            'total_revenue': {'operator': 'sum', 'field': 'amount'},
            'avg_deal_size': {'operator': 'avg', 'field': 'amount'},
            'total_deals': {'operator': 'count', 'field': 'sale_id'}
        })
    
    def process_dashboard_data(self, raw_data):
        """Process raw sales data for dashboard display."""
        fields = {
            'date': {'type': 'date'},
            'amount': {'type': 'float'},
            'product': {'type': 'char'},
            'customer': {'type': 'char'},
            'sale_id': {'type': 'integer'}
        }
        
        # Filter for current month
        current_month = get_date_range('this_month')
        
        # Process trend data
        trend_data = self.sales_trend.process(raw_data, fields)
        
        # Aggregate by product
        product_data = []
        product_totals = {}
        for record in raw_data:
            product = record['product']
            if product not in product_totals:
                product_totals[product] = 0
            product_totals[product] += record['amount']
        
        for product, revenue in product_totals.items():
            product_data.append({'product': product, 'revenue': revenue})
            
        top_products_data = self.top_products.process(product_data, fields)
        
        # Overall metrics
        metrics = self.aggregator.aggregate(raw_data)
        
        return {
            'sales_trend': trend_data,
            'top_products': top_products_data,
            'metrics': metrics,
            'tree_config': self.sales_list
        }

# Usage
dashboard = SalesDashboard()

sample_data = [
    {'date': '2023-10-01', 'amount': 1500, 'product': 'Widget A', 'customer': 'Acme Corp', 'sale_id': 1},
    {'date': '2023-10-02', 'amount': 750, 'product': 'Widget B', 'customer': 'Tech Inc', 'sale_id': 2},
    {'date': '2023-10-03', 'amount': 2200, 'product': 'Widget A', 'customer': 'Global Ltd', 'sale_id': 3},
]

dashboard_data = dashboard.process_dashboard_data(sample_data)
print("Dashboard processed successfully!")
print("Metrics:", dashboard_data['metrics'])
```

This comprehensive set of examples demonstrates the full capabilities of Python OOUI across all its major components. Each example is practical and can be adapted for real-world use cases.