# Calculate the biomass

import pandas as pd
import numpy as np

data = pd.read_excel('ecoli_core_model.xls',sheet_name='Ecoli_core_S',index_col=0)
data_metabolites = pd.read_excel('ecoli_core_model.xls',sheet_name='metabolites',index_col=0)



data = data.loc[data['Biomass_Ecoli_core'] !=0]

def get_molarmass(molecule):
    atoms = {'C': 12, 'O': 16, 'P':31, 'S': 32, 'N': 14, 'H': 1}
    last = 0
    mass = 0
    for s in molecule:
        if s.isdigit():
            if last == 's':
                n = int(s)
            if last == 'd':
                n = int(str(n) + s)
            last = 'd'
        if not s.isdigit():
            if last == 's':
                mass += atoms[ato]*1
            if last == 'd':
                mass += atoms[ato]*n
            last = 's'
            ato = s
    if last == 's':
        mass += atoms[ato]*1
    if last == 'd':
        mass += atoms[ato]*n
    return mass



# Select only the metabolites in the biomass reaction
boo = []
for ind in data_metabolites.index:
    if ind in data.index:
        boo.append(True)
    else:
        boo.append(False)
data_metabolites = data_metabolites.loc[boo]


atoms = {'C': 12, 'O': 16, 'P':31, 'S': 32, 'N': 14, 'H': 1}

formula = data_metabolites[' formula        ']
stoich = data['Biomass_Ecoli_core']
mass = 0
for molecule in formula.index:
    molecular_mass = get_molarmass(formula[molecule])
    print(molecule,' = ',molecular_mass)
    mass += stoich[molecule]*molecular_mass

print(mass)