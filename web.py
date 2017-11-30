#coding:utf-8
# Author: Shun Arahata
from scipy import interpolate
import numpy as np
import math
from unit_convert import *
import csv

class Web(object):
    def __init__(self, thickness, height_a,width_b):
        """
        :param thickness:web厚さ
        :param height_a:前桁高さ
        :param width_b:ウェブの長さ(stiffnerで殺されるのでstiffnerの間隔と同じ)
        height width長い方をaとするがアルゴリズム的に問題なし
        """
        self.thickness_=thickness
        self.height_a_=height_a
        self.width_b_=width_b

    def getQmax(self,Sf,he):
        """
        :param Sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離[mm]
        """
        q_max=Sf/he*1000
        return q_max

    def getShearForce(self,Sf,he):
        """
        ウェブ剪断応力fs
        :param Sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離
        """
        q_max=self.getQmax(Sf,he)
        return q_max/self.thickness_/1000

    def getYoungModulus(self):
        return ksi2Mpa(10.3*1000)

    def getK(self):
        x_axis=self.height_a_/self.width_b_
        if x_axis<1:
            x_axis=1/x_axis
        if x_axis<12:
            x= np.array([0.9,1.5, 2,   3,4,  5,  8,12])
            y= np.array([ 11,6.2,5.8,5.3,5.1  , 5,4.8,4.8])
            f = interpolate.interp1d(x, y,kind='linear')
            k=f(x_axis)
            print("k",k)
            return k
        else:
            print("x_axis",x_axis)
            print("x_axis is too large :in getK in web.py")
            return math.nan


    def getBucklingShearForce(self):
        """
        剪断座屈応力Fscr
        """
        return self.getK()*self.getYoungModulus()*(self.thickness_/self.width_b_)**2

    def getFsu(self):
        """
        表3のF_su
        """

        thickness_in_inch=mm2inch(self.thickness_)
        if thickness_in_inch<0.011:
            print("too small:nan in getFsu in web.py")
            return math.nan
        elif thickness_in_inch<0.039:
            return ksi2Mpa(42)
        elif thickness_in_inch<0.062:
            return ksi2Mpa(42)
        elif thickness_in_inch<0.187:
            return ksi2Mpa(44)
        elif thickness_in_inch<0.000249:
            return ksi2Mpa(45)
        else:
            print("too large :nan in getFsu in web.py")
            return math.nan


    def getMS(self,Sf,he):
        """
        安全率
        :param Sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離
        """
        #F_SUを無視してる
        f_scr=self.getBucklingShearForce()
        f_su=self.getFsu()
        ms = min(f_su,f_scr)/self.getShearForce(Sf,he)-1
        #print(ms)
        return ms


    def getWebHoleLossMS(self,p,d,Sf,he):
        """
        ウェブホールロスの計算
        :param p:リベット間隔
        :param d:リベットの直径[mm]
        :param Sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離
        """

        f_sj=self.getShearForce(Sf,he)*p/(p-d)
        #print(f_sj)
        ms=self.getFsu()/f_sj-1
        print("ms",ms)
        return ms

    def makerow(self,writer,Sf,he):
        """
        :param cav_file:csv.writer()で取得されるもの
        :param Sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離
        """
        fs=self.getShearForce(Sf,he)
        Fscr=self.getBucklingShearForce()
        ms=self.getMS(Sf,he)
        value=[self.thickness_,self.height_a_,self.width_b_,fs,Fscr,ms]
        writer.writerow(value)


    def makeheader(self,writer):
        """
        :param cav_file:csv.writer()で取得されるもの
        """
        header=["web_thickness[mm]","前桁高さ","間隔de","fs","Fscr","M.S"]
        writer.writerow(header)



def test():
    unti=Web(2.03,286,125)
    with open('test.csv','a') as f:
        writer = csv.writer(f)
        unti.makeheader(writer)
        unti.makerow(writer,38429,297)

if __name__ == '__main__':
    test()
