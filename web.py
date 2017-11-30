#coding:utf-8
from scipy import interpolate
import numpy as np
import math
from unit_convert import *

class Web(object):
    def __init__(self, thickness, height_a,width_b):
        """
        :param thickness:web厚さ
        :param height_a:前桁高さ
        :param width_b:間隔de
        """
        self.thickness_=thickness
        self.height_a_=height_a
        self.width_b_=width_b


    def getShearForce(self,q_max):#fs
        return q_max/self.thickness_/1000

    def getYoungModulus(self):
        return ksi2Mpa(10.3*1000)

    def getK(self):
        x_axis=self.height_a_/self.width_b_
        if x_axis<0.9:
            print("x_axis",x_axis)
            return math.nan
        elif x_axis<12:
            x= np.array([0.9,1.5, 2,   3,4,  5,  8,12])
            y= np.array([ 11,6.2,5.8,5.3,5.1  , 5,4.8,4.8])
            f = interpolate.interp1d(x, y,kind='linear')
            k=f(x_axis)
            print("k",k)
            return k
        else:
            print("x_axis",x_axis)
            return math.nan


    def getBucklingShearForce(self):
        return self.getK()*self.getYoungModulus()*(self.thickness_/self.width_b_)**2

    def getMS(self,qmax):
        return self.getBucklingShearForce()/self.getShearForce(qmax)-1


    def getWebHoleLossMS(self,p,d,q_max):
        """
        ウェブホールロスの計算
        :param p:リベット間隔
        :param d:リベットの直径[mm]
        """
        f_sj=self.getShearForce(q_max)*p/(p-d)
        #print(f_sj)
        ms=self.getBucklingShearForce()/f_sj-1
        print("ms",ms)
        return ms



"""
def test():
    unti=Web(2.03,286,125)
    print("fs",unti.getShearForce(129410))
    print("F_scr",unti.getBucklingShearForce())
    print("K",unti.getK())
    print("MS",unti.getMS(129410))

if __name__ == '__main__':
    test()
"""
