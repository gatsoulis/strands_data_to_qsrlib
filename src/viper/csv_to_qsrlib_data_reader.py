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

import qsrlib_io.world_trace



class CSV_to_QSRlib_Data_Reader(object):
    def __init__(self, read_from_files=True,
                 mypath=None, skeleton_filename=None, objects_csv_format="wl",
                 joints_in_file=None, joints=None, skeleton_csv_format="default",
                 data_dict=None):
        """Class to read objects tracks and optionally skeleton tracks and convert them in QSRlib `World_Trace` format.
        The tracks can be read from csv files when `read_from_files=True`, in which case `mypath` is required,
        or by passing a dictionary of {object_name: [positions]} when `read_from_files=False`, in which case `mypath`
        is required.

        The positions can be points as (x, y) or bounding boxes (x, y, width, length), where x, y are the coordinates of
        the center of the bounding box, width is the total x size and length the total y size.


        :param read_from_files: boolean specifying whether to read from files or load from data_dict
        :param joints_in_file: which joints are in the file
        :param joints: which joints are requested
        :param skeleton_csv_format: deal with cases there are other prefix data in the skeleton file and sets offset
                                    default: 0, no prefix data
                                    skeleton_id: 1, first value is the skeleton id
                                    frame: 1, first value is the frame number
                                    frame_skeleton_id: 2, first two values are the frame and the skeleton id
        :param data_dict: the data as a dictionary of {object_name: [(x, y, width, length), ...]}, width and length are optional
                            required when read_from_files=False
        :param mypath: directory path where the files are, required when read_from_files=True
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
        """

        :param mypath: the directory where the csv files are
        :param skeleton_filename: optional skeleton filename (no path needed, but should be in `mypath`)
        :return: the skeleton filename, a list with the objects filenames
        """
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
        """Reads from csv files and returns the objects' tracks as a dictionary


        :return: a dictionary of the object name as key and the tracks as a list of tuples
        """
        tracks = {}
        for filename in self.objects_filenames:
            o_name = os.path.splitext(filename)[0]
            tracks[o_name] = self.read_object_track(filename)
        return tracks


    def read_object_track(self, filename):
        """Reads an object's track from a csv file

        :param filename: the filename of an object's track
        :return: the requested object's track as a list of tuples with contain the position (or bounding box)
        """
        filename = os.path.join(self.path, filename)
        track = []
        with open(filename, "r") as f:
            csvr = csv.reader(f)
            if self.objects_csv_format == "wl":
                for line in csvr:
                    track.append((line[0], line[1], line[2], line[3]))
        return track


    def add_objects_to_world_trace(self, tracks):
        """Adds the object tracks to the `self.world_trace`

        :param tracks: a dictionary of tracks for each object, {object_name: track, ...}
        """
        for name, track in tracks.items():
            self.world_trace.add_object_track_from_list(name, track)


    def read_skeleton_track(self):
        """Reads the skeleton tracks from a csv file, taking into account `self.joints`,
        `self.skeleton_csv_format_offset`


        :return: a dictionary of the tracks for each joint requested in `self.joints`
        """
        offset = self.skeleton_csv_format_offset
        joints_d = {}
        for j in self.joints:
            joints_d[j] = []
        with open(os.path.join(self.path, self.skeleton_filename)) as f:
            csvr = csv.reader(f)
            for line in csvr:
                # for i, j in zip(range(len(self.joints)), self.joints):
                for j in self.joints:
                    i = self.joints_in_file.index(j)
                    j_data = tuple(int(round(float(i))) for i in line[i*3+offset:i*3+offset+2])
                    joints_d[j].append(j_data)
        return joints_d



if __name__ == '__main__':
    argp = argparse.ArgumentParser(description="csv to QSRlib world trace format")
    argp.add_argument("-p", "--path", required=True, help="directory path where the files are")
    argp.add_argument("--skeleton", help="skeleton filename")
    argp.add_argument("-l", "--load", help="pickle filename to load")
    argp.add_argument("-s", "--save")
    args = argp.parse_args()

    foo = CSV_to_QSRlib_Data_Reader(mypath=args.path, skeleton_filename="skeleton.csv",
                                    skeleton_csv_format="frame_skeleton_id", joints=["head", "left_hand", "right_hand"])

    # print(foo.skeleton_filename, foo.objects_filenames)
    # for t in foo.world_trace.get_sorted_timestamps():
    # for t in [foo.world_trace.get_sorted_timestamps()[0]]:
    #     print("-----\nt:", t)
    #     for o_name, o_pos in foo.world_trace.trace[t].objects.items():
    #         print(o_name, o_pos.x, o_pos.y, o_pos.width, o_pos.length)
