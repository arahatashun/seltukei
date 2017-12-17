"""Implementation of Rivet between Web and Stiffener."""
# coding:utf-8
# Author:Shun Arahata,Hirotaka Kondo
from scipy import interpolate
import numpy as np
import math
from unit_convert import ksi2Mpa
from rivet import Rivet
from stiffener import Stiffener
from web import Web
import csv


class RivetWebStiffener(Rivet):
    """ウェブとスティフナーを結合するリベット."""

    def __init__(self, D, stiffener, web):
        """Constructor.

        :param D:リベットの鋲径[mm]
        :param stiffener (Stiffener):スティフナーオブジェクト
        :param web (Web):webオブジェクト
        """
        super().__init__(D)
        self.stiffener = stiffener
        self.web = web
        self.rivet_pitch = self.decide_rivet_pitch()
        self.F_su = ksi2Mpa(41)  # DD鋲を利用する(originalはAD鋲)

    """
    def get_steep_of_inter_rivet_buckling(self):

        鋲間座屈のウェブthicknessによるFirの直線の傾きを求める.
        講義ノートp.3
        :return: steep [ksi/(inch/inch)]

        thickness_in_inch = mm2inch(self.web.thickness)
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
             (30 - 10) / (80 + 20 * 11 / 15 - 30)]
        f = interpolate.interp1d(x, y)
        steep = f(thickness_in_inch)
        return steep
    """

    """
    直線が原点からのびてるっぽいので傾きだけ使えば良く,この関数いらないかも
    def segment_of_inter_rivet_buckling(self):
        Firの傾きは別の関数で得られるのでp/t=20におけるFirを提供する.
        :return fir_at_20: [ksi]

        skin_thickness = self.web.thickness
        x = [0.125, 0.100, 0.090, 0.080, 0.071, 0.063,
             0.050, 0.040, 0.032, 0.025, 0.020, 0.016]
        y = [50, 40, 35, 30, 27.5, 25, 20,
             17, 13, 10, 10 * 10 / 14, 10 * 8 / 14]
        f = interpolate.interp1d(x, y)
        fir_at_20 = f(mm2inch(skin_thickness))
        return fir_at_20
    """
    """
    def get_inter_rivet_buckling(self):

        Firを与える
        鋲間座屈の直線の式を作る
        :return fir_in_ksi:Fir[MPa]

        steep = self.get_steep_of_inter_rivet_buckling()
        x = self.rivet_pitch / self.web.thickness  # p3のx軸のp/t
        fir_in_ksi = steep * x
        fir_in_mpa = ksi2Mpa(fir_in_ksi)
        return fir_in_mpa
    """

    def get_inter_rivet_buckling(self):
        """
        講義ノート2p.3のグラフを線形補間して作成
        :return: Fir
        """
        x = [9, 12, 16, 20, 23, 28, 30, 33, 35, 40, 48, 60, 80]
        y = [68, 64, 60, 56, 50, 45, 40, 32, 30, 23, 16, 10, 6]
        f = interpolate.interp1d(x, y)
        fir_in_ksi = f(self.rivet_pitch / self.web.thickness)
        fir_in_mpa = ksi2Mpa(fir_in_ksi)
        return fir_in_mpa

    def decide_rivet_pitch(self):
        """"リベットピッチ幅を決める"""
        fcc = self.stiffener.get_clippling_stress()
        # print("fcc", fcc)
        for rivet_spacing in np.linspace(6 * self.D, 4 * self.D, 100):
            self.rivet_pitch = rivet_spacing
            fir = self.get_inter_rivet_buckling()
            # print(fir, fcc)
            if fir > fcc:
                return rivet_spacing

        print("web stiffener rivet error")
        return math.nan

    def get_rivet_load(self):
        """
        ウェブとスティフナーを結合するリベット荷重Pf.
        """
        area = self.stiffener.get_area()
        p_2 = self.rivet_pitch
        d_c = self.web.width_b  # スティフナーピッチ
        k = 172  # [MPa](p.13経験式)
        p_f = (k * area / d_c) * p_2
        return p_f

    def get_ms(self):
        """
        リベットの安全率
        """
        ms = self.get_p_allow() / self.get_rivet_load() - 1
        return ms

    def make_row_shear(self, writer):
        """
        CSVのrow出力.
        :param writer:csv.writer()で取得されるもの
        """
        k = 172  # [MPa](p.13経験式)
        area = self.stiffener.get_area()
        ms = self.get_ms()
        pf = self.get_rivet_load()
        p_allow = self.get_p_allow()
        value = [self.web.y_left, self.web.y_right, k, area, self.web.width_b, self.D, self.rivet_pitch,
                 pf, p_allow, ms]
        writer.writerow(value)

    def make_row_buckling(self, writer):
        """
        :param writer: csv.writer()で取得されるもの
        :return:
        """
        fir = self.get_inter_rivet_buckling()
        fcc = self.stiffener.get_clippling_stress()
        value = [self.web.y_left, self.web.y_right, self.stiffener.bs1_bottom, self.stiffener.thickness, fcc, fir,
                 self.rivet_pitch]
        writer.writerow(value)

    def get_web_hole_loss(self, sf, he):
        """
        :param sf: f:前桁荷重負担分[N]
        :param he: he:フランジ間断面重心距離[mm]
        :return: ウェブホールロスのM.S.
        """
        ms = self.web.get_web_hole_loss_ms(self.rivet_pitch, self.D, sf, he)
        return ms

    def make_row_web_hole(self, writer, sf, he):
        """
        :param writer: csv.writer()で取得されるもの
        :param sf:前桁荷重負担分[N]
        :param he:フランジ間断面重心距離[mm]
        :return:
        """
        fs = self.web.get_shear_force(sf, he)
        fsu = self.web.get_fsu()
        fsj = self.web.get_fsj(self.rivet_pitch, self.D, sf, he)
        ms = self.web.get_web_hole_loss_ms(self.rivet_pitch, self.D, sf, he)
        f_scr = self.web.get_buckling_shear_force()
        value = [self.web.y_left, self.web.y_right, self.rivet_pitch, self.D, fs, fsj, fsu, f_scr, ms]
        writer.writerow(value)

    def write_all_row(self, sf, he):
        """
        :param sf:前桁荷重負担分[N]
        :param he:フランジ間断面重心距離[mm]
        :return:
        """
        with open('results/rivet_web_stiffener_shear.csv', 'a', encoding="utf-8") as shear:
            shear_writer = csv.writer(shear)
            self.make_row_shear(shear_writer)
        with open('results/rivet_web_stiffener_buckling.csv', 'a', encoding="utf-8") as buckling:
            buckling_writer = csv.writer(buckling)
            self.make_row_buckling(buckling_writer)
        with open('results/rivet_web_stiffener_web_hole.csv', 'a', encoding="utf-8") as holeloss:
            holeloss_writer = csv.writer(holeloss)
            self.make_row_web_hole(holeloss_writer, sf, he)


