# -*- coding: utf-8 -*-
# Author: Shun Arahata,Hirotaka Kondo
import pandas as pd
import numpy as np
import csv
from  scipy import interpolate
from flange import Flange
from stiffener import Stiffener
from tension_flange import TensionFlange
from compression_flange import CompressionFlange
from web import Web
from rivet_web_stiffener import RivetWebStiffener
from rivet_web_flange import RivetWebFlange

sm_df = pd.read_csv("SandM.csv")


def getHf(sta):
    """
    sta hoge における前桁高さHfを返す
    """
    x = np.array([625, 5000])
    y = np.array([320, 130])
    f = interpolate.interp1d(x, y, kind='linear')
    hf = f(sta)
    return hf


def getStiffnerCounts(rib_distance, stiffner_distance):
    """
    :param rib_distance:リブの間隙
    :param stiffner_distance:スティフナーの距離
    """
    stiffner_counts = rib_distance // stiffner_distance
    return stiffner_counts


def getHe(hf: float, upper: Flange, lower: Flange) -> float:
    """
    hfを受け取りrivet重心位置計算によりheを返す
    :param hf:前桁高さ[mm]
    :return he:桁フランジ断面重心距離
    """
    he = hf - upper.getCenterOfGravity() - lower.getCenterOfGravity()
    return he


he_array = []
qmax_array = []


def calcsta625():
    sta = 625
    y = sm_df.ix[0][1]
    Sf = sm_df.ix[0][4]
    # print("Sf",Sf)
    Mf = sm_df.ix[0][5]
    # print("Mf",Mf)
    # print(getHf(685))
    """
    以下パラメーターの設定
    """
    stiffner_thickness = 1.27  # mm
    stiffner_bs1 = 40
    stiffner_bs2 = 30
    web_thickness = 1.80
    web_distance = 80  # stiffener 間隔でもある
    hf = getHf(sta + web_distance)
    tension_frange_thickness = 6.0
    tension_frange_bottom = 50
    tension_frange_height = 40
    compression_frange_thickness = 6.0
    compression_frange_bottom = 45
    compression_frange_height = 40
    rivet_web_stiffner_diameter = 6.35  # DD8
    rivet_web_frange_N = 2
    rivet_web_frange_D = 6.35
    rivet_web_pdratio = 6
    """
    オブジェクト生成
    """
    stiffener = Stiffener(stiffner_thickness, stiffner_bs1, stiffner_bs2)
    web = Web(web_thickness, getHf(sta), web_distance)
    rivet_web_stiffener = RivetWebStiffener(rivet_web_stiffner_diameter, stiffener, web)
    tension_frange = TensionFrange(tension_frange_thickness, tension_frange_bottom, tension_frange_height)
    compression_frange = CompressionFlange(compression_frange_thickness, compression_frange_bottom,
                                           compression_frange_height)
    he = getHe(hf, tension_frange, compression_frange)
    rivet_web_flange = RivetWebFlange(rivet_web_frange_D, rivet_web_pdratio, rivet_web_frange_N, web)
    # print("he",he)
    he_array.append(he)
    """
    csv書き出し
    """

    with open('sta625.csv', 'w', encoding='UTF-8') as f:
        writer = csv.writer(f)
        web.makeheader(writer)
        web.makerow(writer, Sf, he)
        stiffener.makeheader(writer)
        stiffener.makerow(writer, he, web_distance, web_thickness)
        compression_frange.makeheader(writer)
        compression_frange.makerow(writer, Mf, he, web_thickness)
        tension_frange.makeheader(writer)
        tension_frange.makerow(writer, Mf, he, web_thickness)
        rivet_web_stiffener.makeheader(writer)
        rivet_web_stiffener.makerow(writer, Sf, he, web_distance)
        rivet_web_flange.makeheader(writer)
        rivet_web_flange.makerow(writer, Sf, he)


