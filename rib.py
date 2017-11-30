#coding:utf-8
from scipy import interpolate
import numpy as np
import math
from unit_convert import *
from stiffner import Stiffner
from web import Web
from compression_frange import CompressionFrange
from tesnsion_frange import TensionFrange
from rivet_web_frange import RivetWebFrange
from rivet_web_stiffner import RivetWebStiffner

def getHf(self,y=0):
    """
    yにおける前桁高さHfを返す
    """
    x=np.array([625,5000])
    y=np.array([320,130])
    f = interpolate.interp1d(x, y,kind='linear')
    return f(y)


class Rib(object):

    def __init__(self,sta_index,num_of_stiffners,stiffner_thickness,
                stiffner_bottom,web_thickness,compression_frange_thickness,
                compression_frange_bottom,compression_frange_height,
                tension_frange_thicknes,tension_frange_bottom,tension_frange_height
                rivet_frange_D,rivet_frange_pdratio,rivet_frange_N,rivet_stiffner_D):

        """
        :param sta_index:STA での位置625~5000で625がindex 0に対応する
        :param num_of_stiffners:スティフナーの枚数
        :param stiffner_thickness: スティフナーの厚さts
        :param stiffner_bottom:スティフナーの底の長さbs1
        :param stiffner_height:スティフナーの高さbs2
        :param web_thickness:ウェブの厚さ
        :param compression_frange_thicknes:圧縮側(上側)フランジの厚さ
        :param compression_frange_bottom:圧縮側(上側)フランジの底の長さb1
        :param compression_frange_height:圧縮側(上側)フランジの高さb2
        :param tension_frange_thicknes:引張側(下側)フランジの厚さ
        :param tension_frange_bottom:引張側(下側)フランジの底の長さb1
        :param tension_frange_height:引張側(下側)フランジの高さb2
        :param rivet_frange_D:フランジとウェブをつなぐリベットの鋲径
        :param rivet_frange_pdratio:リベットピッチ/リベットの鋲半径,一般に4D~6Dとすることが多い
        :param rivet_frange_N:リベットフランジの列数
        :param rivet_stiffner_D:ウェブとスティフナーつなぐリベットの直径
        """
        STA_ARRAY=[625,1000,1500,2000,2500,3000,3500,4000,4500]
        RIB_DISTANCE_ARRAY=[375,500,500,500,500,500,500]
        self.num_of_stiffners_=num_of_stiffners
        assert sta_index<=len(STA_ARRAY)-1,"sta_indexの値が大きすぎます"
        self.left_=STA_ARRAY[sta_index]
        #:STAでの左端の座標を保持する
        self.front_spar_height_=self.getHf()
        #:左端における前桁高さ
        self.rib_distance_ =RIB_DISTANCE_ARRAY[sta_index]
        #:リブ間隔
        self.stiffner_distance_=self.rib_distance_/(self.num_of_stiffners_+1)
        #:スティフナー間隔
        self.stiffner_ = Stiffner(stiffner_thickness,stiffner_bottom,stiffner_height)
        #:リブのsta最小でのスティフナーの作成
        self.web_=Web(web_thickness,self.front_spar_height_,self.stiffner_distance_)
        #:ウェブの作成
        self.compression_frange_=CompressionFrange(compression_frange_thickness,
                                    compression_frange_bottom,
                                    compression_frange_height)
        #:フランジ圧縮側
        self.tension_frange_=TensionFrange(tension_frange_thicknes,
                                tension_frange_bottom,tension_frange_height)
        #:フランジ引張側
        self.he_=self.front_spar_height_-(self.compression_frange_.getCenterOfGravity()
        +self.tension_frange_.getCenterOfGravity())
        #:前桁高さからFrangeの分引いたものheとなる
        self.rivet_web_frange_=RivetWebFrange(rivet_frange_D,rivet_frange_pdratio,rivet_frange_N,self.web_)
        #:webとリベットを接合するフランジ
        self.rivet_web_stiffner_=RivetWebStiffner(rivet_stiffner_D,self.stiffner_,self.web_)
        #:webとstiffnerを接合するフランジ



def test():
    frange_compression



if __name__ == '__main__':
    test()
