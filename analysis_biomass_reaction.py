from chempy import Substance
import numpy as np
import pandas as pd

def get_molar_biomass():
    mass_balance = 0
    mass_products = 0
    mass_reactants = 0
    atoms = {}
    atoms_list = []
    for m in biomass_reaction.index.values:
        subs = Substance.from_formula(chemical[m])
        atoms_list.extend(subs.composition.keys())
        mass = subs.mass
        mass_balance += biomass_reaction.loc[m]*mass

        if biomass_reaction.loc[m] >0:
            mass_products += biomass_reaction.loc[m]*mass
        if biomass_reaction.loc[m] <0:
            mass_reactants += biomass_reaction.loc[m]*mass

    atoms_list = list(set(atoms_list))
    atom_name = {15:'P',7:'N',8:'O',16:"S",6:"C",1:"H"}

    for a in atoms_list:
        atoms[a] = 0
    for m in biomass_reaction.index.values:
        subs = Substance.from_formula(chemical[m])
        for atom in subs.composition.keys():
            atoms[atom] += biomass_reaction.loc[m]*subs.composition[atom]
            # print('n of ',atom_name[atom],'atoms',atoms[atom])
    for atom in atoms.keys():
        print(atom_name[atom],atoms[atom])
    return mass_balance,mass_products,mass_reactants

def iterate_all_reactions(df_core,df_mass):
    for reac in df_core.columns.values:
        print(reac)
        biomass_reaction = df_core[reac].loc[df_core[reac]!=0]
        metabolites = df_core.index.values
        chemical = df_mass[' formula        '].dropna()
        mass_balance = get_molar_biomass()
        print(mass_balance)


if __name__ == '__main__':

    filename = 'ecoli_core_model.xlsx'
    df_mass = pd.read_excel(filename,index_col=0,sheet_name='metabolites') 
    df_core = pd.read_excel(filename,index_col=0)
    df_core = df_core.drop("reversible")
    df_reaction = pd.read_excel(filename,index_col=0,sheet_name='reactions') 
    reac = 'Biomass_Ecoli_core'
    biomass_reaction = df_core[reac].loc[df_core[reac]!=0]
    metabolites = df_core.index.values
    chemical = df_mass[' formula        '].dropna()
    mass_balance,mass_products,mass_reactants = get_molar_biomass()
    print(mass_balance)
