"""Implementation of class between web and frange."""
# coding:utf-8
# Author: Shun Arahata

import csv
from unit_convert import ksi2Mpa
from rivet import Rivet
from web import Web


class RivetWebFrange(Rivet):
    """ウェブフランジ結合のリベット."""

    def __init__(self, D, pd_ratio, N, web):
        """Constructor.

        :param D:リベットの鋲径
        :param pd_ration:リベットピッチ/リベットの鋲半径,一般に4D~6Dとすることが多い
        :param N:リベット列数
        :param web:結合されるweb
        """
        super().__init__(D)
        self.F_su_ = ksi2Mpa(30)  # AD
        self.p1_ = D * pd_ratio
        self.N_ = N
        self.web_ = web

    def get_shear_force(self, Sf, he):
        """Ps=qmax*p/Nを返す.

        :param Sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離
        """
        qmax = Sf / he
        Ps = qmax * self.p1_ / self.N_
        return Ps

    def get_ms(self, Sf, he):
        """M.S.=Pallow/Ps-1.

        :param Sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離
        """
        Pallow = self.get_p_allow()
        Ps = self.get_shear_force(Sf, he)
        ms = Pallow / Ps
        return ms

    def get_web_ms(self, Sf, he):
        """ウェブホールロスの計算.

        :param Sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離
        """
        return self.web_.get_web_hole_loss_ms(self.p1_, self.D_, Sf, he)

    def make_row(self, writer, Sf, he):
        """Make CSV ROW.

        :param cav_file:csv.writer()で取得されるもの
        :param Sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離
        """
        Ps = self.get_shear_force(Sf, he)
        ms = self.get_ms(Sf, he)
        ms_web_hole = self.get_web_ms(Sf, he)
        value = [Sf / he * 1000, self.N_, self.D_,
                 self.p1_, Ps, ms, ms_web_hole]
        writer.writerow(value)

    def make_header(self, writer):
        """Make Header of CSV.

        :param cav_file:csv.writer()で取得されるもの
        """
        header = ["qmax", "N", "D", "pitch", "Ps", "M.S", "M.S.web hole loss"]
        writer.writerow(header)


def main():
    """Test Function."""
    unti = Web(650, 2.03, 125)
    test = RivetWebFrange(3.175, 19.05, 2, unti)
    with open('test.csv', 'a') as f:
        writer = csv.writer(f)
        test.make_header(writer)
        test.make_row(writer, 38429, 297)


if __name__ == '__main__':
    main()
