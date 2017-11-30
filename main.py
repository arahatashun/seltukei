# -*- coding: utf-8 -*-
# Author: Shun Arahata
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

def getStiffnerCounts(rib_distance,stiffner_distance):
    """
    :param rib_distance:リブの間隙
    :param stiffner_distance:スティフナーの距離
    """
    stiffner_counts=rib_distance//stiffner_distance
    return stiffner_counts


def gethe(hf):
    """
    hfを受け取りrivet重心位置計算によりheを返す
    :param hf:前桁高さ[mm]
    :return he:
    """
def calcsta625():
    sta625=625
    y=sm_df.ix[0][1]
    Sf=sm_df.ix[0][4]
    #print("Sf",Sf)
    Mf=sm_df.ix[0][5]
    #print("Mf",Mf)
    #print(getHf(685))
    """
    以下パラメーターの設定
    """
    stiffner_thickness=2.03#mm
    stiffner_bs1=65
    stiffner_bs2=20
    web_thickness=1.8
    web_distance=60
    hf=getHf(sta625+web_distance)
    rivet_web_stiffner_diameter=6.25
    tension_frange_thickness=
    """
    オブジェクト生成
    """
    stiffner=Stiffner(stiffner_thickness,stiffner_bs1,stiffner_bs2)
    web=Web(web_thickness,hf,web_thickness)
    rivet_web_stiffner=RivetWebStiffner(rivet_web_stiffner_diameter,stiffner,web)
    """
    csv書き出し
    """
    with open('sta625.csv','a') as f:
        writer = csv.writer(f)
        web.makeheader(f)
        web.makerow(f,Sf,he)






if __name__ == '__main__':
    calcsta625()
