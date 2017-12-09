"""main"""

# -*- coding: utf-8 -*-
# Author: Shun Arahata,Hirotaka Kondo
from web import make_web_header
from stiffener import make_stiffener_header
from tension_flange import make_tflange_header
from compression_flange import make_cflange_header
from rivet_web_stiffener import rivet_ws_make_all_header
from rivet_web_flange import rivet_wf_make_all_header

def init_header():
    """header 作成"""
    make_web_header()
    make_stiffener_header()
    make_cflange_header()
    rivet_wf_make_all_header()
    rivet_ws_make_all_header()

def main():
    init_header()

if __name__ == '__main__':
    main()
