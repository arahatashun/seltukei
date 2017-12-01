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
    """
    Ribのクラス
    分割数からのスティフナー間隔の計算やheの計算を主に受け持つ
    メンバ関数としては
    Componentオブジェクトの生成と
    csv のwriterオブジェクトを受け取るを追加する
    """
    def __init__(y):
        """
        :param y:staの値を受け取る
        """
        self.y_=y



if __name__ == '__main__':
    test()
