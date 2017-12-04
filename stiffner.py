"""stiffner implementation"""
# coding:utf-8
# Author: Shun Arahata
from scipy import interpolate
import numpy as np
import math
from unit_convert import ksi2Mpa, mm2inch, mpa2Ksi
import csv


class Stiffner(object):
    """Stiffner class."""

    def __init__(self, thickness, bs1_bottom, bs2_height):
        """Constructor.

        :param thickness: stiffner厚さ
        :param bs1_bottom:stiffner bottom長さ
        :param bs2_height:stiffner 高さ
        """
        self.thickness_ = thickness
        self.bs1_bottom_ = bs1_bottom
        self.bs2_height_ = bs2_height
        self.E_ = ksi2Mpa(10.3 * 10**3)

    def get_inertia(self):
        """Inertia of Stiffner."""
        first = self.bs1_bottom_ * self.thickness_**3
        second = self.thickness_ * self.bs2_height_**3
        third = -self.thickness_**4
        inertia = 1 / 3 * (first + second + third)
        return inertia

    def get_area(self):
        """ Stiffner断面積."""
        return (self.bs1_bottom_ + self.bs2_height_) * self.thickness_ - self.thickness_**2

    def get_inertia_u(self, he, de, t):
        """ Get Necessary Intertia.

        :param he: 桁フランジ断面重心距離
        :param de: スティフナー間隔
        :param t:ウェブ厚さ
        """
        x_value = he / de
        if x_value < 1.0:
            print("too small in getIntertialU in stiffner py")
            return math.nan

        elif x_value <= 4.0:
            x = np.array([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
            y = np.array([0.1, 0.6, 1.5, 2.5, 3.7, 4.8, 6.2])
            f = interpolate.interp1d(x, y, kind='linear')
            fraction = f(x_value)
            denominator = he * t**3
            inertia_necessary = denominator * fraction
            return inertia_necessary

        else:
            print("too large in getIntertialU in stiffner py")
            return math.nan

    def get_ms(self, he, de, t):
        """ MS (I>IU)
        :param he 桁フランジ断面重心距離
        :param de: スティフナー間隔
        :param t:ウェブ厚さ
        """
        return self.get_inertia() / self.get_inertia_u(he, de, t) - 1

    def get_fcy(self):
        """ F_cy of 7075."""
        thickness_in_inch = mm2inch(self.thickness_)

        if thickness_in_inch < 0.012:
            print("stiffner thickness too small")
            return math.nan
        elif thickness_in_inch < 0.040:
            return ksi2Mpa(61)

        elif thickness_in_inch < 0.062:
            return ksi2Mpa(62)  # 上と同じ

        elif thickness_in_inch < 0.187:
            return ksi2Mpa(64)

        elif thickness_in_inch < 0.249:
            return ksi2Mpa(65)
        else:
            print("too large in getFcy in stiffner py")
            return math.nan

    def get_x_of_graph(self):
        """Get X of Graph 7075(in page 12)."""

        bpert = self.bs1_bottom_ / self.thickness_  # b/t
        x_value = np.sqrt(self.get_fcy() / self.E_) * bpert
        return x_value

    def get_clippling_stress(self):
        """
        クリップリング応力を求める
        フランジと同じ
        :return Fcc:Fcc[MPa]
        """
        right_axis = self.get_x_of_graph()

        if right_axis < 0.1:
            return math.nan
        elif right_axis < 0.1 * 5**(27 / 33):
            # 直線部分
            left_axis = 0.5 * 2**(2.2 / 1.5)
        elif right_axis < 10:
            left_axis = 10**(-0.20761) * right_axis**(-0.78427)
        else:
            return math.nan
        denom = mpa2Ksi(self.get_fcy())  # 分母
        # print("left",left_axis)
        # print("denom",denom)
        numer = left_axis * denom
        Fcc = ksi2Mpa(numer)

        return Fcc

    def make_row(self, writer, he, de, t):
        """
        :param cav_file:csv.writer()で取得されるもの
        :param de:スティフナー間隔
        :param h_e:桁フランジ断面重心距離
        :param t:ウェブ厚さ
        """
        I_U = self.get_inertia_u(he, de, t)
        I = self.get_inertia()
        ms = self.get_ms(he, de, t)
        value = [t, self.thickness_, de, he,
                 self.bs1_bottom_, self.bs2_height_, I, I_U, ms]
        writer.writerow(value)

    def make_header(self, writer):
        """ Make csv header.
        :param cav_file:csv.writer()で取得されるもの
        """
        header = ["web_thickness[mm]", "スティフナー厚さ", "スティフナー間隔",
                  "he", "bs1底", "bs2高さ", "I", "I_U", "M.S"]
        writer.writerow(header)


def main():
    """Test Function."""
    fuck = Stiffner(2.29, 22, 19.0)
    with open('test.csv', 'a') as f:
        writer = csv.writer(f)
        fuck.make_header(writer)
        fuck.make_row(writer, 289, 125, 2.03)


if __name__ == '__main__':
    main()
