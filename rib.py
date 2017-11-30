#coding:utf-8
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

    @type_definition(int,Stiffner,Web,CompressionFrange,TensionFrange,RivetWebFrange,RivetWebStiffner)
    def __init__(self,y_index,web,compression_frange,tension_frange,rivet_web_frange,rivet_web_stiffner):
        """
        :param y_index:sta array の index
        """
        self.y_index_=y_index
        self.web_=web
        self.compression_frange_=compression_frange
        self.tension_frange=tension_frange_
        self.rivet_web_frange_=rivet_web_frange
        self.rivet_web_stiffner_=rivet_web_stiffner

        STA_ARRAY=[625,1000,1500,2000,2500,3000,3500,4000,4500]
        RIB_DISTANCE_ARRAY=[375,500,500,500,500,500,500]
        self.num_of_stiffners_=num_of_stiffners
        assert sta_index<=len(STA_ARRAY)-1,"sta_indexの値が大きすぎます"
        self.left_=STA_ARRAY[sta_index]
        #:STAでの左端の座標を保持する
        self.front_spar_height_=getHf(y)
        #:左端における前桁高さ
        self.he_=self.front_spar_height_-(self.compression_frange_.getCenterOfGravity()
                                            +self.tension_frange_.getCenterOfGravity())





def make_compression frange_index():
    frange_compression=CompressionFrange(7.0, 3.5,3.5)



if __name__ == '__main__':
    test()