def calcsta1000():
    sta = 1000
    y = sm_df.ix[1][1]
    Sf = sm_df.ix[1][4]
    # print("Sf",Sf)
    Mf = sm_df.ix[1][5]
    # print("Mf",Mf)
    # print(getHf(685))
    """
    以下パラメーターの設定
    """
    stiffner_thickness = 1.27  # mm
    stiffner_bs1 = 30
    stiffner_bs2 = 30
    web_thickness = 1.60
    web_distance = 80  # stiffener 間隔でもある
    hf = getHf(sta + web_distance)
    tension_frange_thickness = 6.0
    tension_frange_bottom = 40
    tension_frange_height = 40
    compression_frange_thickness = 6.0
    compression_frange_bottom = 45
    compression_frange_height = 40
    rivet_web_stiffner_diameter = 6.35  # DD8
    rivet_web_frange_N = 2
    rivet_web_frange_D = 6.35
    rivet_web_pdratio = 6
    """
    オブジェクト生成
    """
    stiffener = Stiffener(stiffner_thickness, stiffner_bs1, stiffner_bs2)
    web = Web(web_thickness, getHf(sta), web_distance)
    rivet_web_stiffener = RivetWebStiffener(rivet_web_stiffner_diameter, stiffener, web)
    tension_frange = TensionFrange(tension_frange_thickness, tension_frange_bottom, tension_frange_height)
    compression_frange = CompressionFlange(compression_frange_thickness, compression_frange_bottom,
                                           compression_frange_height)
    he = getHe(hf, tension_frange, compression_frange)
    rivet_web_flange = RivetWebFlange(rivet_web_frange_D, rivet_web_pdratio, rivet_web_frange_N, web)
    # print("he",he)
    he_array.append(he)
    """
    csv書き出し
    """

    with open('sta1000.csv', 'w', encoding='UTF-8') as f:
        writer = csv.writer(f)
        web.makeheader(writer)
        web.makerow(writer, Sf, he)
        stiffener.makeheader(writer)
        stiffener.makerow(writer, he, web_distance, web_thickness)
        compression_frange.makeheader(writer)
        compression_frange.makerow(writer, Mf, he, web_thickness)
        tension_frange.makeheader(writer)
        tension_frange.makerow(writer, Mf, he, web_thickness)
        rivet_web_stiffener.makeheader(writer)
        rivet_web_stiffener.makerow(writer, Sf, he, web_distance)
        rivet_web_flange.makeheader(writer)
        rivet_web_flange.makerow(writer, Sf, he)


def calcsta1500():
    sta = 1500
    y = sm_df.ix[2][1]
    Sf = sm_df.ix[2][4]
    # print("Sf",Sf)
    Mf = sm_df.ix[2][5]
    # print("Mf",Mf)
    # print(getHf(685))
    """
    以下パラメーターの設定
    """
    stiffner_thickness = 1.27  # mm
    stiffner_bs1 = 25
    stiffner_bs2 = 20
    web_thickness = 1.27
    web_distance = 70  # stiffener 間隔でもある
    hf = getHf(sta + web_distance)
    tension_frange_thickness = 6.0
    tension_frange_bottom = 40
    tension_frange_height = 40
    compression_frange_thickness = 6.0
    compression_frange_bottom = 45
    compression_frange_height = 40
    rivet_web_stiffner_diameter = 6.35  # DD8
    rivet_web_frange_N = 2
    rivet_web_frange_D = 6.35
    rivet_web_pdratio = 6
    """
    オブジェクト生成
    """
    stiffener = Stiffener(stiffner_thickness, stiffner_bs1, stiffner_bs2)
    web = Web(web_thickness, getHf(sta), web_distance)
    rivet_web_stiffener = RivetWebStiffener(rivet_web_stiffner_diameter, stiffener, web)
    tension_frange = TensionFrange(tension_frange_thickness, tension_frange_bottom, tension_frange_height)
    compression_frange = CompressionFlange(compression_frange_thickness, compression_frange_bottom,
                                           compression_frange_height)
    he = getHe(hf, tension_frange, compression_frange)
    rivet_web_flange = RivetWebFlange(rivet_web_frange_D, rivet_web_pdratio, rivet_web_frange_N, web)
    # print("he",he)
    he_array.append(he)
    """
    csv書き出し
    """

    with open('sta1500.csv', 'w', encoding='UTF-8') as f:
        writer = csv.writer(f)
        web.makeheader(writer)
        web.makerow(writer, Sf, he)
        stiffener.makeheader(writer)
        stiffener.makerow(writer, he, web_distance, web_thickness)
        compression_frange.makeheader(writer)
        compression_frange.makerow(writer, Mf, he, web_thickness)
        tension_frange.makeheader(writer)
        tension_frange.makerow(writer, Mf, he, web_thickness)
        rivet_web_stiffener.makeheader(writer)
        rivet_web_stiffener.makerow(writer, Sf, he, web_distance)
        rivet_web_flange.makeheader(writer)
        rivet_web_flange.makerow(writer, Sf, he)


