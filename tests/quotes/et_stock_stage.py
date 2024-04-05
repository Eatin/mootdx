import unittest
from dataclasses import dataclass
from enum import Enum


class BS_STATUS(Enum):
    ONLY_BUY = 1
    ONLY_SELL = 2
    BOTH_OK = 3
    BOTH_NOT = 4


'''
个人资产
'''


@dataclass
class PersonMoney():
    '''资金总额'''
    total_money: float
    '''可用资金总额'''
    enable_money: float
    '''票额'''
    stock_money: float
    '''在途买资金'''
    in_buy_money: float
    '''在途卖资金'''
    out_sell_money: float


'''
股票信息
'''


@dataclass
class GpPosition():
    '''股票号码'''
    stock_no: str
    '''现价'''
    init_price: float
    '''持有份额'''
    current_amount: int
    '''可用份额'''
    enable_amount: int

    '''卖价'''
    sell_price: float
    '''卖出份额'''
    sell_amount: int
    '''上涨多少卖出份额'''
    sell_up_percent: float

    '''买价'''
    buy_price: float
    '''买入份额'''
    buy_amount: int
    '''下跌多少买入份额'''
    buy_fall_percent: float

    def refresh_bs_price(self, deal_price, bs_type, pm):
        self.buy_price = round(deal_price * (1 - self.buy_fall_percent / 100), 3)
        self.sell_price = round(deal_price * (1 + self.sell_up_percent / 100), 3)
        if (bs_type == 'S'):
            self.enable_amount = self.enable_amount - self.sell_amount
            self.current_amount = (self.current_amount - self.sell_amount)

        if (bs_type == 'B'):
            self.current_amount = (self.current_amount + self.buy_amount)

        if ((self.enable_amount - self.sell_amount > 0) and (pm.enable_money > self.buy_price * self.buy_amount)):
            return BS_STATUS.BOTH_OK

        if (self.enable_amount - self.sell_amount < 0):
            self.sell_price = 2147483647
            return BS_STATUS.ONLY_BUY
        if (pm.enable_money < self.buy_price * self.buy_amount):
            self.buy_price = 0
            # 已经不足支付下次的购买
            return BS_STATUS.ONLY_SELL

        return BS_STATUS.BOTH_NOT
'''
股票信息
'''


@dataclass
class JyMessage():
    '''股票号码'''
    stock_no = 80000
    '''现价'''
    init_price = 3.67
    '''持有份额'''
    current_amount = 10000
    '''可用份额'''
    current_amount = 10000
