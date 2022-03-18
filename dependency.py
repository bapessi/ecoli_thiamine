import numpy as np 
import pandas as pd

 
def init_dataset(file_input):

    df = pd.read_excel(file_input,index_col=0)
    rev = df.loc['reversible']
    df = df.drop('reversible',axis=0)
    metabolites = df.index.values
    dict = pd.DataFrame(columns=['pos'],index=metabolites)
    return df,metabolites,dict,rev

def get_metabolites_in(df):

    metabolites_in =[]
    met_loop = ['coa','nad','nadp','adp','q8']
    m_in_exception = ['lac-D(e)']
    for m in df.index:
        if '(e)' in m and m not in m_in_exception:
            metabolites_in.append(m)
        if '[e]' in m and m not in m_in_exception:
            metabolites_in.append(m) 
        if m in met_loop:
            metabolites_in.append(m)
    return metabolites_in


def init_positions(dict):

    for m in metabolites:
        if m in metabolites_in:
            dict.loc[m] = 0
        else:
            dict.loc[m] = -100
    return dict

def get_positions(df,dict):

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

if __name__ == '__main__':
    
    file_input = 'ecoli_core_model.xlsx'
    df,metabolites,dict,rev = init_dataset(file_input)
    metabolites_in = get_metabolites_in(df)
    dict = init_positions(dict)
    dict = get_positions(df,dict)
    dict.to_excel('dependencies_' + file_input)
