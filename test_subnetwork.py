import numpy as np 
import pandas as pd
import dependency
# This is a modification
m_A = pd.Series(['glc-D[e]','lac-D[e]'])
m_ignore = pd.Series(["coa",'adp','atp','h2o','h2o[e]',"h",'h[e]','nad','nadh','nadp','nadph','co2'])

def get_reactions(m,df):
    reactions = df.loc[m].loc[df.loc[m]!=0]
    return pd.Series(reactions.index.values)

def get_metabolites(r,df):
    metabolites = df[r].loc[df[r]!=0].index.values
    return pd.Series(metabolites)

def remove_checked(new,checked,actual,ignore=[],m_A=[]):
    print('antes ', new)
    remove = list(set(new)&set(checked))
    for r in remove:
        new.remove(r)
    for n in new:
        if n in ignore or n in m_A or n in actual:
            new.remove(n)
    print('depois ', new)
    return new

def initiate_chain(m_init,df):
    r_init = get_reactions(m_init,df)
    return r_init

def get_reaction_chain(r_unchecked,df):
    m_unchecked = []
    m_checked = []
    r_checked = []
    while r_unchecked:
        for r in r_unchecked:
            m_new = get_metabolites(r,df)
            m_unchecked = m_unchecked + remove_checked(m_new.copy(),m_checked.copy(),m_unchecked.copy(),m_ignore.copy(),m_A.copy())
            r_checked.append(r)

        r_unchecked = []
        for m in m_unchecked:
            r_new = get_reactions(m,df) 
            r_unchecked = r_unchecked + remove_checked(r_new.copy(),r_checked.copy(),r_unchecked.copy())
            m_checked.append(m)
        m_unchecked = []

    return r_checked,m_checked

if __name__ == '__main__':

    print('START')
    file_input = 'ecoli_core_model.xlsx'
    df,metabolites,dict,rev = dependency.init_dataset(file_input)

    m_init = 'pyr'
    r_init = initiate_chain(m_init,df)
    print('n of r init: ', len(r_init))
    r_chain,m_checked = get_reaction_chain(r_init,df)
    print(r_chain)
    print("n of reactions: ",len(r_chain))
    print(len(set(r_chain)))

