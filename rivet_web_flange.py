"""Implementation of class between web and flange."""
# coding:utf-8
# Author: Shun Arahata,Hirotaka Kondo

import csv
from unit_convert import ksi2Mpa, round_sig
from rivet import Rivet
from web import Web


class RivetWebFlange(Rivet):
    """ウェブフランジ結合のリベット."""

    def __init__(self, D, pd_ratio, N, web):
        """Constructor.

        :param D:リベットの鋲径
        :param pd_ratio:リベットピッチ/リベットの鋲半径,一般に4D~6Dとすることが多い
        :param N:リベット列数
        :param web:リベットによってフランジと結合されるwebのクラス
        """
        super().__init__(D)
        self.F_su = ksi2Mpa(30)  # AD
        self.pd_ratio = pd_ratio
        self.rivet_pitch = D * pd_ratio
        self.N = N
        self.web = web

    def get_shear_force(self, sf, he):
        """Ps=q_max*p/Nを返す.

        :param sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離
        """
        q_max = sf / he
        ps = q_max * self.rivet_pitch / self.N
        return ps

    def get_ms(self, sf, he):
        """M.S.=P_allow/Ps-1.

        :param sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離
        """
        p_allow = self.get_p_allow()
        ps = self.get_shear_force(sf, he)
        ms = p_allow / ps - 1
        return ms

    def get_web_ms(self, sf, he):
        """ウェブホールロスの計算.

        :param sf:前桁の分担荷重
        :param he:桁フランジ断面重心距離
        """
        return self.web.get_web_hole_loss_ms(self.rivet_pitch, self.D, sf, he)

    def get_web_hole_loss(self, sf, he):
        """
        :param sf: f:前桁荷重負担分[N]
        :param he: he:フランジ間断面重心距離[mm]
        :return: ウェブホールロスのM.S.
        """
        ms = self.web.get_web_hole_loss_ms(self.rivet_pitch, self.D, sf, he)
        return ms

    def make_row_shear(self, writer, sf, he):
        """
        Make CSV Row for shear.
        :param writer:csv.writer()で取得されるもの
        :param sf:前桁の分担荷重[N]
        :param he:桁フランジ断面重心距離[mm]
        """
        p_allow = self.get_p_allow()
        ps = self.get_shear_force(sf, he)
        ms = self.get_ms(sf, he)
        value = [self.web.y_left, self.web.y_right, int(sf / he * 1000), self.N, self.D,
                 round_sig(self.rivet_pitch, sig = 4), int(ps), int(p_allow), round_sig(ms)]
        writer.writerow(value)

    def make_row_web_hole(self, writer, sf, he):
        """
        Make CSV Row for web hole loss.
        :param writer:
        :param sf: 前桁の分担荷重[N]
        :param he: 桁フランジ断面重心距離[mm]
        :return:
        """
        fs = self.web.get_shear_force(sf, he)
        fsj = self.web.get_fsj(self.rivet_pitch, self.D, sf, he)
        fsu = self.web.get_fsu()
        ms = self.web.get_web_hole_loss_ms(self.rivet_pitch, self.D, sf, he)
        f_scr = self.web.get_buckling_shear_force()
        value = [self.web.y_left, self.web.y_right, self.D,
                 round_sig(self.rivet_pitch), round_sig(fs), round_sig(fsj), round_sig(fsu), round_sig(f_scr),
                 round_sig(ms)]
        writer.writerow(value)

    def write_all_row(self, sf, he):
        """
        :param sf: 前桁の分担荷重[N]
        :param he: 桁フランジ断面重心距離[mm]
        :return:
        """
        with open('results/rivet_web_flange_shear.csv', 'a', encoding="utf-8") as f:
            writer = csv.writer(f)
            self.make_row_shear(writer, sf, he)
        with open('results/rivet_web_flange_web_hole.csv', 'a', encoding="utf-8") as f:
            writer = csv.writer(f)
            self.make_row_web_hole(writer, sf, he)


def _make_header_shear(writer):
    """Make Header of CSV shear M.S.
    :param writer:csv.writer()で取得されるもの
    """
    header = ["左端STA[mm]", "右端STA[mm]", "$q_{max}$[N/m]", "N", "D[mm]", "p[mm]", "Ps[N]", "$P_{allow}$[N]", "M.S."]
    writer.writerow(header)


def _make_header_web_hole(writer):
    """Make Header of CSV web hole loss.
    :param writer:csv.writer()で取得されるもの
    """
    header = ["左端STA[mm]", "右端STA[mm]", "D[mm]", "p[mm]", "$f_s$[MPa]", "$f_{sj}$[MPa]", "$F_{su}$[MPa]",
              "$f_{scr}$[MPa]", "M.S."]
    writer.writerow(header)


def rivet_wf_make_all_header():
    with open('results/rivet_web_flange_shear.csv', 'a', encoding="utf-8") as f:
        writer = csv.writer(f)
        _make_header_shear(writer)
    with open('results/rivet_web_flange_web_hole.csv', 'a', encoding="utf-8") as f:
        writer = csv.writer(f)
        _make_header_web_hole(writer)


def main():
    """Test Function."""
    web = Web(625, 1000, 3, 2.03)
    test = RivetWebFlange(3.175, 6, 2, web)
    rivet_wf_make_all_header()
    test.write_all_row(32117, 297)


if __name__ == '__main__':
    main()
