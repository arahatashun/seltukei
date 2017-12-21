"""main"""

# -*- coding: utf-8 -*-
# Author: Shun Arahata,Hirotaka Kondo
import os
from web import make_web_header
from stiffener import make_stiffener_header
from tension_flange import make_tflange_header
from compression_flange import make_cflange_header
from rivet_web_stiffener import rivet_ws_make_all_header
from rivet_web_flange import rivet_wf_make_all_header
from rib import Rib, make_rib_header
from stiffness import calc_stiffness


def init_header():
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
    make_rib_header()

def calc_all(sta):
    """csv outputとか諸々

    :param sta: Rib instance
    """
    sta.web_csv()
    sta.tflange_csv()
    sta.cflange_csv()
    sta.stiffener_csv()
    sta.rivet_stiffener_csv()
    sta.rivet_flange_csv()
    sta.write_rib_row()
    sta.decide_ms()


def make_sta625():
    sta = Rib(0)
    sta.add_web(2.03, 3)
    sta.add_stiffener(2.03, 16, 22)
    sta.add_compression_flange(7, 30, 25)
    sta.add_tension_flange(10, 30, 30)
    """
    sta.add_compression_flange(7, 60, 25)
    sta.add_tension_flange(8, 60, 30)
    """
    sta.add_rivet_stiffener(3.175)
    sta.add_rivet_flange(3.175, 6, 2)
    calc_all(sta)
    print("sta625 mass", sta.get_total_mass())
    print("he ",sta.he)
    return sta


def make_sta1000():
    sta = Rib(1)
    sta.add_web(1.6, 6)
    sta.add_stiffener(1.8, 22, 21)
    sta.add_compression_flange(8, 27, 20)
    sta.add_tension_flange(9, 30, 30)
    sta.add_rivet_stiffener(4.7625)
    sta.add_rivet_flange(3.175, 6, 2)
    calc_all(sta)
    print("sta1000 mass", sta.get_total_mass())
    return sta


def make_sta1500():
    sta = Rib(2)
    sta.add_web(1.6, 5)
    sta.add_stiffener(1.8, 18, 18)
    sta.add_compression_flange(8, 34, 18)
    sta.add_tension_flange(8, 34, 25)
    sta.add_rivet_stiffener(3.96875)
    sta.add_rivet_flange(3.96875, 6, 2)
    calc_all(sta)
    print("sta1500 mass", sta.get_total_mass())
    return sta


def make_sta2000():
    sta = Rib(3)
    sta.add_web(1.6, 5)
    sta.add_stiffener(1.8, 17, 17)
    sta.add_compression_flange(4, 18, 17)
    sta.add_tension_flange(5, 23, 25)
    sta.add_rivet_stiffener(3.96875)
    sta.add_rivet_flange(3.96875, 6, 1)
    calc_all(sta)
    print("sta2000 mass", sta.get_total_mass())
    return sta


def make_sta2500():
    sta = Rib(4)
    sta.add_web(1.6, 5)
    sta.add_stiffener(1.8, 18, 15)
    sta.add_compression_flange(4, 18, 16)
    sta.add_tension_flange(4, 18, 21)
    sta.add_rivet_stiffener(3.96875)
    sta.add_rivet_flange(3.96875, 6, 1)
    calc_all(sta)
    print("sta2500 mass", sta.get_total_mass())
    return sta


def make_sta3000():
    sta = Rib(5)
    sta.add_web(1.6, 4)
    sta.add_stiffener(1.8, 18, 11)
    sta.add_compression_flange(2.5, 23, 26)
    sta.add_tension_flange(2.5, 23, 26)
    sta.add_rivet_stiffener(3.96875)
    sta.add_rivet_flange(3.96875, 6, 1)
    calc_all(sta)
    print("sta3000 mass", sta.get_total_mass())
    return sta


def make_sta3500():
    sta = Rib(6)
    sta.add_web(1.6, 3)
    sta.add_stiffener(1.8, 17, 10)
    sta.add_compression_flange(2.5, 18, 22)
    sta.add_tension_flange(2.5, 18, 22)
    sta.add_rivet_stiffener(3.96875)
    sta.add_rivet_flange(3.96875, 6, 1)
    calc_all(sta)
    print("sta3500 mass", sta.get_total_mass())
    return sta


def make_sta4000():
    sta = Rib(7)
    sta.add_web(1.6, 3)
    sta.add_stiffener(1.8, 15, 6)
    sta.add_compression_flange(2, 12, 14)
    sta.add_tension_flange(2, 13, 13)
    sta.add_rivet_stiffener(3.125)
    sta.add_rivet_flange(2.38125, 6, 1)
    calc_all(sta)
    print("sta4000 mass", sta.get_total_mass())
    return sta


def make_sta4500():
    sta = Rib(8)
    sta.add_web(1.6, 2)
    sta.add_stiffener(1.27, 13, 7)
    sta.add_compression_flange(1.0, 12, 14)
    sta.add_tension_flange(1.0, 12, 14)
    sta.add_rivet_stiffener(3.125)
    sta.add_rivet_flange(2.38125, 6, 1)
    calc_all(sta)
    print("sta4500 mass", sta.get_total_mass())
    return sta


def main():
    init_header()
    sta625 = make_sta625()
    sta1000 = make_sta1000()
    sta1500 = make_sta1500()
    sta2000 = make_sta2000()
    sta2500 = make_sta2500()
    sta3000 = make_sta3000()
    sta3500 = make_sta3500()
    sta4000 = make_sta4000()
    sta4500 = make_sta4500()
    calc_stiffness(sta625, sta1000, sta1500, sta2000, sta2500, sta3000, sta3500, sta4000, sta4500)


if __name__ == '__main__':
    main()
