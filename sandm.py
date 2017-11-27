# -*- coding: utf-8 -*-
import numpy  as np

C_L = 1.4  # 最大揚力係数
C_ROOT = 2.13 * 1000  # rootのchord長[mm]
C_TIP = 1.07 * 1000  # tipのroot長[mm]
ALPHA_F = np.rad2deg(14.5)# [rad]
W = 1500 * 9.8  # 自重[N]
N_Z = 6  # 最大荷重倍数
DELTA_Y = 25  # [mm]
HARF_SPAN = 5000  # [mm]
Y_REP_FOR_C = 5000 * np.array([0, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.975, 1.0])  # [mm]
C_LA_REP = np.array([0.835, 1.021, 1.095, 1.089, 0.993,
                     0.833, 0.662, 0.548, 0])  # [no dim]
C_LB_REP = np.array([0.049, 0.044, 0.005, -0.033, -
                     0.062, -0.067, -0.056, -0.043, 0])  # [no dim]
C_D_REP = np.array([0.1679, 0.1303, 0.1105, 0.1065, 0.1163,
                    0.1314, 0.1354, 0.1302, 0])  # [no dim]
Y_REP_FOR_W = np.array([625, 750, 1000, 1250, 1500, 1750,
                        2000, 2250, 2500, 2750, 3000, 3250, 3500,
                        3750, 4000, 4250, 4500, 4750, 5000])  # [mm]


Y_DISTANCE_FOR_W=np.array([Y_REP_FOR_W[i+1]-Y_REP_FOR_W[i] for i in range(0,Y_REP_FOR_W.shape[0]-1)])
W_REP = 9.8 * np.array([15, 12, 11, 7, 6, 5, 4, 4, 3,
                        4, 4, 3, 3, 3, 2, 2, 2, 1])#[N]

RHO_REP=W_REP/Y_DISTANCE_FOR_W

def getC_la(y):
    return np.interp(y, Y_REP_FOR_C, C_LA_REP)

def getC_lb(y):
    return np.interp(y,Y_REP_FOR_C,C_LB_REP)

def getC_D(y):
    return np.interp(y,Y_REP_FOR_C,C_D_REP)

def get_RHO(y):
    return np.interp(y,Y_REP_FOR_W,RHO_REP)

if __name__ == '__main__':
    print(getC_la(1000))
