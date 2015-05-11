#!/usr/bin/env python

from __future__ import print_function

import xml.etree.ElementTree as ET

class Viper_ETree_Parser(object):
    def __init__(self, filename):
        self.filename = filename
        with open(filename, 'rt') as f:
            self.tree = ET.parse(f)


    def find(self, what):
        # for node in self.tree.findall('.//obj'):
        #     url = node.attrib.get(what)
        #     print(">:", url, node)
        pass


    def show(self):
        root = self.tree.getroot()
        print(root.tag, root.attrib)
        print()
        for c in root:
            print(c.tag, c.attrib)

        # foo = self.tree.find(path=".", namespaces="{http://lamp.cfar.umd.edu/viper#}object")
        # print(type(foo), foo)
        # tag: {http://lamp.cfar.umd.edu/viper#}object attrib: {'framespan': '1:480', 'id': '0', 'name': 'obj'}
        # foo = ET.Element(";laskd")
        # print(foo)
        # print(self.tree.findtext("green_mug"))
        # print(self.tree.findall('object'))
        # print(self.tree.findall("{http://lamp.cfar.umd.edu/viperdata#}bbox"))
        # print(self.tree)
        # for node in self.tree.iter():
        #     print("tag:", node.tag, "attrib:", node.attrib)
        pass


if __name__ == '__main__':
    viper = Viper_ETree_Parser("S1_V3_obj_ann.xgtf")
    # viper.find("green_mug")
    viper.show()

