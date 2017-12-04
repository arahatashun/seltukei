"""Frange Base Class."""
# coding:utf-8
# Author: Shun Arahata
from unit_convert import inch2mm


class Frange:
    """Frange Base Class."""

    def __init__(self, thickness, b_bottome, b_height):
        """Constructor.

        :param thickness:フランジ厚さ
        :param b_bottom:フランジ底長さ
        :param b_height:フランジ高さ
        """
        self.thickness_ = thickness
        self.b_bottom_ = b_bottome
        self.b_height_ = b_height

    def get_area(self, web_thickness):
        """Get Area of Frange.

        :@param web_thickness:web厚さ
        """
        return (self.b_bottom_ + self.b_height_) * self.thickness_ + web_thickness**2 * 30


    def get_center_of_gravity(self):
        """フランジの底から重心高さを求める.heを求める."""
        area = (self.b_bottom_ + self.b_height_) * self.thickness_
        bottom_area = (self.b_bottom_ + self.thickness_ / 2) * self.thickness_
        residure = area / 2 - bottom_area

        if(residure < 0):
            # print("residure<0")
            return area / 2 / (self.b_bottom_ + self.thickness_ / 2)
        else:
            return self.thickness_ + residure / self.thickness_

    def get_axial_force(self, momentum, h_e):
        """ フランジの軸力を求める.

        :param momentum:前桁負担分モーメント
        :param h_e:桁フランジ断面重心距離
        :return axialforce: [N]
        """
        axialforce = momentum / h_e * 1000
        return axialforce

    def get_stress_force(self, momentum, h_e, web_thickness):
        """Get f_c or f_t.

        :param momentum:前桁分担曲げモーメント
        :param h_e:桁フランジ断面重心距離
        :param web_thickness:ウェブ厚さ
        """
        #  [MPa]
        return self.get_axial_force(momentum, h_e) / self.get_area(web_thickness)


def main():
    """Test Function."""
    test = Frange(6.0, 34.5, 34.5)
    A = test.get_area(2.03)
    print("A", A)
    cofg = test.get_center_of_gravity()
    print("cofg", cofg)
    ax = test.get_axial_force(74623, 297)
    print("P[N]", ax)
    f = test.get_stress_force(74623, 297, 2.03)
    print("fc[MPa]", f)


if __name__ == '__main__':
    main()
