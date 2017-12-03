# -*- coding: utf-8 -*-
# Author: Hirotaka Kondo
import numpy as np
from scipy import interpolate
from scipy.integrate import quad
import csv

C_L = 1.4  # 最大揚力係数
C_ROOT = 2.13 * 1000  # rootのchord長[mm]
C_TIP = 1.07 * 1000  # tipのroot長[mm]
ALPHA_F = np.deg2rad(14.5)  # [rad]
W = 1500 * 9.8  # 自重[N]
N_Z = 6  # 最大荷重倍数
HALF_SPAN = 5000  # [mm]

Y_REP_FOR_C = np.array([0, 1000, 2000, 3000, 4000, 4500, 4750, 4875, 5000])  # [mm]
C_LA_REP = np.array([0.835, 1.021, 1.095, 1.089, 0.993, 0.833, 0.662, 0.548, 0])  # [no dim]
C_LB_REP = np.array([0.049, 0.044, 0.005, -0.033, -0.062, -0.067, -0.056, -0.043, 0])  # [no dim]
C_D_REP = np.array([0.1679, 0.1303, 0.1105, 0.1065, 0.1163, 0.1314, 0.1354, 0.1302, 0])  # [no dim]

CHORD_ARRAY = [C_ROOT, C_TIP]  # [mm]
STA_FOR_CHORD = [0, HALF_SPAN]  # [mm]

Y_REP_FOR_W = np.array(
    [625, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750,
     5000])  # [mm]
Y_DISTANCE_FOR_W = np.array([Y_REP_FOR_W[i + 1] - Y_REP_FOR_W[i] for i in range(0, len(Y_REP_FOR_W) - 1)])
W_REP = 9.8 * np.array([15, 12, 11, 7, 6, 5, 4, 4, 3,
                        4, 4, 3, 3, 3, 2, 2, 2, 1])  # [N]
RHO_REP = W_REP / Y_DISTANCE_FOR_W
RHO_REP = np.append(RHO_REP, [0])  # y=5000での線密度を0として便宜上追加

HF_ARRAY = [130, 320]
Y_ARRAY_FOR_HF = [5000, 625]

ETA_A = 4039.29  # get_etaaで計算済み,計算モデルが変わったらget_etaa()で計算し直すこと


def get_cla(y):
    """
    yに於けるclaを計算
    :param y:
    :return: cla[no dim]
    """
    f = interpolate.interp1d(Y_REP_FOR_C, C_LA_REP, kind='linear')
    return f(y)


def get_clb(y):
    """
    yに於けるclbを計算
    :param y:
    :return: clb[no dim]
    """
    f = interpolate.interp1d(Y_REP_FOR_C, C_LB_REP, kind='linear')
    return f(y)


def get_cd(y):
    """
    yに於けるcdを計算
    :param y:
    :return: cd[no dim]
    """
    f = interpolate.interp1d(Y_REP_FOR_C, C_D_REP, kind='linear')
    return f(y)


def get_cl(y):
    """
    yに於けるclを計算
    :param y:
    :return: cl[no dim]
    """
    return C_L * get_cla(y) + get_clb(y)


def get_cz(y):
    """
    yに於けるczを計算
    :param y:
    :return: cz[no dim]
    """
    return get_cl(y) * np.cos(ALPHA_F) + get_cd(y) * np.sin(ALPHA_F)


def get_chord(y):
    """
    yに於けるchord長を計算
    :param y:
    :return: chord[mm]
    """
    f = interpolate.interp1d(STA_FOR_CHORD, CHORD_ARRAY, kind='linear')
    return f(y)


def get_ccz(y):
    """
    yに於けるc*czを計算
    :param y:
    :return: c*cz[mm]
    """
    return get_chord(y) * get_cz(y)


"""
def get_etaa():
    integral = quad(get_ccz, 0, HALF_SPAN)
    return 1 / 2 * N_Z * W / (integral[0] / 1000 / 1000)  # 単位をmに揃える
"""


def get_sa(y_w, limit_div=50):
    """
    y_wに於けるsaを計算
    :param y_w:
    :param limit_div:
    :return: sa[N]
    """
    integral = quad(get_ccz, y_w, HALF_SPAN, limit=limit_div)
    return ETA_A * integral[0] / 1000 / 1000  # 単位をmに揃える


def get_rho(y):
    """
    yに於ける荷重分布rho[N/mm]を計算
    :param y:
    :return:rho[N/mm]
    """
    f = interpolate.interp1d(Y_REP_FOR_W, RHO_REP, kind='zero')
    return f(y)


def get_si(y_w, limit_div=50):
    """
    y_wに於ける慣性力s1を計算
    :param y_w:
    :param limit_div:
    :return: s1[N]
    """
    integral = quad(get_rho, y_w, HALF_SPAN, limit=limit_div)
    return N_Z * integral[0]  # 単位をmに揃える


def get_s(y_w, limit_div=50):
    """
    y_wにおけるせん断力を計算
    :param y_w:
    :param limit_div:
    :return:
    """
    s = get_sa(y_w, limit_div) - get_si(y_w, limit_div)
    return s


def get_m(y_w, limit_div=50):
    """
    y_wに於ける曲げモーメントMを計算
    :param y_w:
    :param limit_div: quadによる積分計算の分割幅を調整(defaultは50,大きくすると計算時間長くなる)
    :return:
    """
    integral = quad(lambda yp, y: (ETA_A * get_ccz(yp) / 1000 - N_Z * get_rho(yp) * 1000) * (yp - y) / 1000, y_w,
                    HALF_SPAN, args=y_w, limit=limit_div)
    return integral[0] / 1000


def get_hf(y):
    """
    yに於ける前桁の高さを計算
    :param y:
    :return:
    """
    f = interpolate.interp1d(Y_ARRAY_FOR_HF, HF_ARRAY, kind='linear')
    return f(y)


def get_csv():
    """
    全部の値をSTA625からSTA5000まで1刻みに出力
    :return:
    """
    with open('airforce.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(
            ["y[mm]", "cla", "clb", "cd", "cl", "cz", "C[mm]", "C*cz[mm]", 'w[kg/mm]',
             'sa[N]', 'si[N]',
             'S[N]', 'M[N*m]'])
        for i in range(625, 5000):
            writer.writerow(
                [i, get_cla(i), get_clb(i), get_cd(i), get_cl(i), get_cz(i), get_chord(i), get_ccz(i),
                 get_rho(i),
                 get_sa(i, 1), get_si(i, 1), get_s(i, 1), get_m(i, 1)])


if __name__ == "__main__":
    # get_csv()
    for i in range(625, 5000):
        print("M at STA{0} is {1} [N*m]".format(i, get_m(i, 1)))
