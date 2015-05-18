# -*- coding: utf-8 -*-
"""
CAD120 data reader that is compatible with QSRlib.

:Author: Yiannis Gatsoulis <y.gatsoulis@leeds.ac.uk>
:Organization: University of Leeds
"""

from __future__ import print_function

import argparse
import os
import csv
import timeit

import qsrlib_io.world_trace

class CSV_to_QSRlib_Data_Reader(object):
    def __init__(self, read_from_files=True,
                 mypath=None, skeleton_filename=None, objects_csv_format="wl",
                 joints_in_file=None, joints=None, skeleton_csv_format="default",
                 data_dict=None):
        """

        :param mypath: directory path where the files are
        :param skeleton_filename: the filename of the skeleton, without the path
        :param objects_csv_format: "corners" | "wl" | "point"
        :return:
        """
        self.world_trace = qsrlib_io.world_trace.World_Trace()
        if read_from_files:
            if not mypath:
                raise ValueError("'mypath' parameter cannot be empty when 'read_from_files=True'")
            self.path = mypath
            self.skeleton_filename, self.objects_filenames = self.get_filenames(mypath, skeleton_filename)
            self.objects_csv_format = objects_csv_format
            self.skeleton_csv_format_offsets = {"default": 0, "skeleton_id": 1, "frame": 1, "frame_skeleton_id": 2}
            try:
                self.skeleton_csv_format_offset = self.skeleton_csv_format_offsets[skeleton_csv_format]
            except:
                raise KeyError("This skeleton_csv_format is not recognized, must be one of %s" %self.skeleton_csv_format_offsets.keys())

            if joints_in_file:
                self.joints_in_file = joints_in_file
            else:
                self.joints_in_file = ("head", "neck", "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
                                       "left_hand", "right_hand", "torso", "left_hip", "right_hip",
                                       "left_knee", "right_knee", "left_foot", "right_foot")
            if joints:
                for k in joints:
                    if k not in self.joints_in_file:
                        raise ValueError("'%s' in joints parameter not found in joints_in_file:\n%s" %(k, self.joints_in_file))
                self.joints = joints
            else:
                self.joints = self.joints_in_file

            self.add_objects_to_world_trace(self.read_objects_tracks())
            if self.skeleton_filename:
                self.add_objects_to_world_trace(self.read_skeleton_track())

        else:  # if not read_from_files
            if not data_dict:
                raise ValueError(("'data_dict' parameter cannot be empty when 'read_from_files=False'"))
            self.add_objects_to_world_trace(data_dict)


    @staticmethod
    def get_filenames(mypath, skeleton_filename=None):
        objects_filenames = []
        for filename in os.listdir(mypath):
            if filename.endswith(".csv"):
                objects_filenames.append(filename)

        if skeleton_filename:
            try:
                objects_filenames.remove(skeleton_filename)
            except:
                raise ValueError("mistyped skeleton filename or it does not exists in %s" %mypath)
        return skeleton_filename, objects_filenames


    def read_objects_tracks(self):
        tracks = {}
        for filename in self.objects_filenames:
            o_name = os.path.splitext(filename)[0]
            filename = os.path.join(self.path, filename)
            tracks[o_name] = self.read_object_track(filename)
        return tracks


    def read_object_track(self, filename):
        track = []
        with open(filename, "r") as f:
            csvr = csv.reader(f)
            if self.objects_csv_format == "wl":
                for line in csvr:
                    track.append((line[0], line[1], line[2], line[3]))
        return track


    def add_objects_to_world_trace(self, tracks):
        for name, track in tracks.items():
            self.world_trace.add_object_track_from_list(name, track)


    def read_skeleton_track(self):
        offset = self.skeleton_csv_format_offset
        joints_d = {}
        c = 0 #dbg
        for j in self.joints:
            joints_d[j] = []
        with open(os.path.join(self.path, self.skeleton_filename)) as f:
            csvr = csv.reader(f)
            for line in csvr:
                # joints_poses = self.__process_skeleton_line(line)
                for i, j in zip(range(len(self.joints)), self.joints):
                    j_data = tuple(int(round(float(i))) for i in line[i*3+offset:i*3+offset+2])
                    joints_d[j].append(j_data)
                #dbg start
                print(joints_d)
                c += 1
                if c ==2: return
                #dbg stop



if __name__ == '__main__':
    argp = argparse.ArgumentParser(description="csv to QSRlib world trace format")
    argp.add_argument("-p", "--path", required=True, help="directory path where the files are")
    argp.add_argument("--skeleton", help="skeleton filename")
    argp.add_argument("-l", "--load", help="pickle filename to load")
    argp.add_argument("-s", "--save")
    args = argp.parse_args()

    foo = CSV_to_QSRlib_Data_Reader(mypath=args.path, skeleton_filename="skeleton.csv",
                                    skeleton_csv_format="frame_skeleton_id", joints=["head"])

    # print(foo.skeleton_filename, foo.objects_filenames)
    # for t in foo.world_trace.get_sorted_timestamps():
    #     print("-----\nt:", t)
    #     for o_name, o_pos in foo.world_trace.trace[t].objects.items():
    #         print(o_name, o_pos.x, o_pos.y, o_pos.width, o_pos.length)

