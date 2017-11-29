#coding:utf-8
from scipy import interpolate
import numpy as np
import math
from unit_convert import *

class Rivet(object):
    """
    Rivetのsupser class
    AD鋲のみに対応
    """

    def  __init__(self,D):
        """
        :param D:リベットの鋲径
        """
    self.D_=D

    def getAD8(self,thickness):
        """
        :param thickness:板厚[inch]
        """
        x=np.array([])
        y=np.array([])
