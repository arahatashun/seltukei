"""stiffener implementation"""
# coding:utf-8
# Author: Shun Arahata
from scipy import interpolate
import numpy as np
import math
from unit_convert import ksi2Mpa, mm2inch, mpa2Ksi, get_hf, round_sig
from web import Web
import csv


class Stiffener(object):
    """Stiffener class."""

    def __init__(self, thickness, bs1_bottom, bs2_height, web):
        """Constructor.

        :param thickness: stiffener厚さ[mm]
        :param bs1_bottom:stiffener bottom長さ[mm]
        :param bs2_height:stiffener 高さ[mm]
        :param web:このstiffenerが属するwebのクラス
        """
        self.thickness = thickness
        self.bs1_bottom = bs1_bottom
        self.bs2_height = bs2_height
        self.E = ksi2Mpa(10.3 * 10 ** 3)
        self.web = web

    def get_inertia(self):
        """
        Inertia of Stiffener.[mm^4]
        """
        first = self.bs1_bottom * self.thickness ** 3
        second = self.thickness * self.bs2_height ** 3
        third = -self.thickness ** 4
        inertia = 1 / 3 * (first + second + third)
        return inertia

    def get_area(self):
        """ Stiffener断面積.[mm^2]"""
        return (self.bs1_bottom + self.bs2_height) * self.thickness - self.thickness ** 2

    def get_inertia_u(self, he):
        """
        Get Necessary Inertia.
        p11の表参照
        :param he: 桁フランジ断面重心距離[mm]
        """
        de = self.web.width_b  # webのwidth_bとdeは同一
        t = self.web.thickness  # webの厚さ[mm]
        x_value = he / de
        """
        どうしても1未満のところがほしいので
        原点から勝手に補完直線引くようにした
        if x_value < 1.0:
            print("too small to get Inertia U in stiffener.py")
            return math.nan
        """
        if x_value <= 4.0:
            x = np.array([0, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
            y = np.array([0, 0.1, 0.6, 1.5, 2.5, 3.7, 4.8, 6.2])
            f = interpolate.interp1d(x, y, kind='linear')
            fraction = f(x_value)
            denominator = he * t ** 3
            inertia_necessary = denominator * fraction
            return inertia_necessary

        else:
            print("too large to get Inertia U in stiffener.py")
            return math.nan

    def get_ms(self, he):
        """ MS (I>IU)
        :param he 桁フランジ断面重心距離
        """
        return self.get_inertia() / self.get_inertia_u(he) - 1

    def get_fcy(self):
        """ F_cy of 7075."""
        thickness_in_inch = mm2inch(self.thickness)

        if thickness_in_inch < 0.012:
            print("stiffener thickness too small")
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
            print("too large in getFcy in stiffener py")
            return math.nan

    def get_x_of_graph(self):
        """Get X of Graph 7075(in page 12)."""

        b_per_t = self.bs1_bottom / self.thickness  # b/t
        x_value = np.sqrt(self.get_fcy() / self.E) * b_per_t
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
        elif right_axis < 0.1 * 5 ** (27 / 33):
            # 一定部分
            left_axis = 0.5 * 2 ** (2.2 / 1.5)
        elif right_axis < 10:
            left_axis = 10 ** (-0.20761) * right_axis ** (-0.78427)
        else:
            return math.nan
        lower = mpa2Ksi(self.get_fcy())  # 分母
        upper = left_axis * lower
        Fcc = ksi2Mpa(upper)

        return Fcc

    def make_row(self, he):
        """
        :param writer:csv.writer()で取得されるもの
        :param he:桁フランジ断面重心距離
        """
        I_U = self.get_inertia_u(he)
        I = self.get_inertia()
        ms = self.get_ms(he)
        value = [self.web.y_left, self.web.y_right, self.web.thickness, self.web.width_b, he, self.thickness,
                 self.bs1_bottom, self.bs2_height, I, I_U, ms]
        with open('results/stiffener.csv', 'a', encoding="utf-8") as f:
            writer = csv.writer(f)
            round_value = map(lambda x: round_sig(x), value)
            writer.writerow(round_value)

    def get_volume(self):
        """
        stiffenerの体積を計算する
        self.web.divisionが1のときはstiffener0個なので体積0となる
        :return: volume[mm^3]
        """
        area = (self.bs1_bottom + self.bs2_height) * self.thickness - self.thickness ** 2  # [mm^2]
        height = (get_hf(self.web.y_left) + get_hf(self.web.y_right)) / 2  # [mm]
        return area * height * (self.web.division - 1) / 1000  # [cm^3]


def make_stiffener_header():
    """
    Make csv header.

    """
    header = ["左端STA[mm]", "右端STA[mm]", "web thickness[mm]", "スティフナー間隔de[mm]", "he[mm]", "スティフナー厚さts[mm]",
              "bs1 bottom[mm]", "bs2 height[mm]", "I[${mm}^4$]", "$I_U$[${mm}^4$]", "M.S."]
    with open('results/stiffener.csv', 'a', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)


def main():
    """Test Function."""
    web = Web(625, 1000, 3, 2.03)
    test = Stiffener(2.29, 22, 19.0, web)
    make_stiffener_header()
    test.make_row(289)


if __name__ == '__main__':
    main()
