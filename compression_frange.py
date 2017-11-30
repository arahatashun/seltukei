#coding:utf-8
# Author: Shun Arahata
import scipy as sp
import numpy as np
import math
from unit_convert import *
from frange import Frange
import csv


class CompressionFrange(Frange):

    def __init__(self,thickness, b_bottome,b_height):
        """
        :param thickness:フランジ厚さ
        :param b_bottom:フランジ底長さ
        :param b_height:フランジ高さ
        """
        super(CompressionFrange, self).__init__(thickness, b_bottome,b_height)
        self.E_=ksi2Mpa(10.3*10**3)

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

        #b/t
    def getBperT(self):
        return self.b_bottom_/self.thickness_

    def getXofGraph(self):
        return np.sqrt(self.getFcy()/self.E_)*self.getBperT()

    def getFcc(self):
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

    def getMS(self,momentum,h_e,web_thickness):
        ms=self.getFcc()/self.getStressForce(momentum,h_e,web_thickness)-1
        return ms

    def makerow(self,writer,momentum,h_e,web_thickness):
        """
        :param cav_file:csv.writer()で取得されるもの
        :param momentum:前桁分担曲げモーメント
        :param h_e:桁フランジ断面重心距離
        :param web_thickness:ウェブ厚さ
        """
        fcc=self.getFcc()
        ms=self.getMS(momentum,h_e,web_thickness)
        value=[web_thickness,momentum,self.thickness_,self.b_bottom_,self.b_height_,fcc,ms]
        writer.writerow(value)


    def makeheader(self,writer):
        """
        :param cav_file:csv.writer()で取得されるもの
        """
        header=["web_thickness[mm]","momentum","thickness","b_bottom_","b_height","Fcc","M.S"]
        writer.writerow(header)



def test_compression():
    test=CompressionFrange(6.0,34.5,34.5)
    with open('test.csv','a') as f:
        writer = csv.writer(f)
        test.makeheader(writer)
        test.makerow(writer,74623,297,2.03)

    """
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

if __name__ == '__main__':
    test_compression()
