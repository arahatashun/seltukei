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
from rib import Rib

def init_header():
    """header 作成"""
    # delete
    directory = 'results/'
    test = os.listdir( directory )
    for item in test:
        if item.endswith(".csv"):
            os.remove( os.path.join( directory, item ) )
    # header
    make_web_header()
    make_stiffener_header()
    make_tflange_header()
    make_cflange_header()
    rivet_wf_make_all_header()
    rivet_ws_make_all_header()

def make_sta625():
    sta = Rib(0)
    sta.add_web(1.60, 4)
    sta.add_stiffener(1.27, 40, 30)
    sta.add_compression_flange(6.5, 45, 40)
    sta.add_tension_flange(6.5, 50, 40)
    sta.add_rivet_stiffener(6.35)
    sta.add_rivet_flange(6.35,6,2)
    sta.add_rivet_stiffener(6.35)
    he = sta.set_he()
    sta.web_csv()
    sta.tflange_csv()
    sta.cflange_csv()
    sta.stiffener_csv()
    sta.rivet_stiffener_csv()
    sta.rivet_flange_csv()
    print("sta625 volume", sta.get_total_volume())

def make_sta3000():
    sta = Rib(5)
    sta.add_web(1.27, 7)
    sta.add_stiffener(1.02, 30, 20)
    sta.add_compression_flange(3, 35, 30)
    sta.add_tension_flange(3, 30, 25)
    sta.add_rivet_stiffener(6.35)
    sta.add_rivet_flange(6.35,6,2)
    sta.add_rivet_stiffener(6.35)
    he = sta.set_he()
    sta.web_csv()
    sta.tflange_csv()
    sta.cflange_csv()
    sta.stiffener_csv()
    sta.rivet_stiffener_csv()
    sta.rivet_flange_csv()


def main():
    init_header()
    make_sta625()
    make_sta3000()

if __name__ == '__main__':
    main()
