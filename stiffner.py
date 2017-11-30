#coding:utf-8
from scipy import interpolate
import numpy as np
import math
from unit_convert import *

class Stiffner(object):
    def __init__(self, thickness, bs1_bottome,bs2_height):
        """
        :param thickness: stiffner厚さ
        """
        self.thickness_=thickness
        self.bs1_bottom_=bs1_bottome
        self.bs2_height_=bs2_height
        self.E_=ksi2Mpa(10.3*10**3)

    def getInertia(self):
        first=self.bs1_bottom_*self.thickness_**3
        second=self.thickness_*self.bs2_height_**3
        third=self.thickness_**4
        inertia=1/3*(first+second+third)
        return inertia

    def getArea(self):
        return (self.bs1_bottom_+self.bs2_height_)*self.thickness_-1/4*self.thickness_**2


    def getInertiaU(self,he,de,t):
        """
        :param he: 桁フランジ断面重心距離
        :param de: スティフナー間隔
        :param t:ウェブ厚さ
        """
        x_value=he/de
        if x_value<1.0:
            return math.nan

        elif x_value<=4.0:
            x= np.array([1.0,1.5,2.0,2.5,3.0,3.5,4.0])
            y= np.array([0.1,0.6,1.5,2.5,3.7,4.8,6.2])
            f = interpolate.interp1d(x, y,kind='linear')
            fraction=f(x_value)
            denominator=he*t**3
            inertia_necessary=denominator*fraction
            return inertia_necessary

        else :
            return math.nan

    def getMS(self,he,de,t):
        """
        :param he 桁フランジ断面重心距離
        :param de: スティフナー間隔
        :param t:ウェブ厚さ
        """
        return self.getInertia()/self.getInertiaU(he,de,t)-1

    def getFcy(self):
        thickness_in_inch=mm2inch(self.thickness_)

        if thickness_in_inch<0.012:
            print("compression Frange getFcy error")
            return math.nan
        elif thickness_in_inch<0.040:
            return ksi2Mpa(61)

        elif thickness_in_inch<0.062:
            return ksi2Mpa(62)#上と同じ

        elif thickness_in_inch<0.187:
            return ksi2Mpa(64)

        elif thickness_in_inch<0.249:
            return ksi2Mpa(65)
        else:
            return math.nan

    def getXofGraph(self):
        bpert=self.bs1_bottom_/self.thickness_
        x_value=np.sqrt(self.getFcy()/self.E_)*bpert
        return x_value

    def getClipplingStress(self):
        """
        クリップリング応力を求める
        フランジと同じ
        :return Fcc:Fcc[MPa]
        """
        right_axis=self.getXofGraph()

        if right_axis<0.1:
            return math.nan
        elif right_axis<0.1*5**(27/33):
            #直線部分
            print("フランジ 直線部分")
            left_axis = 0.5*2**(2.2/1.5)
        elif right_axis<10:
            left_axis=10**(-0.20761)*right_axis**(-0.78427)
        else :
            return math.nan
        denom=mpa2Ksi(self.getFcy())#分母
        #print("left",left_axis)
        #print("denom",denom)
        numer=left_axis*denom
        Fcc = ksi2Mpa(numer)

        return Fcc



def test():
    fuck=Stiffner(2.29,22,19.0)
    print("Inertia",fuck.getInertia())
    print("inertia_necessary",fuck.getInertiaU(289,125,2.03))
    print("MS",fuck.getMS(289,125,2.03))
    print("FCC",fuck.getClipplingStress())

if __name__ == '__main__':
    test()
