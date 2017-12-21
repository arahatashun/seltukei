"""Flange(tension) implementation."""
# coding:utf-8
# Author: Hirotaka Kondo
import math
import csv
from scipy.interpolate import interp1d
from unit_convert import mm2inch, ksi2Mpa, mpa2Ksi, round_sig
from flange import Flange
from web import Web


class TensionFlange(Flange):
    """ Flange(Tension) class."""

    def __init__(self, thickness, b_bottom, b_height, web):
        """Constructor.
        :param thickness:フランジ厚さ[mm]
        :param b_bottom:フランジ底長さ[mm]
        :param b_height:フランジ高さ[mm]
        :param web:このflangeが属するwebのクラス
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

    def make_row(self, momentum, h_e):
        """ Make row of csv.
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
        with open('results/tension_flange.csv', 'a', encoding="utf-8") as f:
            writer = csv.writer(f)
            round_value = map(lambda x: round_sig(x), value)
            writer.writerow(round_value)


def make_tflange_header():
    """
    Make Header of csv.
    """
    header = ["左端STA[mm]", "右端STA[mm]", "web thickness[mm]", "Momentum[N*m]", "$t_{f}$[mm]", "b bottom f1[mm]",
              "b height f2[mm]", "P[N]", "A[${mm}^2$]", "$f_t$[MPa]", "$F_{tu}$[MPa]", "M.S."]
    with open('results/tension_flange.csv', 'a', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)


def read_sn_graph(maximum_stress):
    """s-nカーブ読み取り.応力比R=0,

    :param maximum_stress: 最大応力[MPa]
    :return fatigue_life:繰り返し回数
    """
    maximum_stress_ksi = mpa2Ksi(maximum_stress)
    # print(maximum_stress_ksi)
    y = [8, 7, 6, 5, 4]  # 下面フランジ(edited by knd)
    x = [13, 15, 18, 27, 46]  # 下面フランジ(edited by knd)
    f = interp1d(x, y, kind='linear')
    multiplier = f(maximum_stress_ksi)
    print("multiplier", multiplier)
    fatigue_life = 10 ** multiplier
    return fatigue_life


def make_fatigue_header():
    """
    Make Header of csv.
    """
    header = ["荷重[LMT]", "応力[MPa]", "n[1/khr]", "N[回]", "n/N"]
    with open('results/tension_flange_fatigue.csv', 'a', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)


def write_fatigue_row(maximum_stress):
    """
    write row of csv
    :param maximum_stress:LMT[MPa]
    """
    accumulated_loss = 0  # 累積損失
    with open('results/tension_flange_fatigue.csv', 'a', encoding="utf-8") as f:
        writer = csv.writer(f)
        for (lmt, n) in zip([40, 50, 60, 70, 80, 90, 100], [20000, 6000, 2000, 600, 200, 60, 20]):
            stress = maximum_stress * lmt / 100
            N = read_sn_graph(stress)
            value = [lmt, stress, n, N, n / N]
            round_value = map(lambda x: round_sig(x), value)
            writer.writerow(round_value)
            accumulated_loss = accumulated_loss + n / N

    print("累積損失", accumulated_loss)
    h = 1000 / accumulated_loss
    print("平均寿命", h)
    s_f = 2
    print("安全寿命", h / s_f)


def main():
    """Test Function."""
    """
    web = Web(625, 1000, 3, 2.03)
    test = TensionFlange(6.60, 36, 42.5, web)
    make_tflange_header()
    test.make_row(74623, 297)
    """
    make_fatigue_header()
    write_fatigue_row(260)


if __name__ == '__main__':
    main()