def calcsta2000():
    sta = 2000
    y = sm_df.ix[3][1]
    Sf = sm_df.ix[3][4]
    # print("Sf",Sf)
    Mf = sm_df.ix[3][5]
    # print("Mf",Mf)
    # print(getHf(685))
    """
    以下パラメーターの設定
    """
    stiffner_thickness = 1.27  # mm
    stiffner_bs1 = 25
    stiffner_bs2 = 18
    web_thickness = 1.27
    web_distance = 70  # stiffener 間隔でもある
    hf = getHf(sta + web_distance)
    tension_frange_thickness = 6.0
    tension_frange_bottom = 40
    tension_frange_height = 40
    compression_frange_thickness = 5.5
    compression_frange_bottom = 40
    compression_frange_height = 40
    rivet_web_stiffner_diameter = 6.35  # DD8
    rivet_web_frange_N = 2
    rivet_web_frange_D = 6.35
    rivet_web_pdratio = 6
    """
    オブジェクト生成
    """
    stiffener = Stiffener(stiffner_thickness, stiffner_bs1, stiffner_bs2)
    web = Web(web_thickness, getHf(sta), web_distance)
    rivet_web_stiffener = RivetWebStiffener(rivet_web_stiffner_diameter, stiffener, web)
    tension_frange = TensionFrange(tension_frange_thickness, tension_frange_bottom, tension_frange_height)
    compression_frange = CompressionFlange(compression_frange_thickness, compression_frange_bottom,
                                           compression_frange_height)
    he = getHe(hf, tension_frange, compression_frange)
    rivet_web_flange = RivetWebFlange(rivet_web_frange_D, rivet_web_pdratio, rivet_web_frange_N, web)
    # print("he",he)
    he_array.append(he)
    """
    csv書き出し
    """

    with open('sta2000.csv', 'w', encoding='UTF-8') as f:
        writer = csv.writer(f)
        web.makeheader(writer)
        web.makerow(writer, Sf, he)
        stiffener.makeheader(writer)
        stiffener.makerow(writer, he, web_distance, web_thickness)
        compression_frange.makeheader(writer)
        compression_frange.makerow(writer, Mf, he, web_thickness)
        tension_frange.makeheader(writer)
        tension_frange.makerow(writer, Mf, he, web_thickness)
        rivet_web_stiffener.makeheader(writer)
        rivet_web_stiffener.makerow(writer, Sf, he, web_distance)
        rivet_web_flange.makeheader(writer)
        rivet_web_flange.makerow(writer, Sf, he)


