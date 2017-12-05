"""Implementation of Rivet between Web and Stiffener."""
# coding:utf-8
# Author: Shun Arahata
from scipy import interpolate
import numpy as np
import math
from unit_convert import ksi2Mpa, mm2inch
from rivet import Rivet
from stiffner import Stiffner
from web import Web
import csv


class RivetWebStiffner(Rivet):
    """ウェブとスティフナーを結合するリベット."""

    def __init__(self, D, stiffner, web):
        """Constructor.

        :param D:リベットの鋲径
        :param stiffener (Stiffener):スティフナーオブジェクト
        :param web (Web):webオブジェクト
        """
        super().__init__(D)
        self.stiffner_ = stiffner
        self.web_ = web
        self.rivet_pitch_ = self.decide_rivet_pitch()
        self.F_su_ = ksi2Mpa(41)  # DD錠を利用する

    def get_steep_of_inter_rivet_buckling(self):
        """鋲間座屈のウェブthicknessによるFirの直線の傾きを求める.

        :return: steep [ksi/(inch/inch)]
        """
        thickness_in_inch = mm2inch(self.web_.thickness_)
        x = [0.125, 0.100, 0.090, 0.080, 0.071, 0.063,
             0.050, 0.040, 0.032, 0.025, 0.020, 0.016]
        y = [(50 - 10) / (20 - 4),  # 0.125
             (60 - 10) / (30 - 20 * 4 / 15),  # 0.1000
             (60 - 10) / (20 + 20 * 11 / 15 - 20 * 5 / 15),  # 0.090
             (60 - 10) / (20 + 20 * 14 / 15 - 20 * 6 / 15),  # 0.080
             (60 - 10) / (40 + 20 * 2 / 15 - 20 * 6 / 15),  # 0.071
             (60 - 10) / (40 + 20 * 6 / 15 - 20 * 6.5 / 15),  # 0.063
             (60 - 10) / (40 + 20 * 14 / 16 - 20 * 8 / 15),  # 0.050
             (60 - 10) / (60 + 20 * 12 / 15 - 20 * 10 / 15),  # 0.040
             (50 - 10) / (60 + 20 * 14 / 15 - 20 * 12 / 15),  # 0.032
             (40 - 10) / (80 - 20),  # 0.025
             (30 - 10) / (60 + 20 * 12 / 15 - (20 + 20 * 4 / 15)),  # 0.020
             (30 - 10) / (80 + 20 * 11 / 15 - (30))]
        f = interpolate.interp1d(x, y)
        steep = f(thickness_in_inch)
        return steep

    def segment_of_inter_rivet_buckling(self):
        """Firの傾きは別の関数で得られるのでp/t=20におけるFirを提供する.

        :return fir_at_20: [ksi]
        """
        skin_thickness = self.web_.thickness_
        x = [0.125, 0.100, 0.090, 0.080, 0.071, 0.063,
             0.050, 0.040, 0.032, 0.025, 0.020, 0.016]
        y = [50, 40, 35, 30, 27.5, 25, 20,
             17, 13, 10, 10 * 10 / 14, 10 * 8 / 14]
        f = interpolate.interp1d(x, y)
        fir_at_20 = f(mm2inch(skin_thickness))
        return fir_at_20

    def get_inter_rivet_buckling(self, rivet_spacing):
        """
        Firを与える
        鋲間座屈の直線の式を作る
        :rivet_spaceing: リベット間隔mm
        :return fir_in_ksi:Fir[MPa]
        """
        steep = self.get_steep_of_inter_rivet_buckling()
        fir_at_20 = self.segment_of_inter_rivet_buckling()
        x_value = rivet_spacing / self.web_.thickness
        fir_in_ksi = fir_at_20 + steep * (x_value - 20)
        fir_in_mpa = ksi2Mpa(fir_in_ksi)
        return fir_in_mpa

    def decide_rivet_pitch(self):
        """"リベットピッチ幅を決める"""
        fcc = self.stiffner_.get_clippling_stress()
        print("fcc", fcc)
        for rivet_spacing in np.linspace(6 * self.D_, 4 * self.D_, 100):
            fir = self.get_inter_rivet_buckling(rivet_spacing)
            print(fir, fcc)
            if fir > fcc:
                return rivet_spacing

        print("web stiffner rivet error")
        return math.nan

    def get_rivet_load(self, stiffner_pitch):
        """ウェブとスティフナーを結合するリベット荷重Pf.

        :param stiffner_pitch:スティフナーピッチ
        """
        area = self.stiffner_.get_area()
        p_2 = self.rivet_pitch_
        d_c = stiffner_pitch
        k = 172  # [MPa]
        p_f = (k * area / d_c) * p_2
        return p_f

    def get_ms(self, stiffner_pitch):
        """
        リベットの安全率
        :param stiffner_pitch:スティフナーピッチ
        """
        ms = self.get_p_allow() / self.get_rivet_load(stiffner_pitch) - 1
        return ms

    def get_web_ms(self, Sf, he):
        """Web_hole_loss_ms."""
        return self.web_.get_web_hole_loss_ms(self.rivet_pitch_, self.D_, Sf, he)

    def make_row(self, writer, Sf, he, stiffener_pitch):
        """
        CSVのrow出力.
        :param writer:csv.writer()で取得されるもの
        :param Sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離
        :param stiffener_pitch: stiffener 間隔
        """
        fir = self.get_inter_rivet_buckling(self.rivet_pitch_)
        fcc = self.stiffner_.get_clippling_stress()
        ms = self.get_ms(stiffener_pitch)
        ms_web_hole = self.get_web_ms(Sf, he)
        pf = self.get_rivet_load(stiffener_pitch)
        value = [Sf / he * 1000, self.D_, self.rivet_pitch_,
                 fir, fcc, pf, ms, ms_web_hole]
        writer.writerow(value)

    def make_header(self, writer):
        """CSV header.

        :param writer:csv.writer()で取得されるもの
        """
        header = ["q_max", "D", "rivet pitch", "Fir",
                  "Fcc", "Pf", "M.S", "M.S.web hole loss"]
        writer.writerow(header)


def main():
    """Test Function."""
    stiffner = Stiffner(2.03, 65, 20)
    web = Web(625, 1000, 1.8, 125)
    test = RivetWebStiffner(6.35, stiffner, web)
    print("MS", test.get_ms(125))
    print("webMS", test.get_web_ms(37429, 297))
    with open('test.csv', 'a') as f:
        writer = csv.writer(f)
        test.make_header(writer)
        test.make_row(writer, 38429, 297, 125)


if __name__ == '__main__':
    main()
