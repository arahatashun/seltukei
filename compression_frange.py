#coding:utf-8
import scipy as sp
import numpy as np
import math
from unit_convert import *
from frange import Frange


class CompressionFrange(Frange):

    def __init__(self,thickness, b_bottome,b_height):
        """
        :param thickness:フランジ厚さ
        :param b_bottom:フランジ底長さ
        :param b_height:フランジ高さ
        """
        super(CompressionFrange, self).__init__(thickness, b_bottome,b_height)
        self.E=ksi2Mpa(10.3*10**3)

    def getFcy(self):
        thickness_in_inch=mm2inch(self.thickness_)

        if thickness_in_inch<0.012:
            print("compression Frange getFcy error")
            return NaN
        elif thickness_in_inch<0.040:
            return ksi2Mpa(61)

        elif thickness_in_inch<0.062:
            return ksi2Mpa(62)#上と同じ

        elif thickness_in_inch<0.187:
            return ksi2Mpa(64)

        elif thickness_in_inch<0.249:
            return ksi2Mpa(65)
        else:
            return NaN

        #b/t
    def getBperT(self):
        return self.b_bottom_/self.thickness_

    def getXofGraph(self):
        return np.sqrt(self.getFcy()/self.E)*self.getBperT()

    def getFcc(self):
        right_axis=self.getXofGraph()
        denom=self.getFcy()#分母

        if right_axis<0.1*5**(27/33):
            #直線部分
            print("フランジ 直線部分")
            left_axis = 0.5*2**(2.2/1.5)
        else :
            left_axis=10**(-0.20761)*right_axis**(-0.78427)
        denom=mpa2Ksi(self.getFcy())#分母
        #print("left",left_axis)
        #print("denom",denom)
        numer=left_axis*denom
        Fcc = ksi2Mpa(numer)

        return Fcc

    def getMS(self,momentum,h_e,web_thickness):
        ms=self.getFcc()/self.getStressForce(momentum,h_e,web_thickness)-1
        return ms

def test_compression():
    test=CompressionFrange(6.0,34.5,34.5)

    A=test.getArea(2.03)
    print("A",A)
    cofg=test.getCenterOfGravity()
    print("cofg",cofg)
    ax=test.getAxialForce(74623,297)
    print("P[N]",ax)
    f=test.getStressForce(74623,297,2.03)
    x=test.getXofGraph()
    print("x",x)
    bpert=test.getBperT()
    print("bpert",bpert)
    print("fc[MPa]",f)

    fcc=test.getFcc()
    print("fcc",fcc)
    ms=test.getMS(74623,297,2.03)
    print("MS",ms)

if __name__ == '__main__':
    test_compression()