def calcsta2500():
    sta = 2500
    y = sm_df.ix[4][1]
    Sf = sm_df.ix[4][4]
    # print("Sf",Sf)
    Mf = sm_df.ix[4][5]
    # print("Mf",Mf)
    # print(getHf(685))
    """
    以下パラメーターの設定
    """
    stiffner_thickness = 1.27  # mm
    stiffner_bs1 = 25
    stiffner_bs2 = 18
    web_thickness = 1.27
    web_distance = 70  # stiffener 間隔でもある
    hf = getHf(sta + web_distance)
    tension_frange_thickness = 4.5
    tension_frange_bottom = 35
    tension_frange_height = 30
    compression_frange_thickness = 4.5
    compression_frange_bottom = 35
    compression_frange_height = 30
    rivet_web_stiffner_diameter = 6.35  # DD8
    rivet_web_frange_N = 2
    rivet_web_frange_D = 6.35
    rivet_web_pdratio = 6
    """
    オブジェクト生成
    """
    stiffener = Stiffener(stiffner_thickness, stiffner_bs1, stiffner_bs2)
    web = Web(web_thickness, getHf(sta), web_distance)
    rivet_web_stiffener = RivetWebStiffener(rivet_web_stiffner_diameter, stiffener, web)
    tension_frange = TensionFrange(tension_frange_thickness, tension_frange_bottom, tension_frange_height)
    compression_frange = CompressionFlange(compression_frange_thickness, compression_frange_bottom,
                                           compression_frange_height)
    he = getHe(hf, tension_frange, compression_frange)
    rivet_web_flange = RivetWebFlange(rivet_web_frange_D, rivet_web_pdratio, rivet_web_frange_N, web)
    he_array.append(he)
    # print("he",he)
    """
    csv書き出し
    """

    with open('sta2500.csv', 'w', encoding='UTF-8') as f:
        writer = csv.writer(f)
        web.makeheader(writer)
        web.makerow(writer, Sf, he)
        stiffener.makeheader(writer)
        stiffener.makerow(writer, he, web_distance, web_thickness)
        compression_frange.makeheader(writer)
        compression_frange.makerow(writer, Mf, he, web_thickness)
        tension_frange.makeheader(writer)
        tension_frange.makerow(writer, Mf, he, web_thickness)
        rivet_web_stiffener.makeheader(writer)
        rivet_web_stiffener.makerow(writer, Sf, he, web_distance)
        rivet_web_flange.makeheader(writer)
        rivet_web_flange.makerow(writer, Sf, he)


def calcsta3000():
    sta = 3000
    y = sm_df.ix[5][1]
    Sf = sm_df.ix[5][4]
    # print("Sf",Sf)
    Mf = sm_df.ix[5][5]
    # print("Mf",Mf)
    # print(getHf(685))
    """
    以下パラメーターの設定
    """

    stiffner_thickness = 0.81  # mm
    stiffner_bs1 = 20
    stiffner_bs2 = 15
    web_thickness = 1.02
    web_distance = 70  # stiffener 間隔でもある
    hf = getHf(sta + web_distance)
    tension_frange_thickness = 3.0
    tension_frange_bottom = 25
    tension_frange_height = 20
    compression_frange_thickness = 3.0
    compression_frange_bottom = 30
    compression_frange_height = 20
    rivet_web_stiffner_diameter = 6.35  # DD8
    rivet_web_frange_N = 2
    rivet_web_frange_D = 6.35
    rivet_web_pdratio = 6
    """
    オブジェクト生成
    """
    stiffener = Stiffener(stiffner_thickness, stiffner_bs1, stiffner_bs2)
    web = Web(web_thickness, getHf(sta), web_distance)
    rivet_web_stiffener = RivetWebStiffener(rivet_web_stiffner_diameter, stiffener, web)
    tension_frange = TensionFrange(tension_frange_thickness, tension_frange_bottom, tension_frange_height)
    compression_frange = CompressionFlange(compression_frange_thickness, compression_frange_bottom,
                                           compression_frange_height)
    he = getHe(hf, tension_frange, compression_frange)
    rivet_web_flange = RivetWebFlange(rivet_web_frange_D, rivet_web_pdratio, rivet_web_frange_N, web)
    # print("he",he)
    he_array.append(he)
    """
    csv書き出し
    """

    with open('sta3000.csv', 'w', encoding='UTF-8') as f:
        writer = csv.writer(f)
        web.makeheader(writer)
        web.makerow(writer, Sf, he)
        stiffener.makeheader(writer)
        stiffener.makerow(writer, he, web_distance, web_thickness)
        compression_frange.makeheader(writer)
        compression_frange.makerow(writer, Mf, he, web_thickness)
        tension_frange.makeheader(writer)
        tension_frange.makerow(writer, Mf, he, web_thickness)
        rivet_web_stiffener.makeheader(writer)
        rivet_web_stiffener.makerow(writer, Sf, he, web_distance)
        rivet_web_flange.makeheader(writer)
        rivet_web_flange.makerow(writer, Sf, he)


