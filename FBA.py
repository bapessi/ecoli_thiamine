import numpy as np
import pandas as pd
from scipy.optimize import linprog

def get_matrix(filename):

    df = pd.read_excel(filename,index_col=0)
    rev = df.loc['reversible',:].values
    df = df.drop('reversible')
    feed_list = feed_excel() 
    Aeq = df.to_numpy(na_value=0)
    beq = np.zeros(Aeq.shape[0]) #  
    c = np.zeros(Aeq.shape[1])
    return df,Aeq,beq,c,rev,feed_list

def get_bounds(rev):
    bounds = []
    b_max = 1e6 #y1
    for r in rev:
        if r == 1:
            bounds.append((-b_max,b_max))
        elif r==0:
            bounds.append((0,b_max))
        else:
            print("error with reversible array")
    return bounds

def correct_feed(feed_list,bounds,c,r_max):
    feed_list = []
    for reaction,i in zip(df.columns,range(len(df.columns))):
        if reaction in feed_list:
            print(reaction)
            bounds[i] = (-1e5,1e5)
        if reaction == r_max:
            print('max reaction: ',reaction)
            c[i] = -1
    return bounds,c

def feed_excel(filename = 'data/feed_list.xlsx'):
    feed_list = pd.read_excel(filename,header=None).to_numpy()
    feed_list=feed_list.flatten()
    return feed_list

if __name__ == '__main__':
    filename = 'ecoli_core_model' 
    r_max = 'Biomass_Ecoli_core'
    fileinput = 'data/' + filename + '.xlsx' 
    fileoutput = 'data/' + 'FBA_' + filename + '.xlsx'
    df,Aeq,beq,c,rev,feed_list = get_matrix(fileinput)
    bounds = get_bounds(rev)
    bounds,c = correct_feed(feed_list,bounds,c,r_max)
    res = linprog(c,A_eq=Aeq,b_eq=beq,bounds=bounds,method="interior-point",options={'tol':1e-7,'maxiter':10000})
    print("max flux ", max(res.x))
    print("min flux", min(res.x))
    flux =pd.Series(res.x,index=df.columns)
    print("Flux biomass: ",flux[r_max])
    print("Flux glucose: ",flux['EX_glc(e)'])
    flux.to_excel(fileoutput)

