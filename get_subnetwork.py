from chempy import Substance
import efmtool
import pandas as pd

def get_molar_biomass():
    mass_balance= 0
    for m in bio_reaction.index.values:
        subs = Substance.from_formula(chemical[m])
        mass = subs.mass
        mass_balance += bio_reaction.loc[m]*mass
    return mass_balance

if __name__ == '__main__':

    filename = 'ecoli_core_model.xlsx'
    df_mass = pd.read_excel(filename,index_col=0,sheet_name='metabolites') 
    df = pd.read_excel(filename,index_col=0)
    bio_reaction = df['Biomass_Ecoli_core'].loc[df['Biomass_Ecoli_core']!=0]
    metabolites = df.index.values
    chemical = df_mass[' formula        '].dropna()
    mass_balance = get_molar_biomass()
    print(mass_balance)

