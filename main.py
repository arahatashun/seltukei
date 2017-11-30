# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from  scipy import interpolate

sm_df=pd.read_csv("SandM.csv")

def getHf(sta):
    """
    sta hoge における前桁高さHfを返す
    """
    x=np.array([625,5000])
    y=np.array([320,130])
    f = interpolate.interp1d(x, y,kind='linear')
    hf=f(sta)
    return hf

def calcsta625():
    y=sm_df.ix[0][1]
    Sf=sm_df.ix[0][4]
    print("Sf",Sf)
    Mf=sm_df.ix[0][5]
    print("Mf",Mf)
    print(getHf(685))








if __name__ == '__main__':
    calcsta625()
