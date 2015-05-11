#!/usr/bin/env python

from __future__ import print_function

import xml.etree.ElementTree as ET

class XML_Parser(object):
    def __init__(self, filename, prefix="{http://lamp.cfar.umd.edu/viper#}"):
        self.prefix = prefix
        self.filename = filename
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()
        self.data = self.root.find(prefix+'data')

    def foo(self):
        # print(self.root.tag, self.root.attrib)
        # for child in self.root:
        #     print(child.tag, child.attrib)
        # print(self.root.findall('{http://lamp.cfar.umd.edu/viper#}country'))
        # for country in self.root.findall('{http://lamp.cfar.umd.edu/viper#}country'):
        #     rank = country.find('{http://lamp.cfar.umd.edu/viper#}rank').text
        #     name = country.get('name')
        #     print(name, rank)
            # print(country.tag, country.attrib)
        # print(self.root.iter('neighbor'))
        # for neighbor in self.root.iter('neighbor'):
        #     print(">", neighbor.attrib)

        # for d in self.root.findall('{http://lamp.cfar.umd.edu/viper#}data'):
        #     print(d.tag, d.attrib)

        print(type(self.root), self.root)
        print(type(self.data), self.data)
        for o in self.data.findall(self.prefix+"object"):
            # o_name = o.find(self.prefix+"attribute/)
            o_name = o.findtext("name")
            print(o_name)
            # o_attribs = list(o.iter(self.prefix+"attribute"))
            # print(o_attribs.tag)
            # for a in o.findall(self.prefix+"attribute"):
            #     print(a.tag, a.attrib)
        pass

if __name__ == '__main__':
    p = XML_Parser("country_data.xml")
    p.foo()
