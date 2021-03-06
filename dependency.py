import numpy as np 
import pandas as pd
import reaction_direction as rd
import FBA as fb
import cut_reactions as cr
 
def init_dataset(file_input):

    df = pd.read_excel(file_input,index_col=0)
    rev = df.loc['reversible']
    df = df.drop('reversible',axis=0)
    # dict = pd.DataFrame(columns=['pos'],index=metabolites)
    return df,rev

def get_metabolites_in(df):

    metabolites_in =[]
    met_loop = ['coa','nad','nadp','adp','q8','h2o','h','atp','nadh','nadph','co2','pep']
    m_in = fb.feed_excel(filename='data/feed_list_metabolites.xlsx').tolist()
    print(m_in)
    for m in df.index:
        if m in met_loop or m in m_in:
            metabolites_in.append(m)
    print(metabolites_in)
    return metabolites_in


def init_positions(dict,df):

    metabolites = df.index.values
    for m in metabolites:
        if m in metabolites_in:
            dict.loc[m] = 0
        else:
            dict.loc[m] = -100
    return dict

def get_positions_rev(df,dict):

    to_update = True
    while to_update: 
        to_update = False 
        for r in df.columns:
            reacts = df.loc[:,r].loc[df[r]<0]
            products = df.loc[:,r].loc[df[r]>0]
            pos_prod_list = []
            pos_reac_list = []
            for p in products.index: 
                pos_prod_list.append(dict.loc[p].values[0])
            for s in reacts.index:
                pos_reac_list.append(dict.loc[s].values[0])
            if rev[r] >0:
                if np.all([p>=0 for p in pos_prod_list]):
                    for s in reacts.index:
                        if dict.loc[s].values[0]<0:
                            dict.loc[s] = max(pos_prod_list)+1
                            to_update = True
            if np.all([s>=0 for s in pos_reac_list]):
                for p in products.index:
                    if dict.loc[p].values[0]<0:
                        dict.loc[p] = max(pos_reac_list)+1
                        to_update = True

    return dict

def get_positions_onedirection(df,dict):

    to_update = True
    while to_update: 
        to_update = False 
        for r in df.columns: # iterate reactions
            if direction_array.loc[r].values[0] > 0:
                reacts = df.loc[:,r].loc[df[r]<0]
                products = df.loc[:,r].loc[df[r]>0]
            if direction_array.loc[r].values[0] <0: # if the reaction is in the inverse direction
                products = df.loc[:,r].loc[df[r]<0]
                reacts = df.loc[:,r].loc[df[r]>0]
            pos_prod_list = [] # lists for the current position/dependency of the metabolite
            pos_reac_list = []
            for p in products.index: 
                pos_prod_list.append(dict.loc[p].values[0]) # get the current position of dependency of the products
            for s in reacts.index:
                pos_reac_list.append(dict.loc[s].values[0]) # get position for the reactants
            if np.all([s>=0 for s in pos_reac_list]): # If all the reactants already have a dependency we can update the dependency of the product
                for p in products.index: # Iterate the products to update position
                    if dict.loc[p].values[0]<0: # If it's negative then it hasn't been updated yet
                        print(pos_reac_list)
                        if pos_reac_list: #if the list is not empty
                            print('TRUE')
                            dict.loc[p] = max(pos_reac_list)+1
                            to_update = True
    return dict


if __name__ == '__main__':
    
    file_input = 'ecoli_core_model.xlsx'
    file_FBA = 'data/FBA_undetermined_feed.xlsx'
    direction_array = rd.get_reaction_direction(file_FBA)
    df,rev = init_dataset('data/'+file_input)
    metabolites_in = get_metabolites_in(df)
    reactions_to_keep = cr.select_reactions(file_FBA)
    df = cr.cut_dataframe(df,reactions_to_keep)
    dict = pd.DataFrame(columns=['pos'],index=df.index.values)
    dict = init_positions(dict,df)
    df.to_excel('data/cut_model.xlsx')
    dict = get_positions_onedirection(df,dict)
    dict.to_excel('data/dependencies_cut_' + file_input)
