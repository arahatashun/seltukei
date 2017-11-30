#coding:utf-8
import scipy as sp
import numpy as np
import math
from unit_convert import *
from frange import Frange

class TensionFrange(Frange):
    def __init__(self,thickness, b_bottome,b_height):
        """
        :param thickness:フランジ厚さ
        :param b_bottom:フランジ底長さ
        :param b_height:フランジ高さ
        """
        super(TensionFrange, self).__init__(thickness, b_bottome,b_height)

    def getFtu(self):
        #cross section 云々は無視してます
        thickness_in_inch=mm2inch(self.thickness_)

        if thickness_in_inch<0.249:
            return ksi2Mpa(57)

        elif thickness_in_inch<0.499:
            return ksi2Mpa(60)

        elif thickness_in_inch<0.749:
            return ksi2Mpa(60)#上と同じ

        elif thickness_in_inch<1.499:
            return ksi2Mpa(65)

        elif thickness_in_inch<2.999:
            return ksi2Mpa(70)

        elif thickness_in_inch<4.499:
            return ksi2Mpa(70)
        else:
            return math.nan

    def getMS(self,momentum,h_e,web_thickness):
        ms=self.getFtu()/self.getStressForce(momentum,h_e,web_thickness)-1
        return ms


def test_tension():
    test=TensionFrange(6.60,36,42.5)
    A=test.getArea(2.03)
    print("A",A)
    cofg=test.getCenterOfGravity()
    print("cofg",cofg)
    ax=test.getAxialForce(74623,297)
    print("P[N]",ax)
    f=test.getStressForce(74623,297,2.03)
    print("fc[MPa]",f)
    MS=test.getMS(74623,297,2.03)
    print("MS",MS)


if __name__ == '__main__':
    test_tension()
