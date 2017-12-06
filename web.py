"""web implementation."""
# coding:utf-8
# Author: Hirotaka Kondo
from scipy import interpolate
import numpy as np
import math
from unit_convert import ksi2Mpa, mm2inch,get_hf
import csv


class Web(object):
    """
    web class.
    仮定として,Webのせん断座屈を計算するとき,Webは
    いくつかのStiffenerで分割されているが,
    Webの最左端(STA最小)にある分割分に対して強度計算をしている.
    (szmtさんがそうしてるっていう理由だけ)
    またテーパーしてるwebの強度計算については,
    大きい方の寸法を用いて長方形近似して強度計算をしている.
    """

    def __init__(self, y_left, y_right, division, thickness):
        """
        heightとwidthのうち長い方をaとするがアルゴリズム的に問題なし
        :param y_left:webの中でstaが一番小さい側の値 [mm]
        :param y_right:webの中でstaが一番大きい側の値 [mm]
        :param division:分割数
        :param thickness:web厚さ[mm] 7075-T6で厚さが規定されている
        width_bはstiffenerで等分割したあとの
        ウェブの長さ(強度計算上ではstiffenerで分割されているので,
        stiffenerの間隔と同じとする) [mm]
        """
        self.y_left = y_left
        self.y_right = y_right
        self.division = division
        self.thickness = thickness
        self.height_a = get_hf(y_left)  # この高さはwebのSTAが一番小さい側の値
        self.width_b = (y_right - y_left) / division
        self.E = ksi2Mpa(10.3 * 1000)  # 表3-3より読み取る [MPa]

    def get_qmax(self, sf, he):
        """
        ウェブの中における剪断流の最大値を取得.
        ただし,今はSTA最小の場所がせん断流maxと仮定計算する.
        暇があったらここも最大値計算すべき.
        :param sf:前桁の分担荷重 [N]
        :param he:桁フランジ断面重心距離[mm]
        :return: q_max [N/m]
        """
        q_max = sf / he * 1000  # 単位を[N/m]に
        return q_max

    def get_shear_force(self, sf, he):
        """
        ウェブ剪断応力fs.
        :param sf:前桁の分担荷重[N]
        :param he:桁フランジ断面重心距離[mm]
        :return: fs[MPa]
        """
        q_max = self.get_qmax(sf, he)
        return q_max / self.thickness * 1000 / (10 ** 6)  # 単位を[MPa]に

    def get_k(self):
        """ウェブ初期剪断座屈応力fscrを求める."""
        x_axis = self.height_a / self.width_b
        if x_axis < 1:
            x_axis = 1 / x_axis  # 2通りあるa/bのうち大きい方を計算

        if x_axis < 12:
            x = np.array([0.9, 1, 1.2, 1.5, 2, 3, 4, 5, 8, 12])
            y = np.array([11, 8, 7, 6.2, 5.8, 5.3, 5.1, 5, 4.8, 4.8])
            f = interpolate.interp1d(x, y, kind='linear')
            k = f(x_axis)
            return k
        else:
            print("x_axis", x_axis)
            print("x_axis is too large :na in getK in web.py")
            return math.nan

    def get_buckling_shear_force(self):
        """
        剪断座屈応力Fscr.
        :return:Fscr[MPa]
        """
        return self.get_k() * self.E * (self.thickness / self.width_b) ** 2

    def get_fsu(self):
        """
        表3のF_suの値を読み取る.
        :return:F_su[Mpa]
        """
        thickness_in_inch = mm2inch(self.thickness)
        if thickness_in_inch <= 0.011:
            print("too small:nan in getFsu in web.py")
            return math.nan
        elif thickness_in_inch <= 0.039:
            return ksi2Mpa(42)
        elif thickness_in_inch <= 0.062:
            return ksi2Mpa(42)
        elif thickness_in_inch <= 0.187:
            return ksi2Mpa(44)
        elif thickness_in_inch <= 0.249:
            return ksi2Mpa(45)
        else:
            print("too large :nan in getFsu in web.py")
            return math.nan

    def get_ms(self, sf, he):
        """
        安全率を求める.
        :param sf:前桁の分担荷重 [N]
        :param he:桁フランジ断面重心距離[mm]
        :return:M.S. 安全率
        """
        f_scr = self.get_buckling_shear_force()
        f_su = self.get_fsu()
        ms = min(f_su, f_scr) / self.get_shear_force(sf, he) - 1
        return ms

    def get_fsj(self, p, d, sf, he):
        """
        :param p: リベット間隔[mm]
        :param d: リベットの直径[mm]
        :param sf: 前桁の分担荷重[N]
        :param he: 桁フランジ断面重心距離[mm]
        :return: M.S. 安全率
        """
        f_sj = self.get_shear_force(sf, he) * p / (p - d)
        return f_sj

    def get_web_hole_loss_ms(self, p, d, sf, he):
        """
        ウェブホールロスの計算.
        :param p:リベット間隔[mm]
        :param d:リベットの直径[mm]
        :param sf:前桁の分担荷重[N]
        :param he:桁フランジ断面重心距離[mm]
        :return: M.S. 安全率
        """
        f_sj = self.get_fsj(p, d, sf, he)
        ms = self.get_fsu() / f_sj - 1
        return ms

    def make_row(self, writer, sf, he):
        """
        Csv output.
        :param writer:csv.writer()で取得されるもの
        :param sf:前桁の分担荷重[N]
        :param he:桁フランジ断面重心距離[mm]
        """
        fs = self.get_shear_force(sf, he)
        q_max = self.get_qmax(sf, he)
        fscr = self.get_buckling_shear_force()
        fsu = self.get_fsu()
        ms = self.get_ms(sf, he)
        value = [self.y_left, self.y_right, self.division, self.width_b, self.thickness, self.height_a,
                 q_max,
                 fscr, fsu, fs, ms]
        writer.writerow(value)

def make_web_header(writer):
    """
    Csv header.
    :param writer:csv.writer()で取得されるもの
    """
    header = ["左端STA[mm]", "右端STA[mm]", "分割数", "間隔de[mm]", "web厚さ[mm]",
                  "STA最小におけるweb高さ[mm]", "q_max[N/m]", "F_scr[MPa]", "F_su[MPa]", "f_s[MPa]", "M.S."]
    writer.writerow(header)


def main():
    """ Test function."""
    test = Web(625, 1000, 3, 2.03)
    with open('web_test.csv', 'a', encoding="Shift_JIS") as f:
        writer = csv.writer(f)
        make_web_header(writer)
        test.make_row(writer, 38429, 297)


if __name__ == '__main__':
    main()
