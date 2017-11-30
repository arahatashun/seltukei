#coding:utf-8
from scipy import interpolate
import numpy as np
import math
from unit_convert import *
from rivet import Rivet
from stiffner import Stiffner
from web import Web

class RivetWebStiffner(Rivet):
    """
    ウェブとスティフナーを結合するリベット
    """
    def  __init__(self,D,stiffner,web):
        """
        :param D:リベットの鋲径
        :param stiffner (Stiffner):スティフナーオブジェクト
        :param web (Web):webオブジェクト
        """
        super(RivetWebStiffner, self).__init__(D)
        self.stiffner_=stiffner
        self.web_=web
        self.rivet_pitch_=self.decideRivetPitch()


    def getSteepofInterRivetBuckling(self):
        """
        鋲間座屈のウェブthicknessによる
        Firの直線の傾きを求める
        :return: steep [ksi/(inch/inch)]
        """
        thickness_in_inch=mm2inch(self.web_.thickness_)
        x=[0.125,0.100,0.090,0.080,0.071,0.063,0.050,0.040,0.032,0.025,0.020,0.016]
        y=[(50-10)/(20-4),#0.125
            (60-10)/(30-20*4/15),#0.1000
            (60-10)/(20+20*11/15-20*5/15),#0.090
            (60-10)/(20+20*14/15-20*6/15),#0.080
            (60-10)/(40+20*2/15-20*6/15),#0.071
            (60-10)/(40+20*6/15-20*6.5/15),#0.063
            (60-10)/(40+20*14/16-20*8/15),#0.050
            (60-10)/(60+20*12/15-20*10/15),#0.040
            (50-10)/(60+20*14/15-20*12/15),#0.032
            (40-10)/(80-20),#0.025
            (30-10)/(60+20*12/15-(20+20*4/15)),#0.020
            (30-10)/(80+20*11/15-(30))]
        f=interpolate.interp1d(x, y)
        steep=f(thickness_in_inch)
        return steep

    def segmentOfInterRivetBuckling(self):
        """
        Firの傾きは別の関数で得られるのでp/t=20
        におけるFirを提供する
        :return fir_at_20: [ksi]
        """
        skin_thickness=self.web_.thickness_
        x=[0.125,0.100,0.090,0.080,0.071,0.063,0.050,0.040,0.032,0.025,0.020,0.016]
        y=[  50,    40,   35,    30,27.5,    25,  20,   17,   13,   10 ,10*10/14, 10*8/14]
        f=interpolate.interp1d(x, y)
        fir_at_20=f(mm2inch(skin_thickness))
        return fir_at_20

    def getInterRivetBuckling(self,rivet_spaceing):
        """
        鋲間座屈の直線の式を作る
        :rivet_spaceing: リベット間隔mm
        :return fir_in_ksi:Fir[MPa]
        """
        steep=self.getSteepofInterRivetBuckling()
        fir_at_20=self.segmentOfInterRivetBuckling()
        x_value =rivet_spaceing/self.web_.thickness_
        fir_in_ksi=fir_at_20+steep*(x_value-20)
        fir_in_mpa=ksi2Mpa(fir_in_ksi)
        return fir_in_mpa

    def decideRivetPitch(self):
        fcc=self.stiffner_.getClipplingStress()
        print("fcc",fcc)
        for rivet_spaceing in np.linspace(4*self.D_,6*self.D_,100):
            fir=self.getInterRivetBuckling(rivet_spaceing)
            print(fir,fcc)
            if abs(fir-fcc)<5:
                return rivet_spaceing

        print("web stiffner rivet error")
        return math.nan

    def getRivetload(self,stiffner_pitch):
        """
        ウェブとスティフナーを結合するリベット荷重
        :param stiffner_pitch:スティフナーピッチ
        """
        area=self.stiffner_.getArea()
        p_2=self.rivet_pitch_
        d_c=stiffner_pitch
        K=172#MPa
        p_f=(K*area/d_c)*p_2
        return p_f

    def getMS(self,stiffner_pitch):
        """
        リベットの安全率
        :param stiffner_pitch:スティフナーピッチ
        """
        ms=self.getPallow()/self.getRivetload(stiffner_pitch)-1
        return ms


def test():
    stiffner=Stiffner(2.03,50,20)
    web=Web(1.8,317.2,60)
    rivet=RivetWebStiffner(6.35,stiffner,web)
    print("MS",rivet.getMS(125))

if __name__ == '__main__':
    test()
