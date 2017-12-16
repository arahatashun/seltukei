"""
剛性計算用.
main関数内の変数を自分の値に変えて実行するだけ.
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Hirotaka Kondo
from rib import Rib
from unit_convert import ksi2Mpa, get_hf
import csv
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np


def get_rib(index, web_t, div, fc_t, bcf1, bcf2, ft_t, btf1, btf2):
    """
    :param index: Ribを定める番号 Ribクラスのy_indexに準拠
    :param web_t: web厚さ[mm]
    :param div:  分割数
    :param fc_t: 圧縮側フランジ厚さ[mm]
    :param bcf1: 圧縮側フランジbottom_length[mm]
    :param bcf2: 圧縮側フランジheight[mm]
    :param ft_t: 引張側フランジ厚さ[mm]
    :param btf1: 引張側フランジbottom_length[mm]
    :param btf2: 圧縮側フランジheight[mm]
    :return:
    """
    rib = Rib(index)
    rib.add_web(web_t, div)
    rib.add_compression_flange(fc_t, bcf1, bcf2)
    rib.add_tension_flange(ft_t, btf1, btf2)
    return rib


def cal_web_I(web_t, height):
    """
    ウェブの断面二次モーメントの計算
    :param web_t:ウェブ厚さ[mm]
    :param height:ウェブ高さ[mm]
    :return: I[mm^4]
    """
    return web_t * height ** 3 / 12


def cal_flange_I(flange_area, he):
    """
    一つの区間の上部(or下部)フランジの
    断面二次モーメントの和を求める.
    :return:
    """
    return flange_area * (he / 2) ** 2


def make_header_stiffness():
    """Make csv header."""
    header1 = ["", "", "ウェブ", "", "", "圧縮側フランジ", "", "", "引張側フランジ", "", "", "合計"]
    header2 = ["STA", "$h_e$[mm]", "ウェブ厚さ[mm]", "I[$mm^4$]", "EI[$Nm^2$]", "有効断面積[$mm^2$]", "I[$mm^4$]", "EI[$Nm^2$]",
               "有効断面積[$mm^2$]", "I[$mm^4$]", "EI[$Nm^2$]", "EI[$Nm^2$]"]
    with open('results/stiffness.csv', 'a', encoding="Shift_JIS") as f:
        writer = csv.writer(f)
        writer.writerow(header1)
        writer.writerow(header2)


def make_stiffness_row(sta):
    web_t = sta.web.thickness
    he = sta.he
    E = ksi2Mpa(10.3 * 1000)  # ヤング率[N/mm^2]
    area_c = sta.cflange.get_area(web_t)
    area_t = sta.tflange.get_area(web_t)
    I_w = cal_web_I(web_t, sta.hf)
    I_c = cal_flange_I(area_c, he)
    I_t = cal_flange_I(area_t, he)
    EI_w = E * I_w / 10 ** 6  # [N*m^2]
    EI_c = E * I_c / 10 ** 6  # [N*m^2]
    EI_t = E * I_t / 10 ** 6  # [N*m^2]
    value = [sta.y_left, he, web_t, I_w, EI_w, area_c, I_c,
             EI_c, area_t, I_t, EI_t, EI_w + EI_c + EI_t]
    with open('results/stiffness.csv', 'a', encoding="Shift_JIS") as f:
        writer = csv.writer(f)
        writer.writerow(value)

    return EI_w + EI_c + EI_t


def cal_EI_sta5000(sta4500):
    """
    翼端部だけ剛性計算用の値が用意されてないので,
    専用関数を作成
    :param sta4500:
    :return:
    """
    web_t = sta4500.web.thickness
    he = sta4500.he + get_hf(5000) - get_hf(4500)
    E = ksi2Mpa(10.3 * 1000)  # ヤング率[N/mm^2]
    area_c = sta4500.cflange.get_area(web_t)
    area_t = sta4500.tflange.get_area(web_t)
    I_w = cal_web_I(web_t, get_hf(5000))
    I_c = cal_flange_I(area_c, he)
    I_t = cal_flange_I(area_t, he)
    return E * (I_w + I_c + I_t) / 10 ** 6  # [N*m^2]


def plot(sta_EI_list):
    """
    EIのグラフ作成用
    :param sta_EI_list:
    :return:
    """
    LEFT_ARRAY = np.array([625, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000])
    plt.xlabel("STA")
    plt.ylabel("EI[$N\cdot$$m^2$]")
    plt.xlim(625, 5000)
    plt.gca().ticklabel_format(style="sci", scilimits=(0, 0), axis="y")
    plt.xticks([625, 1000, 2000, 3000, 4000, 5000])

    sp = interpolate.InterpolatedUnivariateSpline(LEFT_ARRAY, sta_EI_list)
    sx = np.linspace(LEFT_ARRAY[0], LEFT_ARRAY[-1], 100)
    sy = sp(sx)
    plt.plot(LEFT_ARRAY, sta_EI_list, "bo")
    plt.plot(sx, sy, "b")
    plt.show()


def cal_ave(sta_EI_list):
    RIB_WIDTH = np.array([375, 500, 500, 500, 500, 500, 500, 500, 500])
    sta625_1000_EI = (sta_EI_list[0] + sta_EI_list[1]) / 2
    sta1000_1500_EI = (sta_EI_list[1] + sta_EI_list[2]) / 2
    sta1500_2000_EI = (sta_EI_list[2] + sta_EI_list[3]) / 2
    sta2000_2500_EI = (sta_EI_list[3] + sta_EI_list[4]) / 2
    sta2500_3000_EI = (sta_EI_list[4] + sta_EI_list[5]) / 2
    sta3000_3500_EI = (sta_EI_list[5] + sta_EI_list[6]) / 2
    sta3500_4000_EI = (sta_EI_list[6] + sta_EI_list[7]) / 2
    sta4000_4500_EI = (sta_EI_list[7] + sta_EI_list[8]) / 2
    sta4500_5000_EI = (sta_EI_list[8] + sta_EI_list[9]) / 2
    sta_mean_list = np.array(
        [sta625_1000_EI, sta1000_1500_EI, sta1500_2000_EI, sta2000_2500_EI, sta2500_3000_EI, sta3000_3500_EI,
         sta3500_4000_EI, sta4000_4500_EI, sta4500_5000_EI])
    EI_ave = np.dot(sta_mean_list, RIB_WIDTH) / 5000
    print("average EI is {0}[N*m^2]".format(EI_ave))
    return EI_ave


def main():
    """
    get_ribの引数は自分で計算したパラメータを利用
    1番目: そのままで変えないで良い [どのRib区間かを決めるindex(Ribクラスと共通)]
    2番目: ウェブ厚さ[mm]
    3番目: ウェブ分割数
    4番目: 圧縮側(上部)フランジ厚さ[mm]
    5番目: 圧縮側(上部)フランジ底長さ[mm]
    6番目: 圧縮側(上部)フランジ高さ[mm]
    7番目: 引張側(下部)フランジ厚さ[mm]
    8番目: 引張側(下側)フランジ底長さ[mm]
    9番目: 引張側(下側)フランジ高さ[mm]
    :return:
    """
    sta625 = get_rib(0, 1.6, 4, 9, 20, 20, 9, 24, 34)
    sta1000 = get_rib(1, 1.6, 6, 8, 15, 17, 8, 21, 33)
    sta1500 = get_rib(2, 1.6, 5, 8, 15, 15, 8, 27, 15)
    sta2000 = get_rib(3, 1.6, 5, 5, 15, 15, 5, 15, 33)
    sta2500 = get_rib(4, 1.6, 5, 4, 15, 15, 4, 15, 21)
    sta3000 = get_rib(5, 1.6, 4, 2.5, 25, 25, 2.5, 25, 25)
    sta3500 = get_rib(6, 1.6, 3, 2, 20, 20, 2, 20, 20)
    sta4000 = get_rib(7, 1.6, 3, 2, 10, 10, 2, 10, 10)
    sta4500 = get_rib(8, 1.6, 2, 1.6, 10, 10, 1.6, 10, 10)

    make_header_stiffness()

    sta_EI_list = []
    sta_EI_list.append(make_stiffness_row(sta625))
    sta_EI_list.append(make_stiffness_row(sta1000))
    sta_EI_list.append(make_stiffness_row(sta1500))
    sta_EI_list.append(make_stiffness_row(sta2000))
    sta_EI_list.append(make_stiffness_row(sta2500))
    sta_EI_list.append(make_stiffness_row(sta3000))
    sta_EI_list.append(make_stiffness_row(sta3500))
    sta_EI_list.append(make_stiffness_row(sta4000))
    sta_EI_list.append(make_stiffness_row(sta4500))
    sta_EI_list.append(cal_EI_sta5000(sta4500))  # STA5000
    cal_ave(sta_EI_list)
    plot(sta_EI_list)


if __name__ == "__main__":
    main()
