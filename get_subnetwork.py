from chempy import Substance
import numpy as np
import efmtool
import pandas as pd
'''
Treat the core metabolism of e coli and returns a subnetwork according to the list on the spreadsheet reactions
'''
def get_molar_biomass():
    mass_balance= 0
    for m in bio_reaction.index.values:
        subs = Substance.from_formula(chemical[m])
        mass = subs.mass
        mass_balance += bio_reaction.loc[m]*mass
    return mass_balance

def select_subsystem(subsystem):

    df_list = df_reaction[' subSystem'].loc[df_reaction[' subSystem']==subsystem] # select list of reactions of the subsystem
    bool= [s in df_list.index.values for s in df_core.columns.values] # create a boolean array of reactions subsystem in core system
    df_subsystem = df_core.loc[:,bool] # from the core sheet select only reactions from the subsystem 
    df_return = df_subsystem.loc[~np.all(df_subsystem==0,axis=1)]
    if np.all(df_subsystem.loc['reversible']==0):
        rev = df_subsystem.loc['reversible']
        df_return = df_return.append(rev) 
        print(df_return)
    return df_return

def get_efms(df):
    import efmtool
    rev = df.loc['reversible'].values
    df = df.drop("reversible")
    efms = efmtool.calculate_efms(stoichiometry=df.to_numpy(),reversibilities=rev,reaction_names=df.columns.values,metabolite_names=df.index.values)
    return efms

def get_feasible(df):
    list_not_feasible =  []
    for m in df.index.values:
        if not np.any(df.loc[m].values[df.loc[m].values>0]):
            list_not_feasible.append(m)
        if not np.any(df.loc[m].values[df.loc[m].values<0]):
            list_not_feasible.append(m)
    list_not_feasible.remove('reversible')
    list_not_feasible = list_not_feasible

    return list_not_feasible 

def del_non_feasible(df,list_not_feasible):

    for m in list_not_feasible:
        df = df.drop(m)
    for r in df.columns.values:
        if not np.any(df.loc[:,r].values[df.loc[:,r].values!=0]):
            df = df.drop(r,axis=1)

    return df 


if __name__ == '__main__':

    filename = 'ecoli_core_model.xlsx'
    df_mass = pd.read_excel(filename,index_col=0,sheet_name='metabolites') 
    df_core = pd.read_excel(filename,index_col=0)
    df_reaction = pd.read_excel(filename,index_col=0,sheet_name='reactions') 
    bio_reaction = df_core['Biomass_Ecoli_core'].loc[df_core['Biomass_Ecoli_core']!=0]
    metabolites = df_core.index.values
    chemical = df_mass[' formula        '].dropna()
    # mass_balance = get_molar_biomass()

    subsystem_list = list(set(df_reaction[' subSystem'].values))
    subsystem_list.remove(np.nan)
    efms_list = []
    subsystem_list = ["Pyruvate Metabolism"]
    for subsystem in subsystem_list:
        df_subsystem = select_subsystem(subsystem) 
        list_not_feasible= get_feasible(df_subsystem)
        df_feasible = del_non_feasible(df_subsystem,list_not_feasible)
        # print(df_subsystem)
        efms = get_efms(df_feasible)
        print("SYSTEM ",subsystem)
        print(df_feasible)
        print(efms)
        # efms_list.append(efms)
