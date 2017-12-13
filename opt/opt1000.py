# -*- coding: utf-8 -*-
# Author: Hirotaka Kondo
import os
import csv
from web import make_web_header
from stiffener import make_stiffener_header
from tension_flange import make_tflange_header
from compression_flange import make_cflange_header
from rivet_web_stiffener import rivet_ws_make_all_header
from rivet_web_flange import rivet_wf_make_all_header
from rib import Rib
import numpy as np
import numba

"""
1.補強材の板厚はウェブの厚さの1サイズアップとすることが多い.
2.鋲径Dと板厚tに対して,D<=3tが良い(らしい).
3.フランジ(Extrusion材)は板厚最低1.6mmを確保.
"""

# Y_REP = np.array([625, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000])  # WEBの左端右端STA[mm]の候補リスト
# WEB_THICKNESS_LIST = np.array(
#   [0.41, 0.51, 0.64, 0.81, 1.02, 1.27, 1.60, 1.80, 2.03, 2.29, 2.54, 3.18])  # web厚さ[mm]の候補リスト
# WEB_THICKNESS_LIST = [1.60, 1.80, 2.03]  # web厚さ[mm]の候補リスト
# RIVET_DICT = {3: 2.38125, 4: 3.175, 5: 3.96875, 6: 4.7625, 8: 6.35}  # リベット径[mm]の候補辞書(keyは呼び番号)
RIVET_DICT = {5: 3.96875, 6: 4.7625}  # リベット径[mm]の候補辞書(keyは呼び番号)
DIVISION_LIST = [4, 5, 6]  # webの分割数の候補リスト
# STIFFENER_THICKNESS_LIST = [1.80, 2.03, 2.29, 2.54, 3.18]  # 適当
FLANGE_THICKNESS_LIST = [8 + i for i in range(5)]  # 適当
STIFFENER_B_LIST = [15 + 2 * i for i in range(10)]
FLANGE_B_LIST = [15 + 2 * i for i in range(10)]


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


def mass_csv(mass):
    with open('mass.csv', 'a', encoding="Shift_JIS") as f:
        writer = csv.writer(f)
        writer.writerow(mass)


@numba.jit
def make_sta1000():
    min_mass = 100  # [kg]
    counter = 0
    n = len(FLANGE_THICKNESS_LIST) ** 2 * \
        len(STIFFENER_B_LIST) ** 2 * len(FLANGE_B_LIST) ** 2 * len(DIVISION_LIST) ** 2 * len(RIVET_DICT.values()) ** 2
    for fc_thickness in FLANGE_THICKNESS_LIST:
        for ft_thickness in FLANGE_THICKNESS_LIST:
            for bs1 in STIFFENER_B_LIST:
                for bs2 in STIFFENER_B_LIST:
                    for bf1 in FLANGE_B_LIST:
                        for bf2 in FLANGE_B_LIST:
                            for bf3 in FLANGE_B_LIST:
                                for bf4 in FLANGE_B_LIST:
                                    for div in DIVISION_LIST:
                                        for D1 in RIVET_DICT.values():
                                            for D2 in RIVET_DICT.values():
                                                sta625 = Rib(1)
                                                sta625.add_web(1.60, div)
                                                sta625.add_stiffener(1.80, bs1, bs2)
                                                sta625.add_compression_flange(fc_thickness, bf1, bf2)
                                                sta625.add_tension_flange(ft_thickness, bf3, bf4)
                                                sta625.add_rivet_stiffener(D1)
                                                sta625.add_rivet_flange(D2, 4, 2)
                                                sta625.set_he()
                                                if sta625.decide_ms() == True:
                                                    mass = sta625.get_total_mass()  # [kg]
                                                    if mass < min_mass:
                                                        mass_csv([mass])
                                                        counter += 1
                                                        min_mass = mass
                                                        print("counter: {0}/{1}\n".format(counter, n))
                                                        init_header()
                                                        sta625.web_csv()
                                                        sta625.tflange_csv()
                                                        sta625.cflange_csv()
                                                        sta625.stiffener_csv()
                                                        sta625.rivet_stiffener_csv()
                                                        sta625.rivet_flange_csv()
                                                    else:
                                                        counter += 1
                                                        print("counter: {0}/{1}\n".format(counter, n))
                                                else:
                                                    counter += 1
                                                    print("counter: {0}/{1}\n".format(counter, n))


if __name__ == '__main__':
    make_sta1000()
