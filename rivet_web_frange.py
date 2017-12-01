# coding:utf-8
# Author: Shun Arahata
from scipy import interpolate
import numpy as np
import math
import csv
from unit_convert import *
from rivet import Rivet
from web import Web


class RivetWebFrange(Rivet):
    """
    ウェブフランジ結合のリベット
    """

    def __init__(self, D, pd_ratio, N, web):
        """
        :param D:リベットの鋲径
        :param pd_ration:リベットピッチ/リベットの鋲半径,一般に4D~6Dとすることが多い
        :param N:リベット列数
        :param web:結合されるweb
        """
        super(RivetWebFrange, self).__init__(D)
        self.p1_ = D * pd_ratio
        self.N_ = N
        self.web_ = web

    def getShearForce(self, Sf, he):
        """
        Ps=qmax*p/Nを返す
        :param Sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離
        """
        qmax = Sf / he
        Ps = qmax * self.p1_ / self.N_
        return Ps

    def getMS(self, Sf, he):
        """
        :param Sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離
        """

        qmax = Sf / he
        Pallow = self.getPallow()
        Ps = self.getShearForce(Sf, he)
        ms = Pallow / Ps
        return ms

    def getWebMS(self, Sf, he):
        """
        ウェブホールロスの計算
        :param Sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離
        """
        return self.web_.getWebHoleLossMS(self.p1_, self.D_, Sf, he)

    def makerow(self, writer, Sf, he):
        """
        :param cav_file:csv.writer()で取得されるもの
        :param Sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離
        """
        Ps = self.getShearForce(Sf, he)
        ms = self.getMS(Sf, he)
        ms_web_hole = self.getWebMS(Sf, he)
        value = [Sf / he * 1000, self.N_, self.D_,
                 self.p1_, Ps, ms, ms_web_hole]
        writer.writerow(value)

    def makeheader(self, writer):
        """
        :param cav_file:csv.writer()で取得されるもの
        """
        header = ["qmax", "N", "D", "pitch", "Ps", "M.S", "M.S.web hole loss"]
        writer.writerow(header)


def test():
    unti = Web(2.03, 286, 125)
    test = RivetWebFrange(3.175, 19.05, 2, unti)
    with open('test.csv', 'a') as f:
        writer = csv.writer(f)
        test.makeheader(writer)
        test.makerow(writer, 38429, 297)


if __name__ == '__main__':
    test()