def _make_header_shear(writer):
    """
    CSV header shear.
    :param writer:csv.writer()で取得されるもの
    """
    header = ["左端STA[mm]", "右端STA[mm]", "K[MPa]", "As[${mm}^2$]", "dc[mm]", "D[mm]", "p[mm]",
              "$P_f$[N]", "$P_{allow}$[N]", "M.S."]
    writer.writerow(header)


def _make_header_buckling(writer):
    """
    CSV header shear.
    :param writer:csv.writer()で取得されるもの
    """
    header = ["左端STA[mm]", "右端STA[mm]", "b bottom s1[mm]", "ts[mm]", "$F_{cc}$[MPa]", "$F_{ir}$[MPa]",
              "p[mm]"]
    writer.writerow(header)


def _make_header_web_hole(writer):
    """
    CSV header web hole.
    :param writer:csv.writer()で取得されるもの
    """
    header = ["左端STA[mm]", "右端STA[mm]", "p[mm]", "D[mm]", "$f_s$[MPa]", "$f_{sj}$[MPa]", "$F_{su}$[MPa]",
              "$f_{scr}$[MPa]", "M.S."]
    writer.writerow(header)


def rivet_ws_make_all_header():
    with open('results/rivet_web_stiffener_shear.csv', 'a', encoding="utf-8") as shear:
        shear_writer = csv.writer(shear)
        _make_header_shear(shear_writer)
    with open('results/rivet_web_stiffener_buckling.csv', 'a', encoding="utf-8") as buckling:
        buckling_writer = csv.writer(buckling)
        _make_header_buckling(buckling_writer)
    with open('results/rivet_web_stiffener_web_hole.csv', 'a', encoding="utf-8") as holeloss:
        holeloss_writer = csv.writer(holeloss)
        _make_header_web_hole(holeloss_writer)


def main():
    """Test Function."""
    web = Web(625, 1000, 3, 2.03)
    stiffener = Stiffener(2.03, 20, 20, web)
    test = RivetWebStiffener(3.175, stiffener, web)
    rivet_ws_make_all_header()
    test.write_all_row(32119, 297)


if __name__ == '__main__':
    main()
