import sqlite3 as sql
import pandas as pd
import numpy as np
from ivp_solver import Solver
from ivp_data_collector import IVPDataCollector

species_df = pd.read_csv('data/legewie_wild_species.csv')
reaction_df = pd.read_csv('data/legewie_wild_reactions.csv').fillna('empty')
reaction_df['reactants'] = reaction_df['reactant_text'].str.split('+')
reaction_df['products'] = reaction_df['product_text'].str.split('+')
collector = IVPDataCollector('crn.db')
print(reaction_df)
rate_df = pd.DataFrame({
    'rate_set_id': 1,
    'reaction_id': reaction_df.reaction_id,
    'rate': 1
})

collector.store_rate_set(network_id=1, rate_set_id=1, rate_df=rate_df)