"""Flange(compression) implementation."""
# coding:utf-8
# Author: Hirotaka Kondo
import numpy as np
import math
from scipy.interpolate import interp1d
from unit_convert import ksi2Mpa, mm2inch, mpa2Ksi, round_sig
from flange import Flange
import csv


class CompressionFlange(Flange):
    """Flange (Compression) Class."""

    def __init__(self, thickness, b_bottom, b_height, web):
        """ Constructor.

        :param thickness:フランジ厚さ[mm]
        :param b_bottom:フランジ底長さ[mm]
        :param b_height:フランジ高さ[mm]
        :param web:このflangeが属するwebのクラス
        """
        super().__init__(thickness, b_bottom, b_height)
        self.E = ksi2Mpa(10.3 * 10 ** 3)
        self.web = web

    def get_fcy(self):
        """
        Get fcy of 7075.
        p.25の表参照
        :return:[MPa]
        """
        thickness_in_inch = mm2inch(self.thickness)

        if thickness_in_inch < 0.499:
            return ksi2Mpa(68)
        elif thickness_in_inch < 5.000:
            return ksi2Mpa(69)
        else:
            return math.nan

    def get_b_per_t(self):
        """Get b/t."""
        return self.b_bottom / self.thickness

    def get_x_of_graph(self):
        """X axis of graph."""
        return np.sqrt(self.get_fcy() / self.E) * self.get_b_per_t()

    def get_fcc(self):
        """
        7075 graph in page 12.
        :return:[MPa]
        """
        right_axis = self.get_x_of_graph()

        if right_axis < 0.1:
            return math.nan
        elif right_axis < 0.1 * 5 ** (27 / 33):
            # 一定部分
            # print("フランジ 直線部分")
            left_axis = 0.5 * 2 ** (2.2 / 1.5)
        elif right_axis < 10:
            left_axis = 10 ** (-0.20761) * right_axis ** (-0.78427)
        else:
            return math.nan
        lower = mpa2Ksi(self.get_fcy())  # 分母
        upper = left_axis * lower  # 分子
        fcc = ksi2Mpa(upper)

        return fcc

    def get_ms(self, momentum, h_e):
        """M.S. = Fcc/fc -1."""
        ms = self.get_fcc() / self.get_stress_force(momentum, h_e, self.web.thickness) - 1
        return ms

    def make_row(self, momentum, h_e):
        """
        :param momentum:前桁分担曲げモーメント[N*m]
        :param h_e:桁フランジ断面重心距離[mm]
        """
        fcc = self.get_fcc()
        ms = self.get_ms(momentum, h_e)
        p = self.get_axial_force(momentum, h_e)
        a = self.get_area(self.web.thickness)
        fc = self.get_stress_force(momentum, h_e, self.web.thickness)
        sqrt = self.get_x_of_graph()  # p12グラフのx軸の値
        value = [self.web.y_left, self.web.y_right, self.web.thickness, momentum, self.thickness,
                 self.b_bottom, self.b_height, int(p), round_sig(a), round_sig(fc), round_sig(sqrt), round_sig(fcc),
                 round_sig(ms)]
        with open('results/compression_flange.csv', 'a', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(value)


def read_sn_graph(maximum_stress):
    """s-nカーブ読み取り.応力比R=0,

    :param maximum_stress: 最大応力[MPa]
    :return fatigue_life:繰り返し回数
    """
    maximum_stress_ksi = mpa2Ksi(maximum_stress)
    # print(maximum_stress_ksi)
    y = [7, 6, 5, 4, 3.3]  # 上面フランジ(edited by knd)
    x = [6, 11, 18.5, 32, 40]  # 上面フランジ(edited by knd)
    f = interp1d(x, y, kind='linear')
    multiplier = f(maximum_stress_ksi)
    print("multiplier", multiplier)
    fatigue_life = 10 ** multiplier
    return fatigue_life


def make_cflange_header():
    header = ["左端STA[mm]", "右端STA[mm]", "web thickness[mm]", "Momentum[N*m]",
              "$t_f$[mm]", "b bottom f1[mm]", "b height f2[mm]", "P[N]", "A[${mm}^2$]", "fc[MPa]", "√(Fcy/E)(b/t)",
              "$F_{cc}$[MPa]", "M.S."]
    with open('results/compression_flange.csv', 'a', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)


def make_fatigue_header():
    """
    Make Header of csv.
    """
    header = ["荷重[LMT]", "応力[MPa]", "n[1/khr]", "N[回]", "n/N"]
    with open('results/compression_flange_fatigue.csv', 'a', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)


def write_fatigue_row(maximum_stress):
    """
    write row of csv
    :param maximum_stress:LMT[MPa]
    """
    accumulated_loss = 0  # 累積損失
    with open('results/compression_flange_fatigue.csv', 'a', encoding="utf-8") as f:
        writer = csv.writer(f)
        for (lmt, n) in zip([40, 50, 60, 70, 80, 90, 100], [20000, 6000, 2000, 600, 200, 60, 20]):
            stress = maximum_stress * lmt / 100
            N = read_sn_graph(stress)
            value = [lmt, stress, n, N, n / N]
            writer.writerow(value)
            accumulated_loss = accumulated_loss + n / N

    print("累積損失", accumulated_loss)
    h = 1000 / accumulated_loss
    print("平均寿命", h)
    s_f = 2
    print("安全寿命", h / s_f)


def main():
    """Test function."""
    """
    web = Web(625, 1000, 3, 2.03)
    test = CompressionFlange(6.0, 34.5, 34.5, web)
    make_cflange_header()
    test.make_row(74623, 297)
    """
    make_fatigue_header()
    write_fatigue_row(268.6)


if __name__ == '__main__':
    main()
