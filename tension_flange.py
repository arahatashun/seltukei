"""Flange(tension) implementation."""
# coding:utf-8
# Author: Hirotaka Kondo
import math
import csv
from unit_convert import mm2inch, ksi2Mpa
from flange import Flange
from web import Web


class TensionFlange(Flange):
    """ Flange(Tension) class."""

    def __init__(self, thickness, b_bottom, b_height, web):
        """Constructor.
        :param thickness:フランジ厚さ
        :param b_bottom:フランジ底長さ
        :param b_height:フランジ高さ
        """
        super().__init__(thickness, b_bottom, b_height)
        self.web = web

    def get_f_tu(self):
        """
        引張り許容応力の計算.材料は2024-T3511
        p24の表3参照
        """
        # cross section 云々は無視してます
        thickness_in_inch = mm2inch(self.thickness)

        if thickness_in_inch < 0.249:
            return ksi2Mpa(57)

        elif thickness_in_inch < 0.499:
            return ksi2Mpa(60)

        elif thickness_in_inch < 0.749:
            return ksi2Mpa(60)  # 上と同じ

        elif thickness_in_inch < 1.499:
            return ksi2Mpa(65)

        elif thickness_in_inch < 2.999:
            return ksi2Mpa(70)

        elif thickness_in_inch < 4.499:
            return ksi2Mpa(70)
        else:
            return math.nan

    def get_ms(self, momentum, h_e):
        """ 安全余裕 MS =Ftu/ft -1.

        :param momentum:前桁分担曲げモーメント
        :param h_e:桁フランジ分担曲げモーメント
        """
        ms = self.get_f_tu() / self.get_stress_force(momentum, h_e, self.web.thickness) - 1
        return ms

    def make_row(self, writer, momentum, h_e):
        """ Make row of csv.

        :param writer:csv.writer()で取得されるもの
        :param momentum:前桁分担曲げモーメント
        :param h_e:桁フランジ断面重心距離
        """
        p = self.get_axial_force(momentum, h_e)
        a = self.get_area(self.web.thickness)
        ft = self.get_stress_force(momentum, h_e, self.web.thickness)
        ftu = self.get_f_tu()
        ms = self.get_ms(momentum, h_e)
        value = [self.web.y_left, self.web.y_right, self.web.thickness, momentum, self.thickness,
                 self.b_bottom, self.b_height, p, a, ft, ftu, ms]
        writer.writerow(value)

    def make_header(self, writer):
        """ Make Header of csv.

        :param writer:csv.writer()で取得されるもの
        """
        header = ["左端STA[mm]", "右端STA[mm]", "web_thickness[mm]", "momentum[N*m]", "tf[mm]", "b_bottom_f1[mm]",
                  "b_height_f2[mm]", "P[N]", "A[mm^2]", "ft[MPa]", "Ftu[MPa]", "M.S."]
        writer.writerow(header)


def main():
    """Test Function."""
    web2 = Web(625, 1000, 3, 2.03)
    test2 = TensionFlange(6.60, 36, 42.5, web2)
    with open('tension_flange_test.csv', 'a', encoding="Shift_JIS") as f:
        writer = csv.writer(f)
        test2.make_header(writer)
        test2.make_row(writer, 74623, 297)


if __name__ == '__main__':
    main()
