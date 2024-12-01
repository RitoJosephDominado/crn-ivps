import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from parsing import extract_steady_state_df
from parsing import extract_rate_df
from ivp_solver import Solver
from ivp_data_collector import IVPDataCollector
# from ivp_data_collector import store_network_data
# from ivp_data_collector import run_and_store_ivp_sol
# from ivp_data_collector import run_and_store_n_ivp_sols
species_df = pd.read_csv('data/legewie_wild_species.csv')
reaction_df = pd.read_csv('data/legewie_wild_reactions.csv').fillna('empty')
reaction_df['reactants'] = reaction_df['reactant_text'].str.split('+')
reaction_df['products'] = reaction_df['product_text'].str.split('+')
print(reaction_df)
initial_value_df = pd.DataFrame({
    'species_id': species_df.species_id,
    'short_name': species_df.species,
    'population': 10
})

rate_df = pd.DataFrame({
    'reaction_id': reaction_df.reaction_id,
    'reactants': reaction_df.reactants,
    'products': reaction_df.products,
    'rate': reaction_df.bistable_rate
})
print(initial_value_df)

solver = Solver(initial_value_df, rate_df)
solver.solve(num_points=100, start_x=0, end_x=50)
result_df = solver.get_solution_df()
print(result_df)
print(result_df.columns)
fig, axes = plt.subplots(1, 2)

axes[0].plot()
axes[0].plot(result_df.Aa)
axes[0].plot(result_df.X)
# axes[0].plot(result_df.C3)
# axes[0].plot(result_df.C9)
axes[0].plot(result_df.C3a)
axes[0].plot(result_df.C9a)
# plt.show()

# initial_value_df[1, 'rate'] = 200
print('2nd initial value df')

initial_value_df.loc[1, 'population'] = 100
print(initial_value_df)
solver2 = Solver(initial_value_df, rate_df)
solver2.solve(num_points=100, start_x=0, end_x=50)
result_df = solver2.get_solution_df()
print(result_df)
print(result_df.columns)

axes[1].plot(result_df.Aa)
axes[1].plot(result_df.X)
# axes[1].plot(result_df.C3)
# axes[1].plot(result_df.C9)
axes[1].plot(result_df.C3a)
axes[1].plot(result_df.C9a)
plt.show()


# store_network()
# store_rate_set()
# store_ivp()
