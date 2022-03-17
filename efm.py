import numpy as np
import efmtool
import pandas as pd

if __name__ == '__main__':   
    N_matrix = pd.read_excel('network_teste.xlsx')

    # print(N_matrix)
    stoich = N_matrix.values
    # stoich = np.array([[ 1,  0,  0, -1,  0,  0,  0, -1],
    # [0,  1,  0,  0,  0, -1,  0,  0], 
    # [0,  0,  1,  0,  0,  0,  0, -1],
    # [0,  0,  0,  1, -1,  0,  0,  0],
    # [0,  0,  0,  1,  1,  1, -1,  0]
    # ])
    reactions = list(N_matrix.columns)

    efms = efmtool.calculate_efms(stoichiometry = stoich,reversibilities= np.array([0]*len(N_matrix.columns)),reaction_names=reactions,metabolite_names = ['c1','c2','c3','c4','c5'])
    print(efms)


