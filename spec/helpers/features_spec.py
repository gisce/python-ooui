from mamba import *
from expects import *
from ooui.helpers.features import preprocess_feature_tags


from lxml import etree

def xml_equal(xml1, xml2):
    parser = etree.XMLParser(remove_blank_text=True)

    tree1 = etree.fromstring(xml1, parser)
    tree2 = etree.fromstring(xml2, parser)

    canonical1 = etree.tostring(tree1, method='c14n')
    canonical2 = etree.tostring(tree2, method='c14n')

    return canonical1 == canonical2




with description('preprocess_feature_tags'):

    with it('removes feature nodes where the flag is not enabled'):
        def feature_checker(key):
            return key == "enabled.feature"

        xml_input = """
        <form>
            <feature key="enabled.feature">
                <field name="field_a" />
            </feature>
            <feature key="disabled.feature">
                <field name="field_b" />
            </feature>
            <feature key="disabled.feature" status="disabled">
                <field name="field_c" />
            </feature>
        </form>
        """

        result = preprocess_feature_tags(xml_input, feature_checker)

        expected_xml = """
            <form>
            <field name="field_a" />
            <field name="field_c" />
            </form>
        """

        expect(xml_equal(result, expected_xml)).to(be_true)

    with it('keeps all nodes if feature_checker always returns True'):
        def feature_checker(key):
            return True

        xml_input = """
        <form>
            <feature key="any.feature">
                <field name="field_x" />
            </feature>
        </form>
        """

        result = preprocess_feature_tags(xml_input, feature_checker)
        expected_xml = """
            <form>
            <field name="field_x" />
            </form>
        """
        expect(xml_equal(result, expected_xml)).to(be_true)

    with it('removes all feature nodes if feature_checker always returns False'):
        def feature_checker(key):
            return False

        xml_input = """
        <form>
            <feature key="any.feature">
                <field name="field_x" />
            </feature>
        </form>
        """

        result = preprocess_feature_tags(xml_input, feature_checker)
        expected_xml = """
            <form>
            </form>
        """
        expect(xml_equal(result, expected_xml)).to(be_true)

    with it('removes parent feature if parent is not active even if child is active'):
        def feature_checker(key):
            return key == "enabled.child"

        xml_input = """
        <form>
            <feature key="disabled.parent">
                <field name="field_parent" />
                <feature key="enabled.child">
                    <field name="field_child" />
                </feature>
            </feature>
        </form>
        """

        result = preprocess_feature_tags(xml_input, feature_checker)
        expected_xml = """
            <form>
            </form>
        """
        expect(xml_equal(result, expected_xml)).to(be_true)
