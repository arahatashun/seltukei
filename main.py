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
    sta625 = Rib(0)
    sta625.add_web(1.60, 4)
    sta625.add_stiffener(1.27, 40, 30)
    sta625.add_compression_flange(5.0, 50, 40)
    sta625.add_tension_flange(5.0, 50, 40)
    sta625.add_rivet_stiffener(6.35)
    sta625.add_rivet_flange(6.35,4,2)
    sta625.add_rivet_stiffener(6.35)
    he = sta625.set_he()
    sta625.web_csv()
    sta625.tflange_csv()
    sta625.cflange_csv()
    sta625.stiffener_csv()
    sta625.rivet_stiffener_csv()
    sta625.rivet_flange_csv()

def main():
    init_header()
    make_sta625()

if __name__ == '__main__':
    main()
