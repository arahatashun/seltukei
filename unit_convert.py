""" unit conver functions."""
# coding:utf-8
# Author: Shun Arahata
import numpy as np
from scipy import interpolate


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

