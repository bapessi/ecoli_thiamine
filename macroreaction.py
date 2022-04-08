import subnetwork_new as sb 
import pandas as pd
import numpy as np
from os import path
import pickle

def get_macroreaction(efms):
    # m_A = pd.Series(['glc-D[e]','lac-D','succ','B','pyr'])
    m_A = pd.Series(['glc-D[e]','B','pyr'])
    r_exchange = ['GLC_ext','BIO','PYR_ext']
    for e in efms:
        efm = efms[e] 
        dict = {}
        for m in m_A:
            dict[m] = 0
        for r in efms.index.values:
            if r in r_exchange:
                print(r)
                pass
            else:
                for m in m_A:
                    dict[m] += efm[r]*df_rev.loc[m][r]
        print(dict)
    return dict

if __name__ == '__main__':
    print('START')
    df_rev = pd.read_excel('data/B_subnetwork.xlsx',index_col=0)

    if path.exists('data/efms.pkl'):
        f = open('data/efms.pkl','rb')
        efms = pickle.load(f) 
    else:
        efms = sb.get_efms(df_rev)     
        efms = pd.DataFrame(efms,index=df_rev.columns.values)
        efms.to_pickle('data/efms.pkl')
    print(efms)
    macro = get_macroreaction(efms)
    # efms.append(df_rev.columns.values)
