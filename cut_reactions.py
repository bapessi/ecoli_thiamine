import pandas as pd
import numpy as np 
def select_reactions(filename='data/FBA_ecoli_core_model.xlsx'):
    df_fba = pd.read_excel(filename,index_col=0)
    reactions_to_keep = []
    for r in df_fba.index.values:
        if df_fba.loc[r].values >1e-2:
            reactions_to_keep.append(r)
        if df_fba.loc[r].values <-1e-2:
            reactions_to_keep.append(r)
    return reactions_to_keep

def cut_dataframe(df,reactions_to_keep):
    df = df.loc[:,reactions_to_keep] 
    df = df.loc[~np.all(df==0,axis=1)]
    return df

def init_dataset(file_input):

    df = pd.read_excel(file_input,index_col=0)
    rev = df.loc['reversible']
    return df
def init_dataset(file_input):

    df = pd.read_excel(file_input,index_col=0)
    rev = df.loc['reversible']
    df = df.drop('reversible',axis=0)
    metabolites = df.index.values
    dict = pd.DataFrame(columns=['pos'],index=metabolites)
    return df,metabolites,dict,rev

   
if __name__ == '__main__':
    filename = 'data/FBA_ecoli_core_model.xlsx'
    reactions_to_keep = select_reactions(filename)
    file_input = 'ecoli_core_model.xlsx'
    df,metabolites,dict,rev = init_dataset('data/'+file_input)
    print(df)
    df = cut_dataframe(df,reactions_to_keep)
    print(df)
