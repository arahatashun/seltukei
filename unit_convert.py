""" unit conver functions　and other functions."""
# coding:utf-8
# Author: Shun Arahata
import numpy as np
from scipy import interpolate
from math import log10, floor

def ksi2Mpa(ksi):
    return ksi * 6.89475908677537


def inch2mm(inch):
    return 25.4 * inch


def mm2inch(mm):
    return mm * 0.0393701


def mpa2Ksi(pa):
    return pa / 6.89475908677537


def lbs2N(lbs):
    return 4.4482216282509 * lbs


def get_hf(sta):
    """前桁高さ取得関数.
    
    :param sta: staの値
    :return hf: 前桁高さ
    """
    x = np.array([625, 5000])
    y = np.array([320, 130])
    f = interpolate.interp1d(x, y, kind='linear')
    hf = f(sta)
    return hf


def round_sig(x, sig=3):
    """有効数字.
    https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python
    """
    return round(x, sig - int(floor(log10(abs(x)))) - 1)

def round_list(*args, sig=3):
    """有効数字.

    https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python
    """
    absolute = np.abs(args)
    floored_num = np.floor(np.log10(absolute))
    digits = sig - np.trunc(floored_num) - 1
    return np.round(args, decimals = sig)


def main():
    q = 1.44444
    print(round_sig(q, sig =3))


if __name__ == '__main__':
    main()
