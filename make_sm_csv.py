# -*- coding: utf-8 -*-
# Author: Hirotaka Kondo
import numpy as np
from scipy import interpolate
from scipy.integrate import quad

C_L = 1.4  # 最大揚力係数
C_ROOT = 2.13 * 1000  # rootのchord長[mm]
C_TIP = 1.07 * 1000  # tipのroot長[mm]
ALPHA_F = np.deg2rad(14.5)  # [rad]
W = 1500 * 9.8  # 自重[N]
N_Z = 6  # 最大荷重倍数
HALF_SPAN = 5000  # [mm]

Y_REP_FOR_C = 5000 * np.array([0, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.975, 1.0])  # [mm]
C_LA_REP = np.array([0.835, 1.021, 1.095, 1.089, 0.993, 0.833, 0.662, 0.548, 0])  # [no dim]
C_LB_REP = np.array([0.049, 0.044, 0.005, -0.033, -0.062, -0.067, -0.056, -0.043, 0])  # [no dim]
C_D_REP = np.array([0.1679, 0.1303, 0.1105, 0.1065, 0.1163, 0.1314, 0.1354, 0.1302, 0])  # [no dim]

CHORD_ARRAY = [C_ROOT, C_TIP]  # [mm]
STA_FOR_CHORD = [0, HALF_SPAN]  # [mm]

Y_REP_FOR_W = np.array([625, 750, 1000, 1250, 1500, 1750,
                        2000, 2250, 2500, 2750, 3000, 3250, 3500,
                        3750, 4000, 4250, 4500, 4750, 5000])  # [mm]
Y_MID_REP_FOR_W = np.array([687.5, 875, 1125, 1375, 1625, 1875, 2125, 2375, 2625, 2875, 3125, 3375,
                            3625, 3825, 4125, 4375, 4625, 4875])
RIBS_ARRAY = [625, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
Y_DISTANCE_FOR_W = np.array([Y_REP_FOR_W[i + 1] - Y_REP_FOR_W[i] for i in range(0, len(Y_REP_FOR_W) - 1)])
W_REP = 9.8 * np.array([15, 12, 11, 7, 6, 5, 4, 4, 3,
                        4, 4, 3, 3, 3, 2, 2, 2, 1])  # [N]

RHO_REP = W_REP / Y_DISTANCE_FOR_W


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
def get_eta_a():
    integral = quad(get_ccz, 0, HALF_SPAN)
    return 1 / 2 * N_Z * W / (integral[0] / 1000 / 1000)  # 単位をmに揃える
"""


def get_sa(y):
    eta_a = 4039.29  # get_eta_aで計算済み
    integral = quad(get_ccz, y, HALF_SPAN)
    return eta_a * integral[0] / 1000 / 1000  # 単位をmに揃える


"""
def get_rho(y):
    return np.interp(y, Y_MID_REP_FOR_W, RHO_REP)


def getS1(y):
    step = 100
    ans = N_Z * np.sum([getRHO(y + step * i) *
                        step for i in np.arange(np.floor((HALF_SPAN - y) / step))])
    return ans


def getS(y):
    return getSa(y) - getS1(y)


def getM(y):
    step = 100
    ans = np.sum([getS(y + step * i) *
                  step for i in np.arange(np.floor((HALF_SPAN - y) / step))])
    return ans / 1000


# 前桁高さ


def getHf(y):
    HF_ARRAY = [130, 320]
    Y_ARRAY_FOR_HF = [5000, 625]
    return np.interp(y, Y_ARRAY_FOR_HF, HF_ARRAY)
"""

if __name__ == '__main__':
    for i in range(500):
        print(get_sa(i))
