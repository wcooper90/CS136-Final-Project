import numpy as np
import random
from ask import Ask
from bid import Bid


class Agent():
    def __init__(self, id, true_value, num_shares, budget, order_frequency):
        self.id = id
        self.value = true_value
        self.num_shares = num_shares
        self.budget = budget
        self.order_frequency = order_frequency
        self.results = []
        self.trades_executed = 0

    def step(self, history):
        if random.random() <= self.order_frequency:
            order = self.calculate_order(history)
            return order
        return None

    def __repr__(self):
        return "Agent " + str(self.id) + ": " + str(self.num_shares) + " shares -- " + str(self.budget) + " budget remaining -- " + str(self.value) + " true value -- " \
                    + str(self.trades_executed) + " trades executed"


class BuyAgent(Agent):
    def __init__(self, id, true_value, num_shares, budget, order_frequency):
        super().__init__(id, true_value, num_shares, budget, order_frequency)


    def calculate_order(self, history):
        bid = None
        # make sure this agent has enough budget to actually pay their bid price
        if self.budget >= self.value:
            bid = Bid(self, self.value)
        return bid


class SellAgent(Agent):
    def __init__(self, id, true_value, num_shares, budget, order_frequency):
        super().__init__(id, true_value, num_shares, budget, order_frequency)


    def calculate_order(self, history):
        ask = Ask(self, self.value)
        return ask



class MarketMaker(Agent):
    def __init__(self, id, true_value, num_shares, budget, order_frequency, alpha):
        super().__init__(id, true_value, num_shares, budget, order_frequency)
        self.history = []
        # learning rate
        self.alpha = alpha
        self.bid_price = self.value
        self.ask_price = self.value
        self.spread_value = None


    def calculate_order(self, history):
        self.update_valuation(history)
        # replace hard coded integer with number of agents in the simulation
        bid_orders = [Bid(self, self.bid_price) for i in range(100)]
        ask_orders = [Ask(self, self.ask_price) for i in range(100)]

        return bid_orders + ask_orders


    def update_valuation(self, trade_book):
        round_num = 0
        if len(trade_book) > 0:
            round_num = trade_book[-1].iter

        # analyze trades from last round that did not involve this particular market making agent
        recent_trading_prices = [trade.value for trade in trade_book if trade.iter == round_num and trade.seller != self and trade.buyer != self]


        if len(recent_trading_prices) > 0:
            mean = np.mean(recent_trading_prices)
            std = np.std(recent_trading_prices)

            if mean > self.value:
                self.value += self.alpha * (mean - self.value)
            else:
                self.value -= self.alpha * (self.value - mean)

            # will offer to buy a contract one standard deviation below the market price
            self.bid_price = self.value - std
            # will offer to sell a contract one standard deviation above the market price
            self.ask_price = self.value + std


    def print_status(self):
        print("Market maker agent " + str(self.id) + ": ")
        print("bid_price: " + str(self.bid_price))
        print("ask_price: " + str(self.ask_price))
        print("true valuation: " + str(self.value))
        print("number of trades executed: " + str(self.trades_executed))
        print("learning rate: " + str(self.alpha))
        print("number of shares: " + str(self.num_shares))
        print("final utility: " + str(self.budget)) 
