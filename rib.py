"""implementation of rib"""
# coding:utf-8
# Author: Shun Arahata
from stiffener import Stiffener
from web import Web
from compression_flange import CompressionFlange
from tension_flange import TensionFlange
from rivet_web_flange import RivetWebFlange
from rivet_web_stiffener import RivetWebStiffener


# リブ左端の座標
LEFT_ARRAY = [625, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500]
# リブの間隔
RIB_WIDTH = [375, 500, 500, 500, 500, 500, 500, 500, 500]

THICKNESS_7075 = [0.41, 0.51, 0.64, 0.81, 1.02,
                  1.27, 1.60, 1.80, 2.03, 2.29, 2.54, 3.18]


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

    def add_stiffener(self, thickness, bs1_bottom, bs2_height):
        """ Add Stiffener.

        :param thickness: stiffener厚さ
        :param bs1_bottom:stiffener bottom長さ
        :param bs2_height:stiffener 高さ
        """
        self.stiffener = Stiffener(thickness, bs1_bottom, bs2_height)

    def add_web(self, division, thickness_index):
        """ Add web to rib.

        :param division: number of stiffners+1
        :param thickness_index:thickness of web
        """
        thickness = THICKNESS_7075[thickness_index]
        self.web = Web(self.y_left, self.y_right, division, thickness)

    def add_compression_frange(self, thickness, b_bottom, b_height):
        """ Add flange(compression).

        :param thickness:フランジ厚さ
        :param b_bottom:フランジ底長さ
        :param b_height:フランジ高さ
        """
        self.cfrange = CompressionFlange(thickness, b_bottom, b_height)

    def add_tension_frange(self, thickness, b_bottom, b_height):
        self.tfrange = TensionFlange(thickness, b_bottom, b_height)

    def add_rivet_stiffener(self, D, stiffener, web):
        self.rivet_stffener = RivetWebStiffener(D, self.stiffener, self.web)

    def add_rivet_flange(self, D, pd_ratio, N):
        """
        :param D:リベットの鋲径
        :param pd_ratio:リベットピッチ/リベットの鋲半径,一般に4D~6Dとすることが多い
        :param N:リベット列数
        """
        self.ribet_flange = RivetWebFlange(D, pd_ratio, N, self.web)
