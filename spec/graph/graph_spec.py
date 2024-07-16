from mamba import *
from expects import *
from ooui.graph import parse_graph
from ooui.graph.indicator import GraphIndicator, GraphIndicatorField


with description('A Graph'):
    with it('should parse a basic XML title and type indicator'):
        xml = """<?xml version="1.0"?>
        <graph string="My indicator" type="indicator" color="red:debt>0;green:debt==0" icon="slack"  totalDomain="[('user', '=', uid)]"/>
        """
        graph = parse_graph(xml)
        assert isinstance(graph, GraphIndicator)
        expect(graph.string).to(equal('My indicator'))
        expect(graph.type).to(equal('indicator'))
        expect(str(graph.icon)).to(equal('slack'))
        expect(str(graph.color)).to(equal('red:debt>0;green:debt==0'))
        expect(str(graph.total_domain)).to(equal("[('user', '=', uid)]"))
        expect(graph.total_domain.parse({'uid': 3})).to(equal([('user', '=', 3)]))

    with it('should suport indicatorField graphs'):
        xml = """<?xml version="1.0"?>
        <graph string="My indicator" showPercent="1" type="indicatorField" color="red:debt>0;green:debt==0" icon="slack" suffix="kW">
            <field name="potencia" operator="+" />
        </graph>
        """
        graph = parse_graph(xml)
        assert isinstance(graph, GraphIndicatorField)
        expect(graph.string).to(equal('My indicator'))
        expect(graph.type).to(equal('indicatorField'))
        expect(str(graph.icon)).to(equal('slack'))
        expect(str(graph.color)).to(equal('red:debt>0;green:debt==0'))
        expect(graph.fields).to(contain_only('potencia'))
        expect(graph.total_domain).to(be_none)
        expect(graph.show_percent).to(be_true)
        expect(graph.suffix).to(equal('kW'))

    with it("should parse a chart graph XML with type line"):
        xml = """<?xml version="1.0"?>
    <graph type="line" y_range="auto">
      <field name="data_alta" axis="x"/>
      <field name="data_alta" operator="+" axis="y"/>
    </graph>
    """
        graph = parse_graph(xml)
        expect(graph.type).to(equal('line'))
        expect(graph.x).to(not_(be_none))
        expect(graph.y).to(not_(be_none))
        expect(graph.x.name).to(equal('data_alta'))
        expect(graph.y[0].name).to(equal('data_alta'))
        expect(graph.x.axis).to(equal('x'))
        expect(graph.y[0].axis).to(equal('y'))
        expect(graph.y[0].operator).to(equal('+'))
        expect(graph.y_range).to(equal('auto'))

    with description("Processing a Graph"):
        with description("A line graph with y_range auto"):
            with it("should return yAxisProps to the result with min and max values"):
                xml = """<?xml version="1.0"?>
                <graph type="line" y_range="auto" timerange="day">
                  <field name="date" axis="x"/>
                  <field name="v" operator="+" axis="y"/>
                </graph>
                """
                graph = parse_graph(xml)
                values = [
                    {'date': '2024-01-01', 'v': 10},
                    {'date': '2024-01-02', 'v': 20},
                    {'date': '2024-01-03', 'v': 30}
                ]
                fields = {'date': {'type': 'date'}, 'v': {'type': 'integer'}}
                result = graph.process(values, fields)
                expect(result['yAxisProps']).to(equal({
                    'mode': 'auto',
                    'min': 8,
                    'max': 32
                }))
        with description("A line graph with y_range to full"):
            with it("should return yAxisProps to the result with mode full"):
                xml = """<?xml version="1.0"?>
                <graph type="line" y_range="full" timerange="day">
                  <field name="date" axis="x"/>
                  <field name="v" operator="+" axis="y"/>
                </graph>
                """
                graph = parse_graph(xml)
                values = [
                    {'date': '2024-01-01', 'v': 10},
                    {'date': '2024-01-02', 'v': 20},
                    {'date': '2024-01-03', 'v': 30}
                ]
                fields = {'date': {'type': 'date'}, 'v': {'type': 'integer'}}
                result = graph.process(values, fields)
                expect(result['yAxisProps']).to(equal({
                    'mode': 'full',
                }))