def calcsta3500():
    sta = 3500
    y = sm_df.ix[6][1]
    Sf = sm_df.ix[6][4]
    # print("Sf",Sf)
    Mf = sm_df.ix[6][5]
    # print("Mf",Mf)
    # print(getHf(685))
    """
    以下パラメーターの設定
    """

    stiffner_thickness = 0.81  # mm
    stiffner_bs1 = 20
    stiffner_bs2 = 15
    web_thickness = 1.02
    web_distance = 70  # stiffener 間隔でもある
    hf = getHf(sta + web_distance)
    tension_frange_thickness = 2.0
    tension_frange_bottom = 25
    tension_frange_height = 15
    compression_frange_thickness = 2.5
    compression_frange_bottom = 25
    compression_frange_height = 15
    rivet_web_stiffner_diameter = 6.35  # DD8
    rivet_web_frange_N = 2
    rivet_web_frange_D = 6.35
    rivet_web_pdratio = 6
    """
    オブジェクト生成
    """
    stiffener = Stiffener(stiffner_thickness, stiffner_bs1, stiffner_bs2)
    web = Web(web_thickness, getHf(sta), web_distance)
    rivet_web_stiffener = RivetWebStiffener(rivet_web_stiffner_diameter, stiffener, web)
    tension_frange = TensionFrange(tension_frange_thickness, tension_frange_bottom, tension_frange_height)
    compression_frange = CompressionFlange(compression_frange_thickness, compression_frange_bottom,
                                           compression_frange_height)
    he = getHe(hf, tension_frange, compression_frange)
    rivet_web_flange = RivetWebFlange(rivet_web_frange_D, rivet_web_pdratio, rivet_web_frange_N, web)
    # print("he",he)
    he_array.append(he)
    """
    csv書き出し
    """

    with open('sta3500.csv', 'w', encoding='UTF-8') as f:
        writer = csv.writer(f)
        web.makeheader(writer)
        web.makerow(writer, Sf, he)
        stiffener.makeheader(writer)
        stiffener.makerow(writer, he, web_distance, web_thickness)
        compression_frange.makeheader(writer)
        compression_frange.makerow(writer, Mf, he, web_thickness)
        tension_frange.makeheader(writer)
        tension_frange.makerow(writer, Mf, he, web_thickness)
        rivet_web_stiffener.makeheader(writer)
        rivet_web_stiffener.makerow(writer, Sf, he, web_distance)
        rivet_web_flange.makeheader(writer)
        rivet_web_flange.makerow(writer, Sf, he)


def calcsta4000():
    sta = 4000
    y = sm_df.ix[7][1]
    Sf = sm_df.ix[7][4]
    # print("Sf",Sf)
    Mf = sm_df.ix[7][5]
    # print("Mf",Mf)
    # print(getHf(685))
    """
    以下パラメーターの設定
    """

    stiffner_thickness = 0.81  # mm
    stiffner_bs1 = 20
    stiffner_bs2 = 15
    web_thickness = 1.02
    web_distance = 70  # stiffener 間隔でもある
    hf = getHf(sta + web_distance)
    tension_frange_thickness = 2.0
    tension_frange_bottom = 20
    tension_frange_height = 10
    compression_frange_thickness = 2.0
    compression_frange_bottom = 20
    compression_frange_height = 10
    rivet_web_stiffner_diameter = 6.35  # DD8
    rivet_web_frange_N = 2
    rivet_web_frange_D = 6.35
    rivet_web_pdratio = 6
    """
    オブジェクト生成
    """
    stiffener = Stiffener(stiffner_thickness, stiffner_bs1, stiffner_bs2)
    web = Web(web_thickness, getHf(sta), web_distance)
    rivet_web_stiffener = RivetWebStiffener(rivet_web_stiffner_diameter, stiffener, web)
    tension_frange = TensionFrange(tension_frange_thickness, tension_frange_bottom, tension_frange_height)
    compression_frange = CompressionFlange(compression_frange_thickness, compression_frange_bottom,
                                           compression_frange_height)
    he = getHe(hf, tension_frange, compression_frange)
    rivet_web_flange = RivetWebFlange(rivet_web_frange_D, rivet_web_pdratio, rivet_web_frange_N, web)
    # print("he",he)
    he_array.append(he)
    """
    csv書き出し
    """

    with open('sta4000.csv', 'w', encoding='UTF-8') as f:
        writer = csv.writer(f)
        web.makeheader(writer)
        web.makerow(writer, Sf, he)
        stiffener.makeheader(writer)
        stiffener.makerow(writer, he, web_distance, web_thickness)
        compression_frange.makeheader(writer)
        compression_frange.makerow(writer, Mf, he, web_thickness)
        tension_frange.makeheader(writer)
        tension_frange.makerow(writer, Mf, he, web_thickness)
        rivet_web_stiffener.makeheader(writer)
        rivet_web_stiffener.makerow(writer, Sf, he, web_distance)
        rivet_web_flange.makeheader(writer)
        rivet_web_flange.makerow(writer, Sf, he)


