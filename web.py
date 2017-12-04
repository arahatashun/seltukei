"""web implementation."""
# coding:utf-8
# Author: Shun Arahata
from scipy import interpolate
import numpy as np
import math
from unit_convert import ksi2Mpa, mm2inch, get_hf
import csv


class Web(object):
    """ web class."""

    def __init__(self, y, thickness, width_b):
        """ constructor.

        :param y:staでの左端座標
        :param thickness:web厚さ[mm] 7075-T6で厚さが規定されている
        :param width_b:ウェブの長さ(stiffnerで殺されるのでstiffnerの間隔と同じ)
        height width長い方をaとするがアルゴリズム的に問題なし
        """
        self.y_ = y
        self.thickness_ = thickness
        self.height_a_ = get_hf(y)
        self.width_b_ = width_b
        self.E_ = ksi2Mpa(10.3 * 1000)

    def __get_qmax(self, Sf, he):
        """ 剪断流を取得.

        :param Sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離[mm]
        """
        q_max = Sf / he
        return q_max

    def __get_shear_force(self, Sf, he):
        """ウェブ剪断応力fs.

        :param Sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離
        """
        q_max = self.__get_qmax(Sf, he)
        return q_max / self.thickness_

    def __get_k(self):
        """ ウェブ初期剪断座屈応力fscrを求める."""
        x_axis = self.height_a_ / self.width_b_
        if x_axis < 1:
            x_axis = 1 / x_axis
        if x_axis < 12:
            x = np.array([0.9, 1.5, 2,   3, 4,  5,  8, 12])
            y = np.array([11, 6.2, 5.8, 5.3, 5.1, 5, 4.8, 4.8])
            f = interpolate.interp1d(x, y, kind='linear')
            k = f(x_axis)
            # print("k", k)
            return k
        else:
            print("x_axis", x_axis)
            print("x_axis is too large :in getK in web.py")
            return math.nan

    def __get_buckling_shear_force(self):
        """剪断座屈応力Fscr."""
        return self.__get_k() * self.E_ * (self.thickness_ / self.width_b_)**2

    def __get_fsu(self):
        """表3のF_su."""
        thickness_in_inch = mm2inch(self.thickness_)
        if thickness_in_inch < 0.011:
            print("too small:nan in getFsu in web.py")
            return math.nan
        elif thickness_in_inch < 0.039:
            return ksi2Mpa(42)
        elif thickness_in_inch < 0.062:
            return ksi2Mpa(42)
        elif thickness_in_inch < 0.187:
            return ksi2Mpa(44)
        elif thickness_in_inch < 0.000249:
            return ksi2Mpa(45)
        else:
            print("too large :nan in getFsu in web.py")
            return math.nan

    def __get_ms(self, Sf, he):
        """安全率を求める.

        :param Sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離
        """
        f_scr = self.__get_buckling_shear_force()
        f_su = self.__get_fsu()
        ms = min(f_su, f_scr) / self.__get_shear_force(Sf, he) - 1
        # print(ms)
        return ms

    def get_web_hole_loss_ms(self, p, d, Sf, he):
        """ウェブホールロスの計算.

        :param p:リベット間隔
        :param d:リベットの直径[mm]
        :param Sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離
        """

        f_sj = self.__get_shear_force(Sf, he) * p / (p - d)
        # print(f_sj)
        ms = self.__get_fsu() / f_sj - 1
        print("ms", ms)
        return ms

    def make_row(self, writer, Sf, he):
        """Csv output.

        :param y: webの左端の座標(mm)
        :param cav_file:csv.writer()で取得されるもの
        :param Sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離
        """
        fs = self.__get_shear_force(Sf, he)
        Fscr = self.__get_buckling_shear_force()
        ms = self.__get_ms(Sf, he)
        value = [self.y_, self.thickness_, self.height_a_,
                 self.width_b_, fs, Fscr, ms]
        writer.writerow(value)

    def make_header(self, writer):
        """ Csv header.

        :param cav_file:csv.writer()で取得されるもの
        """
        header = ["y[mm]", "web_thickness[mm]",
                  "前桁高さ", "間隔de", "fs", "Fscr", "M.S"]
        writer.writerow(header)


def main():
    """ Test fuction."""
    unti = Web(650, 2.03, 125)
    with open('test.csv', 'a') as f:
        writer = csv.writer(f)
        unti.make_header(writer)
        unti.make_row(writer, 38429, 297)


if __name__ == '__main__':
    main()
