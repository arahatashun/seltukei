# -*- coding: utf-8 -*-
# Author: Shun Arahata
import pandas as pd
import numpy as np
import csv
from  scipy import interpolate
from frange import Frange
from stiffner import Stiffner
from tension_frange import TensionFrange
from compression_frange import CompressionFrange
from web  import Web
from rivet_web_stiffner import RivetWebStiffner


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


def getHe(hf: float,upper: Frange,lower: Frange) ->float :
    """
    hfを受け取りrivet重心位置計算によりheを返す
    :param hf:前桁高さ[mm]
    :return he:桁フランジ断面重心距離
    """
    he = hf-upper.getCenterOfGravity()-lower.getCenterOfGravity()
    return he


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
    stiffner_thickness=2.29#mm
    stiffner_bs1=40
    stiffner_bs2=30
    web_thickness=1.8
    web_distance=80
    hf=getHf(sta625+web_distance)
    rivet_web_stiffner_diameter= 6.25
    tension_frange_thickness = 5
    tension_frange_bottom = 45
    tension_frange_height = 40
    compression_frange_thickness = 6.0
    compression_frange_bottom = 45
    compression_frange_height = 40
    """
    オブジェクト生成
    """
    stiffner=Stiffner(stiffner_thickness,stiffner_bs1,stiffner_bs2)
    web=Web(web_thickness,getHf(sta625),web_distance)
    rivet_web_stiffner=RivetWebStiffner(rivet_web_stiffner_diameter,stiffner,web)
    tension_frange=TensionFrange(tension_frange_thickness,tension_frange_bottom,tension_frange_height)
    compression_frange=CompressionFrange(compression_frange_thickness,compression_frange_bottom,compression_frange_height)
    he=getHe(hf,tension_frange,compression_frange)
    #print("he",he)
    """
    csv書き出し
    """

    with open('sta625.csv','w') as f:
        writer = csv.writer(f)
        web.makeheader(writer)
        web.makerow(writer,Sf,he)
        stiffner.makeheader(writer)
        stiffner.makerow(writer,he,web_distance,web_thickness)
        compression_frange.makeheader(writer)
        compression_frange.makerow(writer,Mf,he,web_thickness)









if __name__ == '__main__':
    calcsta625()
