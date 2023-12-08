import numpy as np
import random
from tqdm import tqdm


from bid import Bid
from ask import Ask
from agent import BuyAgent, SellAgent, MarketMaker
from CDA import CDA
from AMM import AMM
from plot import *




budgets = [1, 20, 40, 60, 80, 100]
# budget in dollars
budget = 1
# separate budget for market maker (functionally infinity)
market_maker_budget = 10000
# probability between 0 and 1 whether an agent can make a trade in any given iteration
order_frequency = 1
# number of agents
num_agents = 100
# how many of these agents are bidders and how many are askers?
buy_sell_ratio = 0.5
# iterations of simulation
sim_length = 100
# number of simulations
num_sims = 50
# how many initial shares of the contract each agent starts with
initial_shares = 0
# regularizer for logarithmic scoring rule based market maker
beta = 10000

# mean and standard deviation for normal distribution to sample from for normal agents
mu, sigma = 0.5, 0.1
# number of bidders and sellers according to buy_sell_ratio
num_buy_agents = int(num_agents * buy_sell_ratio)
num_sell_agents = int(num_agents * (1 - buy_sell_ratio))


# some buyer agents and some seller agents, uniform valuations

# agents = [BuyAgent(i, random.random(), initial_shares, budget, order_frequency) for i in range(num_buy_agents)]
# agents += [SellAgent(i, random.random(), initial_shares, budget, order_frequency) for i in range(num_buy_agents, num_buy_agents + num_sell_agents)]

# some buyer agents and some seller agents, normal valuations

agents = [BuyAgent(i, np.random.normal(mu, sigma), initial_shares, budget, order_frequency) for i in range(num_buy_agents)]
agents += [SellAgent(i, np.random.normal(mu, sigma), initial_shares, budget, order_frequency) for i in range(num_buy_agents, num_buy_agents + num_sell_agents)]

# add market making agents individually
# last parameter for marketmaker agent is their learning rate

agents += [MarketMaker(101, np.random.normal(mu, sigma), initial_shares, 100000, order_frequency, 0)]
# agents += [MarketMaker(102, np.random.normal(mu, sigma), initial_shares, 100000, order_frequency, 0.1)]
# agents += [MarketMaker(103, np.random.normal(mu, sigma), initial_shares, 100000, order_frequency, 0.1)]





# true_valuations = [agent.value for agent in agents]


shares_traded = []
utilities = []



# define the continuous double auction
CDA = CDA(agents)
trade_volume = np.zeros(sim_length)
for i in range(num_sims):


    # some buyer agents and some seller agents, uniform valuations

    # agents = [BuyAgent(i, random.random(), initial_shares, budget, order_frequency) for i in range(num_buy_agents)]
    # agents += [SellAgent(i, random.random(), initial_shares, budget, order_frequency) for i in range(num_buy_agents, num_buy_agents + num_sell_agents)]

    # some buyer agents and some seller agents, normal valuations

    agents = [BuyAgent(i, np.random.normal(mu, sigma), initial_shares, budget, order_frequency) for i in range(num_buy_agents)]
    agents += [SellAgent(i, np.random.normal(mu, sigma), initial_shares, budget, order_frequency) for i in range(num_buy_agents, num_buy_agents + num_sell_agents)]

    # add market making agents individually
    # last parameter for marketmaker agent is their learning rate

    agents += [MarketMaker(101, np.random.normal(mu, sigma), initial_shares, 100000, order_frequency, 0)]
    # agents += [MarketMaker(102, np.random.normal(mu, sigma), initial_shares, 100000, order_frequency, 0.1)]
    # agents += [MarketMaker(103, np.random.normal(mu, sigma), initial_shares, 100000, order_frequency, 0.1)]


    CDA.agents = agents
    trade_volume_ = []
    for j in tqdm(range(sim_length)):
        CDA.iterate_timestep(j, trade_volume_, verbose=False)

    trade_volume = [sum(x) for x in zip(trade_volume, trade_volume_)]

    # generate an outcome
    binary_outcome = None
    outcome_probability = 0.5
    if random.random() < outcome_probability:
        binary_outcome = True
    else:
        binary_outcome = False





    CDA.calculate_returns(binary_outcome, budget, market_maker_budget, verbose=True)

    for agent in CDA.agents:
        if isinstance(agent, MarketMaker):
            utilities.append(agent.budget - market_maker_budget)
            shares_traded.append(agent.trades_executed)


    # CDA.reset_agents(initial_shares, budget, order_frequency)


print("utilities: ", utilities)
print("shares traded: ", shares_traded)


#
#
# line_chart(np.arange(0, sim_length),
#             trade_volume,
#             "CDA Trade Volume Over Time, with 1 MarketMaker",
#             x_label='# iterations',
#             y_label='# of Trades per Iteration',
#             file_name='trades_mm')
#
# line_chart(np.arange(0, sim_length),
#             np.cumsum(trade_volume),
#             "Cumulative CDA Trade Volume Over Time, with 1 MarketMaker",
#             x_label='# iterations',
#             y_label='Cumulative Trades',
#             file_name='cumsum_trades_mm')
#
#
# num_unique_traders = CDA.calculate_unique_traders()
# average_agent_utilities = CDA.calculate_average_agent_utility(include_market_makers=True)
# average_market_maker_utility = CDA.calculate_average_market_maker_utility()
#
# histogram(average_agent_utilities, "CDA Agent Utilities, with 1 MarketMaker", file_name='utility_mm')
# print("Total trades executed: " + str(sum([agent.trades_executed for agent in CDA.agents])))
# print("Total utility for market makers: " + str(average_market_maker_utility))
# print("Average utility for non-market-makers: " + str(sum(average_agent_utilities) / len(average_agent_utilities)))
# print("Number of traders participating in market: " + str(num_unique_traders))
#
#
#
# for agent in CDA.agents:
#     if isinstance(agent, MarketMaker):
#         y_labels = ['bid_price', 'ask_price']
#         mm_line_chart(np.arange(0, sim_length - 1),
#                     [agent.bid_price_history, agent.ask_price_history],
#                     y_labels,
#                     "Market Maker Pricing Spread Over Time",
#                     x_label='# iterations',
#                     y_label='price ($)',
#                     file_name='bid_ask_price_agent_' + str(agent.id))
