"""implementation of rib"""
# coding:utf-8
# Author: Shun Arahata
from stiffener import Stiffener
from web import Web
from compression_flange import CompressionFlange
from tension_flange import TensionFlange
from rivet_web_flange import RivetWebFlange
from rivet_web_stiffener import RivetWebStiffener
from unit_convert import get_hf, round_sig
import csv
import math

# from sandm import get_sf, get_mf

# リブ左端の座標
LEFT_ARRAY = [625, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500]
# リブの間隔
RIB_WIDTH = [375, 500, 500, 500, 500, 500, 500, 500, 500]
SF_LIST = [38540, 35357, 29988, 24251, 18745, 13756, 9233, 5262, 1952]  # だれか全部追加して
MF_LIST = [74012, 60233, 44117, 30306, 19505, 11503, 5757, 2151, 389]  # だれか全部追加して


class Rib(object):
    """Ribのクラス.

    分割数からのスティフナー間隔の計算やheの計算を主に受け持つ
    キーワード変数によるコンストラクタ
    csv のwriterオブジェクトを受け取るものを追加する

    Attributes:
        y_left:リブ左端座標
        y_right:リブ右端座標
        width:リブの大きさ
        web:ウェブ

    """

    def __init__(self, y_index):
        """Constructor.

        :param y_index:リブ左端位置のindex
        """
        self.y_left = LEFT_ARRAY[y_index]
        self.width = RIB_WIDTH[y_index]
        self.y_right = self.y_left + self.width
        self.hf = get_hf(self.y_left)
        self.sf = SF_LIST[y_index]
        self.mf = MF_LIST[y_index]
        # self.sf = get_sf(self.y_left) 計算速度のボトルネック
        # self.mf = get_mf(self.y_left) 計算速度のボトルネック

    def add_web(self, thickness, division_count):
        """ Add web to rib.
        :param division_count: number of stiffeners + 1
        :param thickness:thickness of web
        """
        self.web = Web(self.y_left, self.y_right, division_count, thickness)

    def add_stiffener(self, thickness, bs1_bottom, bs2_height):
        """ Add Stiffener.
        :param thickness: stiffener厚さ
        :param bs1_bottom:stiffener bottom長さ
        :param bs2_height:stiffener 高さ
        """
        self.stiffener = Stiffener(thickness, bs1_bottom, bs2_height, self.web)

    def add_compression_flange(self, thickness, b_bottom, b_height):
        """ Add flange(compression).

        :param thickness:フランジ厚さ
        :param b_bottom:フランジ底長さ
        :param b_height:フランジ高さ
        """
        self.cflange = CompressionFlange(
            thickness, b_bottom, b_height, self.web)

    def add_tension_flange(self, thickness, b_bottom, b_height):
        self.tflange = TensionFlange(thickness, b_bottom, b_height, self.web)

    def add_rivet_stiffener(self, D):
        self.rivet_stiffener = RivetWebStiffener(D, self.stiffener, self.web)

    def add_rivet_flange(self, D, pd_ratio, N):
        """
        :param D:リベットの鋲径
        :param pd_ratio:リベットピッチ/リベットの鋲半径,一般に4D~6Dとすることが多い
        :param N:リベット列数
        """
        self.rivet_flange = RivetWebFlange(D, pd_ratio, N, self.web)

    def set_he(self):
        """rivet重心位置計算によりheを計算.
        :return he:桁フランジ断面重心距離
        """
        self.he = self.hf - (self.tflange.get_center_of_gravity() + self.cflange.get_center_of_gravity())
        return self.he

    def could_be_hit(self):
        """リベットを打てるかどうか.printによる警告"""
        if self.stiffener.bs1_bottom < 4 * self.rivet_stiffener.D:
            print("ERROR Rivet: stiffener bs1 too small")

        if self.cflange.b_height < 4 * self.rivet_stiffener.D:
            print("WARING Rivet: cflange height bf2 may be too small")

        if self.tflange.b_height < 4 * self.rivet_stiffener.D:
            print("WARING Rivet: tflange height bf2 may be too small")

        if self.rivet_flange.N == 2:
            ratio = 2+3+2 # 縁距離+千鳥間隔
        elif self.rivet_flange.N == 1:
            ratio = 2+2

        if self.tflange.b_bottom < ratio * self.rivet_flange.D + self.tflange.thickness/2:
            print("WARING Rivet: tflange bottom bf1 may be too small")

        if self.cflange.b_bottom < ratio * self.rivet_flange.D + self.cflange.thickness/2:
            print("WARING Rivet: cflange bottom bf1 may be too small")

    def get_total_mass(self):
        """
        この区間に於けるウェブ,２つのフランジ,スティフナーの総重量を計算する
        :return: total_mass[kg]
        """
        length_rib2rib = self.web.y_right - self.web.y_left
        v1 = self.web.get_volume()
        v2 = self.stiffener.get_volume()
        v3 = self.cflange.get_volume(length_rib2rib)
        v4 = self.tflange.get_volume(length_rib2rib)
        # print(v1, v2, v3, v4)
        return (v1 + v2 + v3 + v4) * 3.0 / 1000  # {kg]

    def decide_ms(self):
        """
        全てのM.S.を計算して,それが全て正ならTrueを返す
        :return:
        """
        ms1 = self.web.get_ms(self.sf, self.he)
        if ms1 < 0:
            print("Error :web ms")
        ms2 = self.stiffener.get_ms(self.he)
        if ms2 < 0:
            print("Error :stiffener ms")
        ms3 = self.cflange.get_ms(self.mf, self.he)
        if ms3 < 0:
            print("Error :cflange ms")
        ms4 = self.tflange.get_ms(self.mf, self.he)
        if ms4 < 0:
            print("Error :tflange ms")
        ms5 = self.rivet_stiffener.get_ms()
        if ms5 < 0:
            print("Error :rivet stiffener ms")
        ms6 = self.rivet_stiffener.get_web_hole_loss(self.sf, self.he)
        if ms6 < 0:
            print("Error :rivet stiffener web hole loss ms")
        ms7 = self.rivet_flange.get_ms(self.sf, self.he)
        if ms7 < 0:
            print("Error :rivet flange ms")
        ms8 = self.rivet_flange.get_web_hole_loss(self.sf, self.he)
        if ms8 < 0:
            print("Error :rivet flange web hole loss ms")
        # print(ms1, ms2, ms3, ms4, ms5, ms6, ms7, ms8)
        if (math.isnan(ms2)):  # ms2==nanは,stiffenerがそもそもないときに起こる場合がほとんどなので...
            if ms1 >= 0 and ms3 >= 0 and ms4 >= 0 and ms5 >= 0 and ms6 >= 0 and ms7 >= 0 and ms8 >= 0:
                return True
        elif ms1 >= 0 and ms2 >= 0 and ms3 >= 0 and ms4 >= 0 and ms5 >= 0 and ms6 >= 0 and ms7 >= 0 and ms8 >= 0:
            return True
        else:
            print("WARNING: MS<0")
            return False


    def web_csv(self):
        """
        Csv output.
        """
        self.could_be_hit()
        self.set_he()
        self.web.make_row(self.sf, self.he)

    def stiffener_csv(self):
        self.stiffener.make_row(self.he)

    def cflange_csv(self):
        self.cflange.make_row(self.mf, self.he)

    def tflange_csv(self):
        self.tflange.make_row(self.mf, self.he)

    def rivet_stiffener_csv(self):
        self.rivet_stiffener.write_all_row(self.sf, self.he)

    def rivet_flange_csv(self):
        self.rivet_flange.write_all_row(self.sf, self.he)

    def write_rib_row(self):
        """表の中身."""
        value = [self.y_left, self.y_right, self.web.thickness, self.web.division,
                 self.stiffener.thickness, self.stiffener.bs1_bottom, self.stiffener.bs2_height,
                 self.cflange.thickness, self.cflange.b_bottom, self.cflange.b_height,
                 self.tflange.thickness, self.tflange.b_bottom, self.tflange.b_height,
                 self.rivet_stiffener.D, self.rivet_flange.D, self.rivet_flange.pd_ratio,
                 self.rivet_flange.N, round_sig(self.get_total_mass())]
        with open('results/rib.csv', 'a', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(value)


def make_rib_header():
    """リブに囲まれたSTA区間の諸元についての表のheaderを作成する."""
    header = ["左端STA[mm]", "右端STA[mm]", "ウェブ厚さ", "分割数", "stiffener厚さts", "同bs1", "同bs2",
              "上(圧縮側)フランジ$t_f$", "bf1", "bf2", "下(引張側)フランジ$t_f$", "bf1", "bf2",
              "Rivet(stiffener) D", "Rivet(flange) D",
              "同P/D", "同列数", "質量"]
    with open('results/rib.csv', 'a', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)


def main():
    """
    web_thickness = 1.80
    web_distance = 80  # stiffener間隔でもある
    hf = getHf(sta + web_distance)
    tension_flange_thickness = 6.0
    tension_flange_bottom = 50
    tension_flange_height = 40
    compression_flange_thickness = 6.0
    compression_flange_bottom = 45
    compression_flange_height = 40
    rivet_web_stiffener_diameter = 6.35  # DD8
    rivet_web_flange_N = 2
    rivet_web_flange_D = 6.35
    rivet_web_pd_ratio = 6
    """
    sta625 = Rib(0)
    sta625.add_web(1.60, 5)
    sta625.add_stiffener(1.27, 40, 30)
    sta625.add_compression_flange(5.0, 45, 40)
    sta625.add_tension_flange(5.0, 45, 40)
    sta625.add_rivet_stiffener(6.35)
    sta625.add_rivet_flange(6.35, 4, 2)
    sta625.add_rivet_stiffener(6.35)
    sta625.set_he()
    sta625.web_csv()
    sta625.tflange_csv()
    sta625.cflange_csv()
    sta625.rivet_stiffener_csv()
    sta625.rivet_flange_csv()
    make_rib_header()
    sta625.write_rib_row()


if __name__ == '__main__':
    main()
