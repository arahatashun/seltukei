"""implementation of rib"""
# coding:utf-8
# Author: Shun Arahata
from stiffener import Stiffener
from web import Web, make_web_header
from compression_flange import CompressionFlange, make_cflange_header
from tension_flange import TensionFlange, make_tflange_header
from rivet_web_flange import RivetWebFlange
from rivet_web_stiffener import RivetWebStiffener
from unit_convert import get_hf
from sandm.py import get_sf, get_mf
import csv

# リブ左端の座標
LEFT_ARRAY = [625, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500]
# リブの間隔
RIB_WIDTH = [375, 500, 500, 500, 500, 500, 500, 500, 500]

"""
THICKNESS_7075 = [0.41, 0.51, 0.64, 0.81, 1.02,
                  1.27, 1.60, 1.80, 2.03, 2.29, 2.54, 3.18]
"""


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
        self.sf = get_sf(self.y_left)
        self.mf = get_mf(self.y_left)

    def add_web(self, thickness, division_count):
        """ Add web to rib.

        :param division: number of stiffeners + 1
        :param thickness_index:thickness of web
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
        self.set_he()

    def add_rivet_stiffener(self, D,):
        self.rivet_stiffener = RivetWebStiffener(D, self.stiffener, self.web)

    def add_rivet_flange(self, D, pd_ratio, N):
        """
        :param D:リベットの鋲径
        :param pd_ratio:リベットピッチ/リベットの鋲半径,一般に4D~6Dとすることが多い
        :param N:リベット列数
        """
        self.ribet_flange = RivetWebFlange(D, pd_ratio, N, self.web)

    def set_he(self):
        """rivet重心位置計算によりheを計算.
        :param hf:前桁高さ[mm]
        :return he:桁フランジ断面重心距離
        """
        self.he = self.hf - \
            (self.tflange.get_center_of_gravity() +
             self.cflange.get_center_of_gravity())
        return self.he

    def web_csv(self, writer):
        """
        Csv output.
        :param writer:csv.writer()で取得されるもの
        """
        self.web.make_row(writer, self.sf, self.he)

    def stiffener_csv(self, writer):
        """
        :param writer:csv.writer()で取得されるもの
        :param he:桁フランジ断面重心距離
        """
        self.stiffener.make_row(writer, self.he)

    def cflange_csv(self, writer):
        """
        :param writer:csv.writer()で取得されるもの
        :param momentum:前桁分担曲げモーメント[N*m]
        :param h_e:桁フランジ断面重心距離[mm]
        """
        self.cflange.make_row(writer, self.mf, self.he)

    def tflange_csv(self, writer):
        self.tflange.make_row(writer, self.mf, self.he)


def main():
    """
    web_thickness = 1.80
    web_distance = 80  # stiffener 間隔でもある
    hf = getHf(sta + web_distance)
    tension_frange_thickness = 6.0
    tension_frange_bottom = 50
    tension_frange_height = 40
    compression_frange_thickness = 6.0
    compression_frange_bottom = 45
    compression_frange_height = 40
    rivet_web_stiffner_diameter = 6.35  # DD8
    rivet_web_frange_N = 2
    rivet_web_frange_D = 6.35
    rivet_web_pdratio = 6
    """
    sta625 = Rib(0)
    sta625.add_web(1.60, 5)
    sta625.add_stiffener(1.27, 40, 30)
    sta625.add_compression_flange(5.0, 45, 40)
    sta625.add_tension_flange(5.0, 45, 40)
    with open('sta625.csv', 'w', encoding='Shift_JIS') as f:
        writer = csv.writer(f)
        make_web_header(writer)
        he = sta625.get_he()
        print("he", he)
        sta625.web.make_row(writer, 32116 * 1.2, he)
        make_tflange_header(writer)
        sta625.tflange.make_row(writer, 61676 * 1.2, he)
        make_cflange_header(writer)
        sta625.cflange.make_row(writer, 61676 * 1.2, he)
    """
    stiffner_thickness = 0.81  # mm
    stiffner_bs1 = 20
    stiffner_bs2 = 15
    web_thickness = 1.02
    web_distance = 70  # stiffener 間隔でもある
    hf = getHf(sta + web_distance)
    tension_frange_thickness = 3.0
    tension_frange_bottom = 25
    tension_frange_height = 20
    compression_frange_thickness = 3.0
    compression_frange_bottom = 30
    compression_frange_height = 20
    rivet_web_stiffner_diameter = 6.35  # DD8
    rivet_web_frange_N = 2
    rivet_web_frange_D = 6.35
    rivet_web_pdratio = 6
    """
    sta3000 = Rib(5)
    sta3000.add_web(1.02, 7)
    sta3000.add_stiffener(0.81, 20, 15)
    sta3000.add_compression_flange(3.0, 30, 20)
    sta3000.add_tension_flange(3.0, 30, 20)
    with open('sta3000.csv', 'w', encoding='Shift_JIS') as f:
        writer = csv.writer(f)
        make_web_header(writer)
        he = sta3000.get_he()
        print("he", he)
        sta3000.web.make_row(writer, 11463 * 1.2, he)
        make_tflange_header(writer)
        sta3000.tflange.make_row(writer, 9585 * 1.2, he)
        make_cflange_header(writer)
        sta3000.cflange.make_row(writer, 9585 * 1.2, he)


if __name__ == '__main__':
    main()
