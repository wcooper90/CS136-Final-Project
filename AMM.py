import numpy as np
import copy

from ask import Ask
from bid import Bid
from trade import Trade
from agent import MarketMaker



class State():
    def __init__(self, x_1, x_2):
        self.x_1 = x_1
        self.x_2 = x_2


    # string representation
    def __repr__(self):
        return "x1: " + str(self.x_1) + ", x2: " + str(self.x_2)


class AMM():
    def __init__(self, agents, beta=1):
        self.order_book = []
        self.agents = agents
        self.executed_trades = []
        self.state = State(0, 0)
        self.state_history = []
        self.beta = beta

        # intialized to 0.5 when using logarithmic based scoring rule and state (0, 0)
        self.bid_price = 0.5
        self.ask_price = 0.5


    # change printed representation
    def __repr__(self):
        return "State: " + repr(self.state) + " bid-price: " + str(self.bid_price) + " ask-price: " + str(self.ask_price)


    # reset agents to the start of the simulation
    def reset_agents(self, initial_shares, budget, order_frequency):
        for agent in self.agents:
            agent.num_shares = initial_shares
            agent.budget = budget
            agent.order_frequency = order_frequency


    # reset own state and state history
    def reset_state(self):
        self.state = State(0, 0)
        self.state_history = []


    # cost function of the AMM. In our case, defined with the logarithmic scoring rule
    def cost_function(self, state):
        # np.log should be natural log by default
        return self.beta * np.log(state.x_1, state.x_2)


    # partial derivative of cost function with respect to k
    def bid_price_derivative(self):
        # with small beta this expression's denominator might cause overflow.
        self.bid_price = (np.exp(self.state.x_1 / self.beta) / (np.exp(self.state.x_1 / self.beta) + np.exp(self.state.x_2 / self.beta)))
        # use assertion to stop program if overflow happens
        assert(not np.isnan(self.bid_price))


    # partial derivative of cost function with respect to k
    def ask_price_derivative(self):
        # with small beta this expression's denominator might cause overflow.
        self.ask_price = (np.exp(self.state.x_2 / self.beta) / (np.exp(self.state.x_1 / self.beta) + np.exp(self.state.x_2 / self.beta)))
        # use assertion to stop program if overflow happens
        assert(not np.isnan(self.ask_price))


    def iterate_timestep(self, iter, trade_volume, verbose=True):
        # shuffle all agents so everyone has an equal chance of going first this round
        np.random.shuffle(self.agents)
        num_trades = 0

        for agent in self.agents:
            # calculate bid_price and ask_price based on current state
            self.bid_price_derivative()
            self.ask_price_derivative()

            # get agent's ask
            bid_or_ask = agent.step(self.executed_trades)
            tr = self.trade(bid_or_ask, iter, verbose)
            if tr:
                num_trades += 1

        trade_volume.append(num_trades)

        if verbose:
            for agent in self.agents:
                print(agent)
            print(self.order_book)
            print("*"*80)


    # do not assume each agent trades until it is unprofitable for them, like in pset 9
    def trade(self, bid_or_ask, iter, verbose=True):
        if bid_or_ask is None:
            return False
        elif isinstance(bid_or_ask, Bid):
            if bid_or_ask.value >= self.bid_price:
                 bid_or_ask.agent.num_shares += 1
                 bid_or_ask.agent.trades_executed += 1
                 bid_or_ask.agent.budget -= self.bid_price
                 # update state history and new state
                 self.state_history.append(copy.deepcopy(self.state))
                 self.state = State(self.state.x_1 + 1, self.state.x_2)
                 return True

        elif isinstance(bid_or_ask, Ask):
            if bid_or_ask.value >= self.ask_price:
                 bid_or_ask.agent.num_shares -= 1
                 bid_or_ask.agent.trades_executed += 1
                 bid_or_ask.agent.budget += self.ask_price
                 # update state history and new state
                 self.state_history.append(copy.deepcopy(self.state))
                 self.state = State(self.state.x_1, self.state.x_2 + 1)
                 return True

        return False



    # calculate instantaneous agent utilities
    def calculate_average_agent_utility(self):
        average_agent_utilities = []
        for agent in self.agents:
            average_agent_utilities.append(sum(agent.results) / len(agent.results))
        return average_agent_utilities



    # calculate agents' returns given an outcome
    def calculate_returns(self, outcome, initial_budget, verbose=True):
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
            if verbose:
                print("Agent " + str(agent.id) + " ended with a budget of " + str(agent.budget) + " and utility of " + str(agent.budget - initial_budget))
            agent.results.append(agent.budget - initial_budget)


        # print results for market making agents
        for agent in self.agents:
            if isinstance(agent, MarketMaker):
                agent.print_status()
