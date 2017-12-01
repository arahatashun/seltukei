# coding:utf-8
# Author: Shun Arahata
from scipy import interpolate
import numpy as np
import math
from unit_convert import *
from stiffner import Stiffner
from web import Web
from compression_frange import CompressionFrange
from tension_frange import TensionFrange
from rivet_web_frange import RivetWebFrange
from rivet_web_stiffner import RivetWebStiffner


class Rib(object):
    """Ribのクラス.

    分割数からのスティフナー間隔の計算やheの計算を主に受け持つ
    メンバ関数としては
    Componentオブジェクトの生成と
    csv のwriterオブジェクトを受け取るを追加する
    """

    def __init__(self, y):
        """constructor.

        :param y:staの値を受け取る
        """
        self.y_ = y

    def __get_hf(sta):
        """前桁高さ取得関数.

        :param sta: staの値
        :return hf: 前桁高さ
        """
        x = np.array([625, 5000])
        y = np.array([320, 130])
        f = interpolate.interp1d(x, y, kind='linear')
        hf = f(sta)
        return hf

    def __get_web_iterval(rib_distance, stiffner_counts):
        """ウェブ(スティフナー)間隔取得.

        スティフナーの個数とリブの間隔を受け取りウェブの間隔を返す.
        ウェブの間隔はスティフナーの間隔と同じ.
        スティフナーはリブを等間隔に分割するものとする.
        :param rib_distance:リブの間隙
        :param stiffner_counts:スティフナーの個数
        :return web_interval:ウェブの間隔
        """
        web_interval = rib_distance / stiffner_counts
        return web_interval

    def __get_he(hf: float,
                 compression: CompressionFrange, tension: TensionFrange) ->float:
        """
        桁フランジ断面重心距離heを取得.

        :param hf:前桁高さ[mm]
        :param compression:圧縮側フランジオブジェクト
        :param tension:引張り側フランジオブジェクト
        :return he:桁フランジ断面重心距離[mm]
        """
        he = hf - (tension.getCenterOfGravity() +
                   compression.getCenterOfGravity())
        return he


if __name__ == '__main__':
