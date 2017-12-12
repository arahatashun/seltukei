# -*- coding: utf-8 -*-
# Author: Hirotaka Kondo
import os
from web import make_web_header
from stiffener import make_stiffener_header
from tension_flange import make_tflange_header
from compression_flange import make_cflange_header
from rivet_web_stiffener import rivet_ws_make_all_header
from rivet_web_flange import rivet_wf_make_all_header
from rib import Rib
import numpy as np

# WEB_THICKNESS_LIST = np.array(
#   [0.41, 0.51, 0.64, 0.81, 1.02, 1.27, 1.60, 1.80, 2.03, 2.29, 2.54, 3.18])  # web厚さ[mm]の候補リスト
WEB_THICKNESS_LIST = np.array(
    [2.29])  # web厚さ[mm]の候補リスト
# RIVET_DICT = {3: 2.38125, 4: 3.175, 5: 3.96875, 6: 4.7625, 8: 6.35}  # リベット径[mm]の候補辞書(keyは呼び番号)
RIVET_DICT = {8: 6.35}  # リベット径[mm]の候補辞書(keyは呼び番号)
# Y_REP = np.array([625, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000])  # WEBの左端右端STA[mm]の候補リスト
DIVISION_LIST = np.array([4])  # webの分割数の候補リスト
STIFFENER_THICKNESS_LIST = np.array([0.5 + i * 0.5 for i in range(5)])  # 適当
FLANGE_THICKNESS_LIST = np.array([5 + i for i in range(5)])  # 適当
STIFFENER_B_LIST = np.array([20 + i for i in range(20)])
FLANGE_B_LIST = np.array([20 + i for i in range(20)])


# リブ左端の座標
# LEFT_ARRAY = [625, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500]
# リブの間隔
# RIB_WIDTH = [375, 500, 500, 500, 500, 500, 500, 500, 500]


def init_header():
    """header 作成"""
    # delete
    directory = 'results/'
    test = os.listdir(directory)
    for item in test:
        if item.endswith(".csv"):
            os.remove(os.path.join(directory, item))
    # header
    make_web_header()
    make_stiffener_header()
    make_tflange_header()
    make_cflange_header()
    rivet_wf_make_all_header()
    rivet_ws_make_all_header()


def make_sta625():
    min_mass = 100  # [kg]
    counter = 0
    for w_thickness in WEB_THICKNESS_LIST:
        for s_thickness in STIFFENER_THICKNESS_LIST:
            for fc_thickness in FLANGE_THICKNESS_LIST:
                for ft_thickness in FLANGE_THICKNESS_LIST:
                    for bs1 in STIFFENER_B_LIST:
                        for bs2 in STIFFENER_B_LIST:
                            for div in DIVISION_LIST:
                                for bf1 in FLANGE_B_LIST:
                                    for bf2 in FLANGE_B_LIST:
                                        for D1 in RIVET_DICT.values():
                                            for D2 in RIVET_DICT.values():
                                                sta625 = Rib(0)
                                                sta625.add_web(w_thickness, div)
                                                sta625.add_stiffener(s_thickness, bs1, bs2)
                                                sta625.add_compression_flange(fc_thickness, bf1, bf2)
                                                sta625.add_tension_flange(ft_thickness, bf1, bf2)
                                                sta625.add_rivet_stiffener(D1)
                                                sta625.add_rivet_flange(D2, 4, 2)
                                                sta625.set_he()
                                                if (sta625.decide_ms() == True):
                                                    print("all M.S. > 0")
                                                    mass = sta625.get_total_volume() * 3.0 / 1000  # [kg]
                                                    if mass < min_mass:
                                                        counter += 1
                                                        print("counter: {0}".format(counter))
                                                        print("found lighter one: {0}[kg]\n".format(mass))
                                                        min_mass = mass
                                                        init_header()
                                                        sta625.web_csv()
                                                        sta625.tflange_csv()
                                                        sta625.cflange_csv()
                                                        sta625.stiffener_csv()
                                                        sta625.rivet_stiffener_csv()
                                                        sta625.rivet_flange_csv()
                                                    else:
                                                        counter += 1
                                                        print("counter: {0}".format(counter))
                                                        print("not lighter one\n")
                                                else:
                                                    counter += 1
                                                    print("counter: {0}".format(counter))
                                                    print("not all M.S. > 0\n")


def main():
    init_header()
    make_sta625()


if __name__ == '__main__':
    make_sta625()
