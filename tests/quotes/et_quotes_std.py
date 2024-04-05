# from mootdx.logger import logger
# from mootdx.quotes import Quotes
# from tests.quotes.et_stock_stage import GpPosition, PersonMoney
#
#
# class StdQuotes():
#     client = None
#
#     # 初始化工作
#     def setup_class(self):
#         self.client = Quotes.factory(market='std', timeout=10, verbose=2)  # 标准市场
#         logger.debug('初始化工作')
#
#     # 退出清理工作
#     def teardown_class(self):
#         self.client.client.close()
#         del self.client
#         logger.debug('退出清理工作')
#
#     def testMinute(self, gp, pm):
#         today = '20240403'
#         data1 = self.client.minutes(symbol='180101', date=today)
#         # 当前价格在买卖价中间，则不需要在看了
#         # print(data1)
#
#         for index, row in data1.iterrows():
#             # 一些etf，拿到的金额是实际金额的10倍
#             row["price"] = row["price"] / 10
#             # print(index, round(row["price"],3),  '监控价格买 ' + str(gp.buy_price) + ' 卖' + str(gp.sell_price))
#             # 在途挂单买的金额，如果成交买，则需要付出这么多钱
#             pm.in_buy_money = gp.buy_price * gp.buy_amount
#             # 在途挂单卖的金额,如果成交卖，则收获这么多钱
#             pm.out_sell_money = gp.sell_price * gp.sell_amount
#             # 判断价格在买卖价中间，则不处理
#             if (row["price"] > gp.buy_price and row["price"] < gp.sell_price):
#                 # print("不触发")
#                 continue
#             if (row["price"] < gp.buy_price):
#                 print("按照价格  " + str(gp.buy_price) + "  触发买入")
#                 # 刷新资产，因为在途买资金成为股票份额，初始化，更新可用资金
#                 pm.enable_money = pm.enable_money - pm.in_buy_money
#                 # 股票资产= 股票总资产 * 价格
#                 pm.stock_money = (gp.current_amount + gp.buy_amount) * gp.buy_price
#                 # 总资产
#                 pm.total_money = pm.stock_money + pm.enable_money
#                 # 刷新下一次的买卖价格
#                 gp.refresh_bs_price(gp.buy_price, 'B')
#
#             if (row["price"] > gp.sell_price):
#                 print("按照价格  " + str(gp.sell_price) + "  触发卖出")
#                 # 刷新资产，因为在途买资金成为股票份额，初始化，更新可用资金
#                 pm.enable_money = pm.enable_money + pm.out_sell_money
#                 # 股票资产= 股票总资产 * 价格
#                 pm.stock_money = (gp.current_amount - gp.sell_amount) * gp.sell_price
#                 # 总资产
#                 pm.total_money = pm.stock_money + pm.enable_money
#                 # 刷新下一次的买卖价格
#                 gp.refresh_bs_price(gp.sell_price, 'S')
#
#             # 涉及买卖，因此总资产需要交手续费，大约是1元
#             pm.total_money = pm.total_money - 1
#
#         pm.in_buy_money = 0
#         pm.out_sell_money = 0
#         print(gp)
#         print(pm)
#
#
# def cal_best_percent(percent1, percent2):
#     pm = PersonMoney(total_money=20000,
#                      enable_money=20000 - 1.863 * 9400,
#                      stock_money=1.863 * 9400,
#                      in_buy_money=0,
#                      out_sell_money=0
#                      )
#
#     gp = GpPosition(stock_no=str(180101),
#                     init_price=1.866,
#                     current_amount=9400,
#                     enable_amount=9400,
#                     sell_price=0,
#                     sell_amount=1000,
#                     sell_up_percent=0.3,
#                     buy_price=0,
#                     buy_amount=1000,
#                     buy_fall_percent=0.3
#                     )
#
#     stdmarket = StdQuotes()
#     stdmarket.setup_class()
#     print("-------------------------------------------------")
#     print("原始资金")
#     print(gp)
#     print(pm)
#
#     gp.sell_price = round(gp.init_price * (1 + percent1 / 100), 3)
#     gp.buy_price = round(gp.init_price * (1 - percent2 / 100), 3)
#
#     print("交易后的资金 上涨比例 " + str(percent1) + "下跌比例" + str(percent2))
#     stdmarket.testMinute(gp=gp, pm=pm)
#     return pm.total_money
#
#
# # 保存最大值
# max_money = 0
# for up_percent in range(1, 10):
#     for down_percent in range(1, 10):
#         percent1 = up_percent / 10
#         percent2 = down_percent / 10
#         result_money = cal_best_percent(percent1=percent1, percent2=percent2)
#
#         max_money = max(max_money, result_money)
# print(max_money)
