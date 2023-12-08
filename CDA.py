import numpy as np
from ask import Ask
from bid import Bid
from trade import Trade
from agent import MarketMaker, BuyAgent, SellAgent



class CDA():
    def __init__(self, agents):
        self.order_book = []
        self.agents = agents
        self.executed_trades = []


    # reset agents to the start of the simulation
    def reset_agents(self, initial_shares, budget, order_frequency):
        for agent in self.agents:
            agent.reset()


    def iterate_timestep(self, iter, trade_volume, verbose=True):
        if verbose:
            print("Iteration: " + str(iter))

        # shuffle agents so they all have equal chance of submitting an order first at this iteration
        np.random.shuffle(self.agents)


        # marketmakers always get to go first, but only after the first round
        if iter > 0:
            for agent in self.agents:
                if isinstance(agent, MarketMaker):
                    # first remove all orders placed from last iteration by this marketmaker
                    self.remove_orders(agent)
                    market_maker_orders = agent.step(self.executed_trades)
                    if market_maker_orders is not None:
                        self.order_book = self.order_book + market_maker_orders


        # rest of agents now go to make trades
        num_trades = 0
        for agent in self.agents:
            if not isinstance(agent, MarketMaker):
                # agent places order if they can
                bid_or_ask = agent.step(self.executed_trades)
                # make sure the order is not None and not already in the book
                if bid_or_ask is not None and not self.check_if_order_in_book(bid_or_ask):
                    self.order_book.append(bid_or_ask)
                    # excute trade if possible
                    tr = self.trade(verbose, iter)
                    if tr:
                        num_trades += 1

        trade_volume.append(num_trades)

        if verbose:
            for agent in self.agents:
                print(agent)
            print(self.order_book)
            print("*"*80)


    # takes agent as argument, removes the orders from the order book with this agent as a buyer or seller
    def remove_orders(self, agent):
        bruh = []
        for order in self.order_book:
            if order.agent != agent:
                bruh.append(order)

        self.order_book = bruh
        # self.order_book = [order for order in self.order_book if order.agent != agent]


    # find the most recent viable trade and execute it
    def trade(self, verbose, iter):
        recent_order = self.order_book[-1]
        traded_order = None
        order_price = None
        seller = None
        buyer = None
        spread = None
        # if the most recent order is an Ask, filter only through Bids
        if isinstance(recent_order, Ask):
            for order in self.order_book[:-1]:
                if isinstance(order, Ask):
                    continue
                # if the bid's value is greater than the ask, the traded_order's price is set to the bid's value
                else:
                    if order.value >= recent_order.value:
                        traded_order = order
                        order_price = traded_order.value
                        # buyer submitted the bid
                        buyer = traded_order.agent
                        # seller submitted the recent ask
                        seller = recent_order.agent
                        # set spread
                        spread = np.abs(order.value - recent_order.value)
                        break
        # otherwise only filter through Asks
        else:
            for order in self.order_book[:-1]:
                if isinstance(order, Bid):
                    continue
                else:
                    # if the ask's value is less than the bid, traded_order's price is set to ask's value
                    if order.value <= recent_order.value:
                        traded_order = order
                        order_price = traded_order.value
                        # seller submitted the ask
                        seller = traded_order.agent
                        # buyer submitted the recent bid
                        buyer = recent_order.agent
                        # set spread
                        spread = np.abs(order.value - recent_order.value)
                        break


        if traded_order is not None:
            # buyer cannot afford to buy
            if buyer.budget - order_price < 0:
                return False

            # remove the matched order
            self.order_book.remove(traded_order)
            # remove the recent order that was matched
            self.order_book.pop()
            buyer.budget -= order_price
            buyer.num_shares += 1
            seller.budget  += order_price
            seller.num_shares -=1

            # update number of trades each agent has made
            buyer.trades_executed += 1
            seller.trades_executed += 1


            if isinstance(buyer, MarketMaker):
                buyer.buys += 1
            if isinstance(seller, MarketMaker):
                seller.sales += 1

            assert(buyer.budget >= 0)

            new_trade = Trade(buyer, seller, order_price, spread, iter)
            self.executed_trades.append(new_trade)


            if verbose:
                print("Agent " + str(buyer.id) + " bought 1 share from agent " + str(seller.id) + " for a price of " + str(order_price))
            return True

        return False



    def check_if_order_in_book(self, order):
        for o in self.order_book:
            if o.agent.id == order.agent.id and o.agent.value == order.agent.value:
                return True
        return False


    def calculate_returns(self, outcome, initial_budget, market_maker_budget, verbose=True):
        if verbose:
            print("CDA results:" )
        if outcome:
            if verbose:
                print("The event DID happen!")
            for agent in self.agents:
                # if they have negative number of shares, it will be subtracted from their budget
                agent.budget += agent.num_shares

        else:
            if verbose:
                print("The event did NOT happen!")


        for agent in self.agents:
            # if verbose:
            #     print("Agent " + str(agent.id) + " ended with a budget of " + str(agent.budget) + " and utility of " + str(agent.budget - initial_budget))

            # market makers have a separate intial budget to subtract
            if isinstance(agent, MarketMaker):
                agent.results.append(agent.budget - market_maker_budget)
            else:
                agent.results.append(agent.budget - initial_budget)


        # print results for market making agents
        for agent in self.agents:
            if isinstance(agent, MarketMaker):
                agent.print_status(market_maker_budget)


    def calculate_average_agent_utility(self, include_market_makers=False):
        average_agent_utilities = []
        for agent in self.agents:
            if isinstance(agent, MarketMaker):
                if not include_market_makers:
                    continue
            average_agent_utilities.append(sum(agent.results) / len(agent.results))
        return average_agent_utilities


    def calculate_average_market_maker_utility(self):
        market_maker_utilities = []
        for agent in self.agents:
            if isinstance(agent, MarketMaker):
                market_maker_utilities.append(sum(agent.results) / len(agent.results))
        return market_maker_utilities


    def calculate_unique_traders(self):
        return sum([1 for agent in self.agents if agent.trades_executed != 0])
