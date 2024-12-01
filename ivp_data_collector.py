import sqlite3
import pandas as pd
from parsing import extract_steady_state_df
from parsing import extract_rate_df
from ivp_solver import Solver
import numpy as np

class IVPDataCollector:
    def __init__(self, db_file):
        self.db_file = db_file
        self.con = sqlite3.connect(db_file)

    def store_network(self, network_id, reaction_df, network_name =''):
        con = self.con
        self.con.execute(f'''
        INSERT INTO Networks (network_id, name) VALUES ({network_id}, "{network_name}")
        ''')

        species_df = pd.read_sql_query('SELECT * FROM Species', con)
        print(species_df)
        species_mapping_dict = dict(zip(species_df['short_name'], species_df['species_id']))

        reaction_df['reactants_species_id'] = reaction_df['reactants'].apply(lambda x: [species_mapping_dict[shortname] for shortname in x])
        reaction_df['products_species_id'] = reaction_df['products'].apply(lambda x: [species_mapping_dict[shortname] for shortname in x])

        for i in range(reaction_df.shape[0]):
            reaction_df_row = reaction_df.iloc[i, :]

            self.con.execute(f'INSERT INTO Reactions(network_id, reaction_id)\
                        VALUES({network_id}, {i+1})')

            for reactant in reaction_df_row.reactants_species_id:
                con.execute(f'INSERT INTO Reactants(network_id, reaction_id, species_id)\
                        VALUES({network_id}, {i+1}, "{reactant}")')
                
            for product in reaction_df_row.products_species_id:
                con.execute(f'INSERT INTO Products(network_id, reaction_id, species_id)\
                        VALUES({network_id}, {i+1}, "{product}")')
                
        con.commit()
        # con.close()

    def store_rate_set(self, network_id, rate_set_id, rate_df):
        con = self.con
        self.con.execute(f'''
                         INSERT INTO RateSets (network_id, rate_set_id)
                         VALUES({network_id}, {rate_set_id})
                         ''')
        
        for i in range(rate_df.shape[0]):
            rate_df_row = rate_df.iloc[i, :]
            rate_set_id = rate_df_row.rate_set_id
            rate = rate_df_row.rate

            self.con.execute(f'INSERT INTO Rates(rate_set_id, reaction_id, rate)\
                        VALUES({rate_set_id}, {i+1}, {rate})')

        con.commit()
        con.close()
        # print(f'Done storing data from network {network_id}')
    
    def store_ivp(self, ivp_id, rate_set_id, num_points, time_step, initial_value_df):
        self.con.execute(
            f'''INSERT INTO IVPS(ivp_id, rate_set_id, num_points, time_step)
            VALUES({ivp_id}, {rate_set_id}, {num_points}, {time_step})
        ''')

        # self.con.execute(
        #     f'''INSERT INTO IVPS(ivp_id, rate_set_id, num_points, time_step)
        #     VALUES({ivp_id}, {rate_set_id}, {num_points}, {time_step})
        # ''')


    def store_species_populations(self, rate_set_id, ivp_id, rate_df, initial_value_df, num_points):
        self.con = sqlite3.connect(self.db_file)
        species_df = pd.read_sql_query('SELECT * FROM ')

        sol = Solver(initial_value_df, rate_df)
        sol.solve(num_points = num_points, start_x=0, end_x=num_points, method='Radau')
        result_df = sol.get_solution_df()
        result_df['time'] = result_df.index
        result_df = result_df.melt(var_name='short_name')

    def run_and_store_ivp_sol(self, rate_set_id, ivp_id, species_df, rate_df, initial_value_df, num_points):
        time_step = 1
        self.con.execute(f'INSERT INTO IVPs(ivp_id, rate_set_id, num_points, time_step)\
                VALUES({ivp_id}, {rate_set_id}, {num_points}, {time_step})')
        
        sol = Solver(initial_value_df, rate_df)    
        sol.solve(num_points = num_points, start_x=0, end_x=num_points, method='Radau')
        result_df = sol.get_solution_df()
        result_df['time'] = result_df.index
        
        result_df = result_df.melt(var_name='short_name', value_name='population', id_vars = 'time').\
            merge(species_df[['species_id', 'short_name']], on=['short_name', 'short_name'])
        insert_query = """
        INSERT INTO SpeciesPopulations(ivp_id, species_id, time, population)
        VALUES(?, ?, ?, ?)
        """
        res_list = [(ivp_id, x[0], x[1], x[2]) for x in zip(result_df.species_id, result_df.time, result_df.population)]
        
        self.con.executemany(insert_query, res_list)
        self.con.commit()
        # self.con.close()
        # self.con.commit()


    def run_and_store_n_ivp_sols(self, rate_set_id, rate_df, num_points, num_ivps):
        self.con = sqlite3.connect(self.db_file) 
        species_df = pd.read_sql_query('SELECT * FROM Species', self.con)
        # species_df = pd.read_csv('csvs/legewi_wild_species.csv', header=0)

        current_ivp_df = pd.read_sql_query('SELECT COUNT(*) as num FROM IVPs', self.con)
        current_ivp_id = int(current_ivp_df.num[0])

        ivp_id = current_ivp_id + 1
        for i in range(num_ivps):
            ivp_id += 1
            ivp_id = int(ivp_id)
            initial_value_df = species_df.copy(deep=True)
            # initial_value_df['population'] = np.repeat(0, 4) + np.random.randint(0, 1000, initial_value_df.shape[0] - 4)
            initial_value_df['population'] = np.concatenate([np.random.randint(0, 1000, 4), np.repeat(0, initial_value_df.shape[0] - 4)])
            self.run_and_store_ivp_sol(rate_set_id, ivp_id, species_df, rate_df, initial_value_df, num_points)
        # self.con.commit()
        # self.con.executemany(insert_query, res_list)
        # self.con.commit()
        
        self.con.close()
