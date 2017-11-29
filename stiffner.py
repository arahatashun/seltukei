#coding:utf-8
from scipy import interpolate
import numpy as np
import math
from unit_convert import *

class Stiffner(object):
    def __init__(self, thickness, bs1_bottome,bs2_height):
        self.thickness_=thickness#stiffner厚さ
        self.bs1_bottom_=bs1_bottome
        self.bs2_height_=bs2_height

    def getInertia(self):
        first=self.bs1_bottom_*self.thickness_**3
        second=self.thickness_*self.bs2_height_**3
        third=self.thickness_**4
        inertia=1/3*(first+second+third)
        return inertia


    def getInertiaU(self,he,de,t):
        """
        :param he 桁フランジ断面重心距離
        :param de: スティフナー間隔
        :param t:ウェブ厚さ
        """
        x_value=he/de
        if x_value<1.0:
            return NaN

        elif x_value<=4.0:
            x= np.array([1.0,1.5,2.0,2.5,3.0,3.5,4.0])
            y= np.array([0.1,0.6,1.5,2.5,3.7,4.8,6.2])
            f = interpolate.interp1d(x, y,kind='linear')
            fraction=f(x_value)
            denominator=he*t**3
            inertia_necessary=denominator*fraction
            return inertia_necessary

        else :
            return NaN

    def getMS(self,he,de,t):
        """
        :param he 桁フランジ断面重心距離
        :param de: スティフナー間隔
        :param t:ウェブ厚さ
        """
        return self.getInertia()/self.getInertiaU(he,de,t)-1


"""
def test():
    fuck=Stiffner(2.29,22,19.0)
    print("Inertia",fuck.getInertia())
    print("inertia_necessary",fuck.getInertiaU(289,125,2.03))
    print("MS",fuck.getMS(289,125,2.03))

if __name__ == '__main__':
    test()
"""
