#coding:utf-8
from scipy import interpolate
import numpy as np
import math
from unit_convert import *
from rivet import Rivet

class RivetWebStiffner(Rivet):
    """
    ウェブとスティフナーを結合するリベット荷重
    """
    def  __init__(self,D):
        """
        :param D:リベットの鋲径
        """
        super(RivetWebFrange, self).__init__(D)

    def get(self):
