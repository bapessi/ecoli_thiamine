import numpy as np 
import pandas as pd
import dependency
# This is a modification
def get_reactions(m,df):
    reactions = df.loc[m].loc[df.loc[m]!=0]
    return pd.Series(reactions.index.values)

def get_metabolites(r,df):
    metabolites = df[r].loc[df[r]!=0].index.values
    return pd.Series(metabolites)

def remove_checked(new,checked,actual,ignore=[],m_A=[]):
    remove = list(set(new)&set(checked))
    new = new.loc[~new.isin(checked)].loc[~new.isin(actual)]
    new = new.loc[~new.isin(ignore)].loc[~new.isin(m_A)]
    return new

def initiate_chain(m_init,df):
    r_init = get_reactions(m_init,df)
    return r_init

def get_reaction_chain(r_unchecked,df):

    m_unchecked = pd.Series(dtype='object') 
    m_checked = pd.Series(dtype='object') 
    r_checked = pd.Series(dtype='object') 

    while not r_unchecked.empty:
        for r in r_unchecked:
            m_new = get_metabolites(r,df)
            m_unchecked = pd.concat([m_unchecked,remove_checked(m_new,m_checked,m_unchecked,m_ignore,m_A)],ignore_index=True) 
            r_checked = pd.concat([r_checked,pd.Series([r])],ignore_index=True)
        r_unchecked = pd.Series(dtype='object') 

        for m in m_unchecked:
            r_new = get_reactions(m,df) 
            r_unchecked = pd.concat([r_unchecked,remove_checked(r_new,r_checked,r_unchecked)],ignore_index=True)
            m_checked = pd.concat([m_checked,pd.Series([m])],ignore_index=True)
        m_unchecked = pd.Series(dtype='object') 

    return r_checked,m_checked

if __name__ == '__main__':
    m_A = pd.Series(['pyr','glc-D[e]','lac-D[e]','gln-L','glu-L','oaa'])
    m_ignore = pd.Series(["coa",'adp','atp','h2o','h2o[e]',"h",'h[e]','nad','nadh','nadp','nadph','co2'])


    print('START')
    file_input = 'ecoli_core_model.xlsx'
    df,metabolites,dict,rev = dependency.init_dataset(file_input)

    m_init = 'pyr'
    r_init = initiate_chain(m_init,df)
    r_chain,m_checked = get_reaction_chain(r_init,df)
    print(r_chain)
    print("n of reactions: ",len(r_chain))
    print(len(set(r_chain)))
    df_reactions = pd.Series(df.columns.values)  
    print(df_reactions.loc[~df_reactions.isin(r_chain)])
