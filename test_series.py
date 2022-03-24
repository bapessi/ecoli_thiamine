import pandas as pd
import numpy as np
import dependency

file_input = 'ecoli_core_model.xlsx'
m_ignore = pd.Series(["coa",'adp','atp','h2o','h2o[e]',"h",'h[e]','nad','nadh','nadp','nadph','co2'])
m_test = pd.Series(["coa",'adp','co2'])
m_remove = pd.Series(['atp','adp'])
df,metabolites,dict,rev = dependency.init_dataset(file_input)

# for m in m_ignore:
#     if np.any(m_test.isin([m])):
#       m_ignore  

print(m_ignore.loc[~m_ignore.isin(m_test)])
m_ignore = m_ignore.loc[~m_ignore.isin(m_test)]
m_ignore = m_ignore.loc[~m_ignore.isin(m_remove)]
print(m_ignore)

# m_unchecked = pd.Series(dtype='object') 
# if m_unchecked.empty:
#     print('empty')
#     m_unchecked = pd.concat([m_unchecked,pd.Series(['atp'])])
# print(m_unchecked)
