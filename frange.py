#coding:utf-8
import scipy as sp
import numpy as np
import math
from unit_convert import *

class Frange:
    def __init__(self, thickness, b_bottome,b_height):
        self.thickness_=thickness
        self.b_bottom_=b_bottome
        self.b_height_=b_height

    def getArea(self,web_thickness):
        return (self.b_bottom_+self.b_height_)*self.thickness_+web_thickness**2*30

    #取り付け場所からのheを求めるための排除長さ
    def getCenterOfGravity(self):
        area=(self.b_bottom_+self.b_height_)*self.thickness_
        bottom_area=(self.b_bottom_+self.thickness_/2)*self.thickness_
        residure=area/2-bottom_area

        if(residure<0):
            #print("residure<0")
            return area/2/(self.b_bottom_+self.thickness_/2)
        else:
            return self.b_bottom_+residure/self.thickness_

    def getAxialForce(self,momentum,h_e):
        #単位[N]
        return momentum/h_e*1000

    #f_c,f_t
    def getStressForce(self,momentum,h_e,web_thickness):
        #[MPa]
        return self.getAxialForce(momentum,h_e)/self.getArea(web_thickness)


"""
def test_frange():
    test=Frange(6.0,34.5,34.5)
    A=test.getArea(2.03)
    print("A",A)
    cofg=test.getCenterOfGravity()
    print("cofg",cofg)
    ax=test.getAxialForce(74623,297)
    print("P[N]",ax)
    f=test.getStressForce(74623,297,2.03)
    print("fc[MPa]",f)
"""

class CompressionFrange(Frange):

    def __init__(self,thickness, b_bottome,b_height):
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
"""
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
"""


class TensionFrange(Frange):
    def __init__(self,thickness, b_bottome,b_height):
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
            return NaN

    def getMS(self,momentum,h_e,web_thickness):
        ms=self.getFtu()/self.getStressForce(momentum,h_e,web_thickness)-1
        return ms

"""
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
"""
