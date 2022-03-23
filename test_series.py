import pandas as pd
import numpy as np
import dependency

file_input = 'ecoli_core_model.xlsx'
m_ignore = pd.Series(["coa",'adp','atp','h2o','h2o[e]',"h",'h[e]','nad','nadh','nadp','nadph','co2'])
m_test = pd.Series(["coa",'adp','co2'])
df,metabolites,dict,rev = dependency.init_dataset(file_input)
for m in m_ignore:
    print(m)
    print(np.any(m_test.isin([m])))

print(m_ignore.loc[m_ignore.isin(m_test)])