def calcsta4500():
    sta = 4500
    y = sm_df.ix[8][1]
    Sf = sm_df.ix[8][4]
    # print("Sf",Sf)
    Mf = sm_df.ix[8][5]
    # print("Mf",Mf)
    # print(getHf(685))
    """
    以下パラメーターの設定
    """

    stiffner_thickness = 0.81  # mm
    stiffner_bs1 = 20
    stiffner_bs2 = 15
    web_thickness = 1.02
    web_distance = 70  # stiffener 間隔でもある
    hf = getHf(sta + web_distance)
    tension_frange_thickness = 2.0
    tension_frange_bottom = 20
    tension_frange_height = 10
    compression_frange_thickness = 2.0
    compression_frange_bottom = 20
    compression_frange_height = 10
    rivet_web_stiffner_diameter = 6.35  # DD8
    rivet_web_frange_N = 2
    rivet_web_frange_D = 6.35 / 2

    rivet_web_pdratio = 6

    """
    オブジェクト生成
    """
    stiffener = Stiffener(stiffner_thickness, stiffner_bs1, stiffner_bs2)
    web = Web(web_thickness, getHf(sta), web_distance)
    rivet_web_stiffener = RivetWebStiffener(rivet_web_stiffner_diameter, stiffener, web)
    tension_frange = TensionFrange(tension_frange_thickness, tension_frange_bottom, tension_frange_height)
    compression_frange = CompressionFlange(compression_frange_thickness, compression_frange_bottom,
                                           compression_frange_height)
    he = getHe(hf, tension_frange, compression_frange)
    rivet_web_flange = RivetWebFlange(rivet_web_frange_D, rivet_web_pdratio, rivet_web_frange_N, web)
    # print("he",he)
    he_array.append(he)
    """
    csv書き出し
    """

    with open('sta4500.csv', 'w', encoding='UTF-8') as f:
        writer = csv.writer(f)
        web.makeheader(writer)
        web.makerow(writer, Sf, he)
        stiffener.makeheader(writer)
        stiffener.makerow(writer, he, web_distance, web_thickness)
        compression_frange.makeheader(writer)
        compression_frange.makerow(writer, Mf, he, web_thickness)
        tension_frange.makeheader(writer)
        tension_frange.makerow(writer, Mf, he, web_thickness)
        rivet_web_stiffener.makeheader(writer)
        rivet_web_stiffener.makerow(writer, Sf, he, web_distance)
        rivet_web_flange.makeheader(writer)
        rivet_web_flange.makerow(writer, Sf, he)


def printhe():
    print(he_array)


if __name__ == '__main__':
    calcsta625()
    calcsta1000()
    calcsta1500()
    calcsta2000()
    calcsta2500()
    calcsta3000()
    calcsta3500()
    calcsta4000()
    calcsta4500()
    printhe()
