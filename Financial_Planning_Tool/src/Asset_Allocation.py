import Assets
import utils
import Personal
import Debt
from utils import output
from utils import STOCK_GROWTH_RATE, BOND_GROWTH_RATE, CASH_GROWTH_RATE

LIFE_EXPECTANCY = 90

class Asset_Allocation:
    def __init__(self, assets, surplus, mortgage, personal, expenses):
        self.a = assets
        self.d = mortgage
        self.s = surplus
        self.p = personal
        self.e = expenses
        self.t = personal.getRetireAge() - personal.getCurrentAge()

    def allocate(self):
        output.section_start("Mortgage payoff calculation and projection at retirement")
        equity = 0.0
        debt = 0.0
        for n,v in self.d.items():
            (val, rate, years) = v
            home_equity, home_debt = utils.mortgage_payment(val, int(self.t*12), rate, years)
            equity += home_equity
            debt += home_debt
        output.action("Keep paying your mortgage as regular to build home equity")
        output.section_end()
        assets = self.a.total
        allocation = dict()
        equity_percent = self.p.data['risk aversion'];
        bond_percent = 100 - equity_percent

        output.section_start("Investing your assets with chosen asset allocation %d:%d (stocks:bonds)" %
                             (equity_percent, bond_percent))
        allocation['equity'] = (assets * equity_percent/100, STOCK_GROWTH_RATE)
        allocation['bond'] = (assets * bond_percent/100, BOND_GROWTH_RATE)
        output.action("Re-balance your assets of %s%.2f as %d_%d (stocks_bonds)" %
                     (utils.get_currency(), assets, equity_percent, bond_percent))
        utils.piechart("Asset_allocated_now", "Asset allocation now", [n for n,v in allocation.items()], [v[0] for n,v in allocation.items()])
        invest = dict()
        invest['equity'] = self.s * equity_percent/100
        invest['bond'] = self.s * bond_percent/100
        total = utils.fv_allocation(allocation, invest, self.t)
        allocation['real estate'] = (equity)
        total += equity
        output.action("Invest %s%.2f per month for %.2f years" % (utils.get_currency(), self.s, self.t))
        output.info("Total assets with proper allocation: %s%.2f" % (utils.get_currency(), total))
        output.info("Total debt at retirement: %s%.2f" % (utils.get_currency(), debt))
        output.info("Net worth: %s%.2f" % (utils.get_currency(), (total - debt)))
        utils.piechart("Assets_in_%d_years" % (self.t), "Assets in %d years" %
                       (self.t), [n for n,v in allocation.items()], [v for n,v in allocation.items()])
        net_worth = total - debt
        output.action("Preserve your net worth %s%.2f by moving to safer assets" % (utils.get_currency(), net_worth))
        expense = self.e.get_monthly()
        years = net_worth/(expense*12)
        output.info("Your net worth will last %d years if you spend %s%.2f monthly as of today." %
                    (years, utils.get_currency(), expense))
        if ((years + self.p.getRetireAge()) > LIFE_EXPECTANCY):
            output.info("You have a secure retirement considering life expectancy of %d years" % (LIFE_EXPECTANCY))
            output.action("Enjoy your retirement with %s%.2f, withdraw %s%.2f per month." %
                          (utils.get_currency(), net_worth, utils.get_currency(), expense))
        else:
            output.warn("You will not have enough corpus to last a retired life expectancy of %d years" % (LIFE_EXPECTANCY))
            output.action("You need to save more or reduce your expenses")
        output.section_end()
