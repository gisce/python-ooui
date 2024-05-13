from mamba import *
from expects import *
from ooui.graph import parse_graph
from ooui.graph.indicator import GraphIndicator, GraphIndicatorField


with description('A Graph'):
    with it('should parse a basic XML title and type indicator'):
        xml = """<?xml version="1.0"?>
        <graph string="My indicator" type="indicator" color="red:debt>0;green:debt==0" icon="slack" />
        """
        graph = parse_graph(xml)
        assert isinstance(graph, GraphIndicator)
        expect(graph.string).to(equal('My indicator'))
        expect(graph.type).to(equal('indicator'))
        expect(str(graph.icon)).to(equal('slack'))
        expect(str(graph.color)).to(equal('red:debt>0;green:debt==0'))

    with it('should suport indicatorField graphs'):
        xml = """<?xml version="1.0"?>
        <graph string="My indicator" showPercent="1" type="indicatorField" color="red:debt>0;green:debt==0" icon="slack">
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
        expect(graph.show_percent).to(be_true)

    with it("should parse a chart graph XML with type line"):
        xml = """<?xml version="1.0"?>
    <graph type="line">
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