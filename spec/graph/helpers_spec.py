from mamba import *
from expects import *

from ooui.helpers import parse_bool_attribute

with description('Helpers module'):
    with description('when parsing a bool attribute'):
        with it('should parse True'):
            expect(parse_bool_attribute(True)).to(equal(True))
            expect(parse_bool_attribute("True")).to(equal(True))
            expect(parse_bool_attribute(1)).to(equal(True))
            expect(parse_bool_attribute("1")).to(equal(True))
            expect(parse_bool_attribute("true")).to(equal(True))
        with it('should parse False'):
            expect(parse_bool_attribute(False)).to(equal(False))
            expect(parse_bool_attribute("False")).to(equal(False))
            expect(parse_bool_attribute("0")).to(equal(False))
            expect(parse_bool_attribute(0)).to(equal(False))
            expect(parse_bool_attribute("false")).to(equal(False))
