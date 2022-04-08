import numpy as np
import efmtool
import pandas as pd
import reaction_direction as rd
import dependency_nocut as dp
import cut_reactions as cr
 
def init_dataset(file_input):

    df = pd.read_excel(file_input,index_col=0)
    df = df.drop('reversible',axis=0)
    return df

def get_reaction_chain(r_unchecked,df):
    m_unchecked = pd.Series(dtype='object') 
    m_checked = pd.Series(dtype='object') 
    r_checked = pd.Series(dtype='object') 
    while not r_unchecked.empty:
        for r in r_unchecked:
            m_new = get_metabolites(r,df)
            print('reaction: ',r)
            m_unchecked = pd.concat([m_unchecked,remove_checked(m_new,m_checked,m_unchecked,m_ignore,m_A)],ignore_index=True) 
            print('new metabolites: ',m_unchecked.values)
            r_checked = pd.concat([r_checked,pd.Series([r])],ignore_index=True)
        r_unchecked = pd.Series(dtype='object') 

        for m in m_unchecked:
            r_new = get_reactions(m,df) 
            r_unchecked = pd.concat([r_unchecked,remove_checked(r_new,r_checked,r_unchecked)],ignore_index=True)
            print('metabolite :',m)
            print('new reactions: ',r_unchecked.values)
            m_checked = pd.concat([m_checked,pd.Series([m])],ignore_index=True)
        m_unchecked = pd.Series(dtype='object') 
        print('--NEW ITERATION--')
    print('--END--')
    return r_checked,m_checked

def get_reactions(m,df): # Select the reactions where the metabolite is a product 
    reactions = df.loc[m].loc[df.loc[m]!=0]
    for r in reactions.index.values:
        reactions[r] = direction_array.loc[r]*reactions[r]
        if reactions[r] <0:
            reactions = reactions.drop(r)
    return pd.Series(reactions.index.values)

def get_metabolites(r,df): # Select metabolites that are reactants from that reaction

    if direction_array.loc[r].values[0] < 0:
        metabolites = df[r].loc[df[r]>0].index.values
    if direction_array.loc[r].values[0] > 0:
        metabolites = df[r].loc[df[r]<0].index.values
    return pd.Series(metabolites)

def remove_checked(new,checked,actual,ignore=[],m_A=[]):
    remove = list(set(new)&set(checked))
    new = new.loc[~new.isin(checked)].loc[~new.isin(actual)]
    new = new.loc[~new.isin(ignore)].loc[~new.isin(m_A)]
    return new

def get_efms(df):
    try:
        rev = df.loc['reversible'].to_numpy(int)
        df = df.drop("reversible")
    except:
        rev = np.zeros(len(df.columns),dtype=int)
    efms = efmtool.calculate_efms(stoichiometry=df.to_numpy(),reversibilities=rev,reaction_names=df.columns.values,metabolite_names=df.index.values)
    return efms

def reverse_reactions(df,direction_array):
    df_rev = pd.DataFrame(index=df.index)
    for r in df.columns.values:
        if direction_array.loc[r].values[0] <0:
            df_rev[r] =-1*df[r] 
        else:
            df_rev[r] = df[r]
    return df_rev

def compare_subnetworks():
    df1 = pd.read_excel('data/B_subnetwork.xlsx',index_col=0)
    df2 = pd.read_excel('data/pyr_subnetwork.xlsx',index_col=0)
    for r in df1.columns.values:
        if r in df2.columns.values:
            print('estah dentro: ',r)
        if r not in df2.columns.values:
            print('estah fora:  ',r)

if __name__ =='__main__':

    m_A = pd.Series(['glc-D[e]','lac-D','succ','B'])
    # m_ignore = pd.Series(["coa",'adp','atp','h2o','h2o[e]',"h",'h[e]','nad','nadh','nadp','nadph','co2','pi'])
    m_ignore = pd.Series(["coa",'adp','atp','h2o','h2o[e]',"h",'h[e]','nad','nadh','nadp','nadph','co2','pi','pyr','B','glc-D[e]'])
    file_FBA = 'data/FBA_undetermined_feed_biomass.xlsx'
    file_input = 'data/ecoli_core_model_biomass.xlsx'
    direction_array = rd.get_reaction_direction(file_FBA)
    reactions_to_keep = cr.select_reactions(file_FBA)
    df = init_dataset(file_input)
    df = cr.cut_dataframe(df,reactions_to_keep)
    m_in_loop = dp.get_metabolites_in(df)
    m_init = 'B'
    r_init = get_reactions(m_init,df) # Reactions containing 
    r_chain,m_checked = get_reaction_chain(r_init,df)
    df = df[r_chain]
    df = df.loc[~np.all(df==0,axis=1)] # Eliminate metabolites not participating in these reactions
    df_rev = reverse_reactions(df,direction_array) # Change the stoichiometry based on the direction_array
    df_rev = df_rev.loc[~df_rev.index.isin(m_ignore)]
    # df_rev.to_excel('data/'+m_init +'_subnetwork2.xlsx')
    # df_rev = pd.read_excel('data/B_subnetwork.xlsx',index_col=0)
    df_rev = pd.read_excel('data/B_subnetwork2.xlsx',index_col=0)
    efms = get_efms(df_rev)
    efms = list(efms.T)
    efms.append(df_rev.columns.values)
    print(np.array(efms).T)
