"""Rivet Base Class."""
# coding:utf-8
# Author: Shun Arahata
import numpy as np
from unit_convert import ksi2Mpa


class Rivet(object):
    """ Rivet Base Class."""

    def __init__(self, D):
        """Constructor.

        :param D:リベットの鋲径(直径mm)
        """
        self.D_ = D
        self.F_su_ = ksi2Mpa(30)  # とりあえずAD鋲を仮定

    """
    def getAD8(self,thickness):

        継手強度を求める
        :param thickness:板厚[inch]
        :return: 継手強度

        x=np.array([0.025+0.025*4/18,0.025+0.025*13/18,0.075,(0.2+0.175)/2])
        y=np.array([1000+200*12/16,1480,1550.1550])
        f=interpolate.interp1d(x, y,kind='linear')
    """

    def get_p_allow(self):
        """Pallow=pi/4*D^2*Fsu."""
        return np.pi / 4 * self.D_**2 * self.F_su_


def main():
    """Test Function."""
    r = Rivet(6.35)
    print("Pallow", r.get_p_allow())


if __name__ == '__main__':
    main()
