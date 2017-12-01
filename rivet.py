# coding:utf-8
# Author: Shun Arahata
from scipy import interpolate
import numpy as np
import math
from unit_convert import *


class Rivet(object):
    """
    Rivetのsupser class
    AD鋲のみに対応
    """

    def __init__(self, D):
        """
        :param D:リベットの鋲径
        """
        self.D_ = D
        self.F_su_ = ksi2Mpa(30)
        #:ファスナ船団許容応力

    """
    def getAD8(self,thickness):

        継手強度を求める
        :param thickness:板厚[inch]
        :return: 継手強度

        x=np.array([0.025+0.025*4/18,0.025+0.025*13/18,0.075,(0.2+0.175)/2])
        y=np.array([1000+200*12/16,1480,1550.1550])
        f=interpolate.interp1d(x, y,kind='linear')
    """

    def getPallow(self):
        return np.pi / 4 * self.D_**2 * self.F_su_


def test():
    r = Rivet(3.175)
    print("Pallow", r.getPallow())


if __name__ == '__main__':
    test()
