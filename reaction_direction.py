import pandas as pd
import numpy as np

def get_reaction_direction(filename="data/FBA_ecoli_core_model.xlsx"):
    df = pd.read_excel(filename,index_col =0)
    direction_array = pd.DataFrame(np.ones(len(df)),index=df.index)
    for r in df.index:
        if df.loc[r].values[0] <0:
           direction_array.loc[r] = -1
    return direction_array


if __name__ == '__main__':
    direction_array = get_reaction_direction()
    print(direction_array)
