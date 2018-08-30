class Investor:
    name = 'Default'
    cash = 1.0
    holding = None

    def __init__(self, name, cash):
        self.name = name
        self.cash = cash

    def buy(self, fin_id, label, price, share):
        result = TradeResult()
        if price * share <= self.cash:
            self.cash = self.cash - price * share
            self.holding = Position(fin_id, label, price, share)
            result.msg = '== Successful Trade.'
        else:
            result.msg = '== Failed Trade, not enough cash.'
        result.print_me()
        return result

    def print_me(self):
        print('Name: ' + self.name)
        print('Cash: ' + str(self.cash))
        if self.holding is not None:
            self.holding.print_me()


class Position:
    finst = None
    share = 0
    market_value = 0

    def __init__(self, fin_id, label, price, share):
        self.finst = Finst(label, fin_id, price)
        self.share = share
        self.market_value = self.finst.price * self.share

    def print_me(self):
        print('Holding: ' + str(self.market_value) + '[' + self.finst.label + ']')


class Finst:
    label = 'Default'
    fin_id = '600002'
    price = 0.0

    def __init__(self, label, fin_id, price):
        self.label = label
        self.fin_id = fin_id
        self.price = price


class TradeResult:
    msg = 'Error!'

    def print_me(self):
        print(self.msg)