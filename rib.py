"""implementation of rib"""
# coding:utf-8
# Author: Shun Arahata
from scipy import interpolate
import numpy as np
import math
from unit_convert import get_hf
from stiffner import Stiffner
from web import Web
from compression_frange import CompressionFrange
from tension_frange import TensionFrange
from rivet_web_frange import RivetWebFrange
from rivet_web_stiffner import RivetWebStiffner


# リブ左端の座標
LEFT_ARRAY = [625, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500]
# リブの間隔
RIB_WIDTH = [375, 500, 500, 500, 500, 500, 500, 500, 500]

class Rib(object):
    """Ribのクラス.

    分割数からのスティフナー間隔の計算やheの計算を主に受け持つ
    キーワード変数によるコンストラクタ
    csv のwriterオブジェクトを受け取るものを追加する
    """

    def __init__(self, **kwargs):
        """constructor.

        :param **kwargs:ウェブ諸元のdictionary
        {
            "y_index",Rib 左端の座標のindex
            "web_thickness",ウェブの厚さ
            "stiffner counts",stiffnerの枚数
            "stiffner thickness",stiffner厚さ
            "stiffner bottom",stiffner 底の長さ
            "stiffner height",stiffner 高さ
            "compression frange thickness",フランジ圧縮側厚さ
            "comprssion frange height",フランジ圧縮側高さ
            "compression frange width"フランジ圧縮側幅
            "tension frange height",フランジ引張側高さ
            "tension frange width",フランジ引張側幅
            "tension frange thickenss",フランジ引張側厚さ
            "rivet stifner D",スティフナーリベットの直径
            "rivet frange D",フランジのリベット直径
            "rivet frange pd ration",フランジのリベットピッチ/リベットの鋲半径
            "rivet frange N",フランジのリベット列数
        }
        """
        assert kwargs["y_index"] < len(LEFT_ARRAY), "rib index too large"

    def get_web_iterval(rib_distance, stiffner_counts):
        """ウェブ(スティフナー)間隔取得.

        スティフナーの個数とリブの間隔を受け取りウェブの間隔を返す.
        ウェブの間隔はスティフナーの間隔と同じ.
        スティフナーはリブを等間隔に分割するものとする.
        :param rib_distance:リブの間隙
        :param stiffner_counts:スティフナーの個数
        :return web_interval:ウェブの間隔
        """
        web_interval = rib_distance / (stiffner_counts+1)
        return web_interval
