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
species_df['short_name'] = species_df.species
rate_df = pd.DataFrame({
    'rate_set_id': 1,
    'reaction_id': reaction_df.reaction_id,
    'reactants': reaction_df.reactants,
    'products': reaction_df.products,
    'rate': 1
})

initial_value_df = pd.DataFrame({
    'species_id': species_df.species_id,
    'short_name': species_df.species,
    'population': 10
})

initial_value_df.loc[0, 'population'] = 50


collector.run_and_store_ivp_sol(rate_set_id=1, ivp_id=3, species_df=species_df, 
                                rate_df=rate_df, initial_value_df=initial_value_df, num_points=100)

initial_value_df = pd.DataFrame({
    'species_id': species_df.species_id,
    'short_name': species_df.species,
    'population': 10
})

initial_value_df.loc[1, 'population'] = 50

collector.run_and_store_ivp_sol(rate_set_id=1, ivp_id=4, species_df=species_df, 
                                rate_df=rate_df, initial_value_df=initial_value_df, num_points=100)

collector.con.close()