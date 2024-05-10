from mamba import *
from expects import *

from ooui.helpers import parse_bool_attribute
from ooui.helpers.conditions import ConditionParser


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

    with description('when parsing attributes conditions'):
        with it('should parse the keys of attribute'):
            result = ConditionParser.parse_condition("red:active==0;black:active==1 and meter_type=='PF';blue:active==1 and meter_type=='G';green:active==1 and meter_type=='C';")
            expect(result).to(have_len(4))

        with description('when evaluating conditions'):
            with before.all as self:
                self.cond = ConditionParser("red:active==0;black:active==1 and meter_type=='PF';blue:active==1 and meter_type=='G';green:active==1 and meter_type=='C';")

            with it('should return the correct key'):
                result = self.cond.eval({'active': False})
                expect(result).to(equal('red'))

                result = self.cond.eval({'active': True, 'meter_type': 'PF'})
                expect(result).to(equal('black'))

                result = self.cond.eval({'active': True, 'meter_type': 'G'})
                expect(result).to(equal('blue'))

                result = self.cond.eval({'active': True, 'meter_type': 'C'})
                expect(result).to(equal('green'))

                result = self.cond.eval({'active': True, 'meter_type': 'X'})
                expect(result).to(be_none)

            with it('should use time builin'):
                c = ConditionParser("grey:reconcile_id!=0;blue:amount_to_pay==0;red:date_maturity<time.strftime('%Y-%m-%d')")
                from datetime import datetime, timedelta
                dm = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                result = c.eval({'date_maturity': dm, 'reconcile_id': False, 'amount_to_pay': 40})
                expect(result).to(equal('red'))

            with it('should evaluate lists'):
                c = ConditionParser("red:state in ['tall', 'baixa', 'cancelada']")
                result = c.eval({'state': 'tall'})
                expect(result).to(equal('red'))

            with it('should work with AND'):
                c = ConditionParser("grey:state in ('cancel','done');blue:remaining_hours<0;red:bool(date_deadline) & (date_deadline<current_date) & (state in ('draft','open'))")
                result = c.eval({'state': 'open', 'remaining_hours': 10, 'date_deadline': '2021-01-01'})
                expect(result).to(equal('red'))

            with it('should work with False/True/None'):
                c = ConditionParser("blue:valid==False")
                result = c.eval({'valid': False})
                expect(result).to(equal('blue'))

            with it('should represent as string'):
                c = ConditionParser("blue:valid==False")
                expect(str(c)).to(equal('blue:valid==False'))
