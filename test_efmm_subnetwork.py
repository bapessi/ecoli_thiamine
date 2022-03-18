import efmtool
import pandas as pd
import numpy as np

def get_efms(df):
    rev = df.loc['reversible'].to_numpy(int)
    print(rev)
    df = df.drop("reversible")
    efms = efmtool.calculate_efms(stoichiometry=df.to_numpy(),reversibilities=rev,reaction_names=df.columns.values,metabolite_names=df.index.values)
    return efms

filename = 'ecoli_core_model.xlsx'
df = pd.read_excel(filename,index_col=0)
m_accum = ['pyr','glc-D[e]']
list_index = []
for m in m_accum:
    list_index.append(np.where(df.index.values==m)[0][0])
# efms = get_efms(df)
print(list_index)
