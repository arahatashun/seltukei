#coding:utf-8
# Author: Shun Arahata
import scipy as sp
import numpy as np
import math
from unit_convert import *

class Frange:
    def __init__(self, thickness, b_bottome,b_height):
        """
        :param thickness:フランジ厚さ
        :param b_bottom:フランジ底長さ
        :param b_height:フランジ高さ
        """
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
        """
        :param momentum:前桁負担分モーメント
        :param h_e:桁フランジ断面重心距離
        :return axialforce: [N]
        """
        axialforce=momentum/h_e*1000
        return axialforce

    #f_c,f_t
    def getStressForce(self,momentum,h_e,web_thickness):
        """
        :param momentum:前桁分担曲げモーメント
        :param h_e:桁フランジ断面重心距離
        :param web_thickness:ウェブ厚さ
        """
        #[MPa]
        return self.getAxialForce(momentum,h_e)/self.getArea(web_thickness)



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


if __name__ == '__main__':
    test_frange()
