#!/usr/bin/env python

from __future__ import print_function

import xml.etree.ElementTree as ET
import os
import csv
import argparse

class Viper_XML_Parser(object):
    def __init__(self, filename, prefix="{http://lamp.cfar.umd.edu/viper#}"):
        self.prefix = prefix
        self.filename = filename
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()


    def find_etree_bbox(self, which):
        foo = self.prefix+"data"+"/"+self.prefix+"sourcefile"+"/"+self.prefix+"object"
        objs = self.root.findall(foo)
        bbox = None
        for o in objs:
            found = False
            bbox_temp = None
            for a in o:
                if a.attrib["name"] == "bbox":
                    bbox_temp = a
                elif a.attrib["name"] == "name":
                    for v in a:
                        if v.attrib["value"] == which:
                            found = True
            if found:
                bbox = bbox_temp
                break

        return bbox


    def bbox_etree_to_list_expanded(self, bbox_etree):
        bbox_list = []
        for b in bbox_etree:
            # print(b.tag, b.attrib)
            x = int(b.attrib["x"])
            y = int(b.attrib["y"])
            width = int(b.attrib["width"])
            height = int(b.attrib["height"])
            framespan = [int(foo) for foo in b.attrib["framespan"].split(":")]
            duration = 1 + framespan[1] - framespan[0]
            bbox_list += [(x, y, width, height)]*duration
        return bbox_list


    def save_object_bbox_list_as_csv(self, bbox, filename):
        if os.path.exists(filename):
            print("Warning: file already exists")
        with open(filename, "wt") as f:
            w = csv.writer(f)
            w.writerows(bbox)



if __name__ == '__main__':
    argp = argparse.ArgumentParser(description="From viper xml to csv values")
    argp.add_argument("-i", "--input", help="input xml .xgtf file", required=True)
    argp.add_argument("-w", "--which", help="which object", required=True)
    argp.add_argument("-s", "--save", help="save to file")
    args = argp.parse_args()

    xmlp = Viper_XML_Parser(args.input)
    bbox_etree = xmlp.find_etree_bbox(args.which)
    bbox_list = xmlp.bbox_etree_to_list_expanded(bbox_etree=bbox_etree)
    if args.save:
        xmlp.save_object_bbox_list_as_csv(bbox_list, args.save)


