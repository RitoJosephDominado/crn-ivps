import sqlite3

con = sqlite3.connect('crn.db')

con.execute('DROP TABLE IF EXISTS Species')
con.execute('DROP TABLE IF EXISTS Reactions')
con.execute('DROP TABLE IF EXISTS Networks')
con.execute('DROP TABLE IF EXISTS Reactants')
con.execute('DROP TABLE IF EXISTS Products')
con.execute('DROP TABLE IF EXISTS InitialValues')
con.execute('DROP TABLE IF EXISTS IVPs')
con.execute('DROP TABLE IF EXISTS Rates')
con.execute('DROP TABLE IF EXISTS RateSets')
con.execute('DROP TABLE IF EXISTS SpeciesPopulations')

con.execute('''
CREATE TABLE Networks(
            network_id INT PRIMARY KEY,
            name TEXT
            )
            ''')

con.execute('''
CREATE TABLE Reactions(
            network_id INT,
            reaction_id INT,
            FOREIGN KEY(network_id) REFERENCES Networks(network_id)
            PRIMARY KEY(network_id, reaction_id)
            )
            ''')

con.execute('''
CREATE TABLE Species(
            species_id INTEGER PRIMARY KEY,
            name TEXT,
            short_name TEXT UNIQUE
            )
''')

con.execute('''
CREATE TABLE Reactants(
            network_id INT,
            reaction_id INT,
            species_id INT,
            num INT DEFAULT 1,
            FOREIGN KEY(network_id) REFERENCES Networks(network_id),
            FOREIGN KEY(reaction_id) REFERENCES Reactions(reaction_id),
            FOREIGN KEY(species_id) REFERENCES Species(species_id)
            PRIMARY KEY(network_id, reaction_id, species_id)
            )
''')

con.execute('''
CREATE TABLE Products(
            network_id INT,
            reaction_id INT,
            species_id INT,
            num INT DEFAULT 1,
            FOREIGN KEY(network_id) REFERENCES Networks(network_id),
            FOREIGN KEY(reaction_id) REFERENCES Reactions(reaction_id),
            FOREIGN KEY(species_id) REFERENCES Species(species_id)
            PRIMARY KEY(network_id, reaction_id, species_id)
            )
''')


con.execute('''
CREATE TABLE RateSets(
            rate_set_id INTEGER PRIMARY KEY,
            network_id INT NOT NULL,
            FOREIGN KEY(network_id) REFERENCES Networks(network_id)
            )
''')



con.execute('''
CREATE TABLE IVPs(
            ivp_id INTEGER PRIMARY KEY,
            rate_set_id INT NOT NULL,
            num_points INT NOT NULL,
            time_step REAL NO NULL,
            FOREIGN KEY(rate_set_id) REFERENCES RateSets(rate_set_id)
            )
''')

con.execute('''
CREATE TABLE Rates(
            rate_set_id INT NOT NULL,
            reaction_id INT NOT NULL,
            rate REAL NOT NULL,
            FOREIGN KEY(rate_set_id) REFERENCES RateSets(rate_set_id),
            FOREIGN KEY(reaction_id) REFERENCES Reactions(reaction_id),
            PRIMARY KEY(rate_set_id, reaction_id)
            )
''')

con.execute('''
CREATE TABLE SpeciesPopulations(
            ivp_id INT NOT NULL,
            species_id INT NOT NULL,
            time INT NOT NULL,
            population REAL NOT NULL,
            FOREIGN KEY(ivp_id) REFERENCES IVPs(ivp_id),
            FOREIGN KEY(species_id) REFERENCES Species(species_id),
            PRIMARY KEY(ivp_id, species_id, time)
            )
''')

con.execute('''
CREATE TABLE InitialValues(
            ivp_id INT NOT NULL,
            species_id INT NOT NULL,
            population REAL NOT NULL,
            FOREIGN KEY(ivp_id) REFERENCES IVPs(ivp_id),
            FOREIGN KEY(species_id) REFERENCES Species(species_id),
            PRIMARY KEY(ivp_id, species_id)
            )
''')

# con.execute(''''
# CREATE TABLE Statuses(
#             status_id INT PRIMARY KEY,
#             ivp_id INT,
#             start_time TIME,
#             end_time TIME,
#             time_elapsed INT )
            
# ''')

con.execute('''
INSERT INTO Species (name, short_name) 
            SELECT "empty" AS "name", "empty" as "short_name"
            UNION ALL SELECT "Caspase 3", "C3"
            UNION ALL SELECT "Caspase 9", "C9"
            UNION ALL SELECT  "XIAP", "X"
            UNION ALL SELECT  "APAF1", "Aa"
            UNION ALL SELECT  "Activated Caspase 3", "C3a"
            UNION ALL SELECT  "Activated Caspase 9", "C9a"
            UNION ALL SELECT  "Activated Caspase 3 binded with XIAP", "C3aX"
            UNION ALL SELECT  "Activated Caspase 9 binded with XIAP", "C9aX"
            UNION ALL SELECT  "Caspase 9 binded with XIAP", "C9X"
            UNION ALL SELECT  "Caspase 9 binded with APAF1", "AaC9"
            UNION ALL SELECT  "Activated Caspase 9 binded with APAF1", "AaC9a"
            UNION ALL SELECT  "Caspase 9 binded with APAF1 and XIAP", "AaC9X"
            UNION ALL SELECT  "Activated Caspase 9 binded with APAF1 and XIAP", "AaC9aX"
''')



con.commit()
con.close()
