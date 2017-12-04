"""Frange(tension) implementation."""
# coding:utf-8
# Author: Shun Arahata
import math
import csv
from unit_convert import mm2inch, ksi2Mpa
from frange import Frange


class TensionFrange(Frange):
    """ Frange(Tension) class."""

    def __init__(self, thickness, b_bottome, b_height):
        """Constructor.

        :param thickness:フランジ厚さ
        :param b_bottom:フランジ底長さ
        :param b_height:フランジ高さ
        """
        super().__init__(thickness, b_bottome, b_height)

    def get_f_tu(self):
        """引張り許容応力 2024."""
        # cross section 云々は無視してます
        thickness_in_inch = mm2inch(self.thickness_)

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

    def get_ms(self, momentum, h_e, web_thickness):
        """ MS =Ftu/ft -1.

        :param momentum:前桁分担曲げモーメント
        :param h_e:桁フランジ分担曲げモーメント
        :param web_thickness:ウェブ厚さ
        """
        ms = self.get_f_tu() / self.get_stress_force(momentum, h_e, web_thickness) - 1
        return ms

    def make_row(self, writer, momentum, h_e, web_thickness):
        """ Make row of csv.

        :param cav_file:csv.writer()で取得されるもの
        :param momentum:前桁分担曲げモーメント
        :param h_e:桁フランジ断面重心距離
        :param web_thickness:ウェブ厚さ
        """
        ftu = self.get_f_tu()
        ms = self.get_ms(momentum, h_e, web_thickness)
        value = [web_thickness, momentum, self.thickness_,
                 self.b_bottom_, self.b_height_, ftu, ms]
        writer.writerow(value)

    def make_header(self, writer):
        """ Make Header of csv.

        :param cav_file:csv.writer()で取得されるもの
        """
        header = ["web_thickness[mm]", "momentum",
                  "thickness", "b_bottom_", "b_height", "Ftu", "M.S"]
        writer.writerow(header)


def main():
    """Test Function."""
    test = TensionFrange(6.60, 36, 42.5)
    f = test.get_stress_force(74623, 297, 2.03)
    print("fc[MPa]", f)
    MS = test.get_ms(74623, 297, 2.03)
    print("MS", MS)
    with open('test.csv', 'a') as f:
        writer = csv.writer(f)
        test.make_header(writer)
        test.make_row(writer, 74623, 297, 2.03)


if __name__ == '__main__':
    main()
