import efmtool
from os import path
import pandas as pd
import numpy as np
import pickle
def get_efms(df):
    rev = df.loc['reversible'].to_numpy(int)
    df = df.drop("reversible")
    efms = efmtool.calculate_efms(stoichiometry=df.to_numpy(),reversibilities=rev,reaction_names=df.columns.values,metabolite_names=df.index.values)
    return efms

filename = 'ecoli_core_model.xlsx'
df = pd.read_excel(filename,index_col=0)
m_accum = ['pyr','glc-D[e]']
list_index_pyr = []
list_index_glc = []
# for m in m_accum:
#     list_index.append(np.where(df.index.values==m)[0][0])
# efms = get_efms(df)


list_reaction_pyr = df.loc['pyr'].loc[df.loc['pyr'] !=0].index.values
list_reaction_glc = df.loc['glc-D[e]'].loc[df.loc['glc-D[e]'] !=0].index.values

print(list_reaction_pyr)
print(list_reaction_glc)

for r in list_reaction_pyr:
    list_index_pyr.append(np.where(df.columns.values==r)[0][0])
for r in list_reaction_glc:
    list_index_glc.append(np.where(df.columns.values==r)[0][0])


print(list_index_pyr)

'''
Checking if the reactions are present in all EFMs
'''

# if path.exists('TemporaryFiles/efms.pkl'):
#     f = open('TemporaryFiles/efms.pkl','rb')
#     efms = pickle.load(f)
#     f.close()
# else:
#     efms = get_efms(df)
#     f = open('TemporaryFiles/efms.pkl','wb')
#     pickle.dump(efms,f)
#     f.close()

# print(len(efms.T))
# reactions_present = []
# for index in list_index_pyr:
#    reactions_present.append(np.where(efms[index]!=0)[0])

# efmInAllReactions = []
# j = 0
# for i in range(len(efms.T)):
#     bool = False
#     for re_list in reactions_present:
#         if not i in re_list:
#             bool = True
#     if bool:
#         j += 1
#         print(j)

