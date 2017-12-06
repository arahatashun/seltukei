"""Flange Base Class."""


# coding:utf-8
# Author: Hirotaka Kondo


class Flange:
    """Flange Base Class."""

    def __init__(self, thickness, b_bottom, b_height):
        """Constructor.

        :param thickness:フランジ厚さ[mm]
        :param b_bottom:フランジ底長さ(bf1)[mm]
        :param b_height:フランジ高さ(bf2)[mm]
        """
        self.thickness = thickness
        self.b_bottom = b_bottom
        self.b_height = b_height

    def get_area(self, web_thickness):
        """
        Get Area of Flange.
        :param web_thickness:web厚さ
        :return:面積[mm^2]
        """
        return (self.b_bottom + self.b_height) * self.thickness + web_thickness ** 2 * 30

    def get_center_of_gravity(self):
        """heを求めるために,フランジの図心の値を求める
        フランジの角部分.この関数の返り値を
        前桁高さから引いてheを得る.(ただし上下フランジ2つ分)
        :return [mm]
        """
        area1 = (self.b_height - self.thickness) * self.thickness
        area2 = (self.b_bottom + self.thickness / 2) * self.thickness
        y = (area1 * (self.thickness / 2) + area2 / 2 * (self.b_bottom + self.thickness / 2)) / (area1 + area2)
        print(y)
        return y

    def get_axial_force(self, momentum, h_e):
        """
        フランジの軸力を求める.
        :param momentum:前桁負担分モーメント
        :param h_e:桁フランジ断面重心距離[mm]
        :return axial_force: [N]
        """
        axial_force = momentum / h_e * 1000  # 単位を[N]に
        return axial_force

    def get_stress_force(self, momentum, h_e, web_thickness):
        """Get f_c or f_t.
        :param momentum:前桁分担曲げモーメント[N*m]
        :param h_e:桁フランジ断面重心距離[mm]
        :param web_thickness:ウェブ厚さ[mm]
        :return: 応力[MPa]
        """
        return self.get_axial_force(momentum, h_e) / self.get_area(web_thickness)


def main():
    """Test Function."""
    test = Flange(6, 30, 30)
    print("A[mm^2]", test.get_area(1.6))
    print("C.G.[mm]", test.get_center_of_gravity())
    ax = test.get_axial_force(74623, 297)
    print("P[N]", ax)
    f = test.get_stress_force(74623, 297, 2.03)
    print("fc[MPa]", f)


if __name__ == '__main__':
    main()
