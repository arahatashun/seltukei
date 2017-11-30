#coding:utf-8
from scipy import interpolate
import numpy as np
import math
from unit_convert import *
from rivet import Rivet

class RivetWebFrange(Rivet):
    """
    ウェブフランジ結合のリベット
    """

    def  __init__(self,D,pd_ration,N,web):
        """
        :param D:リベットの鋲径
        :param pd_ration:リベットピッチ/リベットの鋲半径,一般に4D~6Dとすることが多い
        :param N:リベット列数
        :param :結合されるweb
        """
        super(RivetWebFrange, self).__init__(D)
        self.p1_=D*pd_ration
        self.N_=N
        self.web_=web



    def getShearForce(self,qmax):
        """
        Ps=qmax*p/Nを返す
        :param: qmax
        """
        Ps=qmax*self.p1_/self.N_
        return Ps

    def getMS(self,qmax):
        Pallow=self.getPallow()
        Ps=self.getShearForce(qmax)
        ms=Pallow/Ps
        return ms

    def calcWebMS(self,qmax):
        return self.web_.getWebHoleLossMS(self.p1_,self.D_,qmax)

def test():
    test=RivetWebFrange(3.175,19.05,2)
    print("test",test.getMS(129410))

if __name__ == '__main__':
    test()
