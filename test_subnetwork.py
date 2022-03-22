import numpy as np 
import pandas as pd
import dependency

m_A = ['pyr','glc-D[e]','lac-D[e]']
m_ignore = ["coa",'adp','atp','h2o','h2o[e]',"h",'h[e]','nad','nadh','nadp','nadph']

def get_reactions(m,df):
    reactions = df.loc[m].loc[df.loc[m]!=0]
    return list(reactions.index.values)

def get_metabolites(r,df):
    metabolites = df[r].loc[df[r]!=0].index.values
    return list(metabolites)

def remove_checked(new,checked,ignore=[],m_A=[]):

    remove = list(set(new)&set(checked))
    for r in remove:
        new.remove(r)
    for n in new:
        if n in ignore or n in m_A:
            new.remove(n)
    return new

def initiate_chain(m_init,df):
    r_init = []
    r = get_reactions(m_init,df)
    r_init = r_init + list(r)
    print(r_init)
    return r_init
def get_reaction_chain(r_unchecked,df):
    m_unchecked = []
    m_checked = []
    r_checked = []
    while r_unchecked:
        for r in r_unchecked:
            m_new = get_metabolites(r,df)
            m_new = remove_checked(m_new,m_checked,m_ignore)
            m_unchecked = m_unchecked + m_new
            r_checked.append(r)
            print(r)

        r_unchecked = []
        for m in m_unchecked:
            r_new = get_reactions(m,df) 
            r_new = remove_checked(r_new,r_checked)
            r_unchecked = r_unchecked + r_new
            m_checked.append(m)
            m_unchecked.remove(m)
        m_unchecked = []

    return r_checked

if __name__ == '__main__':

    print('START')
    file_input = 'ecoli_core_model.xlsx'
    df,metabolites,dict,rev = dependency.init_dataset(file_input)

    m_init = 'pyr'
    r_init = initiate_chain(m_init,df)
    r_chain = get_reaction_chain(r_init,df)
    print(r_chain)
    print("n of reactions: ",len(r_chain))
