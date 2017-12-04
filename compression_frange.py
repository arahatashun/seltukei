"""Frange(compression) implementation."""
# coding:utf-8
# Author: Shun Arahata
import numpy as np
import math
from unit_convert import ksi2Mpa, mm2inch, mpa2Ksi
from frange import Frange
import csv


class CompressionFrange(Frange):
    """Frange (Complesstion) Class."""

    def __init__(self, thickness, b_bottome, b_height):
        """ Constructor.

        :param thickness:フランジ厚さ
        :param b_bottom:フランジ底長さ
        :param b_height:フランジ高さ
        """
        super().__init__(thickness, b_bottome, b_height)
        self.E_ = ksi2Mpa(10.3 * 10**3)

    def get_fcy(self):
        """Get fcy og 7075."""
        thickness_in_inch = mm2inch(self.thickness_)

        if thickness_in_inch < 0.012:
            print("compression Frange getFcy error")
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
            return math.nan

    def get_b_per_t(self):
        """Get b/t."""
        return self.b_bottom_ / self.thickness_

    def get_x_of_graph(self):
        """X axis of graph."""
        return np.sqrt(self.get_fcy() / self.E_) * self.get_b_per_t()

    def get_fcc(self):
        """7075 graph in page 12."""
        right_axis = self.get_x_of_graph()

        if right_axis < 0.1:
            return math.nan
        elif right_axis < 0.1 * 5**(27 / 33):
            # 直線部分
            # print("フランジ 直線部分")
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

    def get_ms(self, momentum, h_e, web_thickness):
        """MS = FCC/fc -1."""
        ms = self.get_fcc() / self.get_stress_force(momentum, h_e, web_thickness) - 1
        return ms

    def make_row(self, writer, momentum, h_e, web_thickness):
        """
        :param cav_file:csv.writer()で取得されるもの
        :param momentum:前桁分担曲げモーメント
        :param h_e:桁フランジ断面重心距離
        :param web_thickness:ウェブ厚さ
        """
        fcc = self.get_fcc()
        ms = self.get_ms(momentum, h_e, web_thickness)
        value = [web_thickness, momentum, self.thickness_,
                 self.b_bottom_, self.b_height_, fcc, ms]
        writer.writerow(value)

    def make_header(self, writer):
        """
        :param cav_file:csv.writer()で取得されるもの
        """
        header = ["web_thickness[mm]", "momentum",
                  "thickness", "b_bottom_", "b_height", "Fcc", "M.S"]
        writer.writerow(header)


def main():
    """Test fucntion."""
    test = CompressionFrange(6.0, 34.5, 34.5)
    with open('test.csv', 'a') as f:
        writer = csv.writer(f)
        test.make_header(writer)
        test.make_row(writer, 74623, 297, 2.03)


if __name__ == '__main__':
    main()
