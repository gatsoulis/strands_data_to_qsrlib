#!/usr/bin/env python
from __future__ import print_function
import argparse

from qsrlib.qsrlib import QSRlib, QSRlib_Request_Message
from csv_to_qsrlib_data_reader import CSV_to_QSRlib_Data_Reader
from qsr_keeper import QSR_Keeper

if __name__ == '__main__':
    options = {"rcc2": "rcc2_rectangle_bounding_boxes_2d",
               "rcc3": "rcc3_rectangle_bounding_boxes_2d",
               "rcc8": "rcc8_rectangle_bounding_boxes_2d",
               "cone_direction": "cone_direction_bounding_boxes_centroid_2d",
               "qtcb": "qtc_b_simplified",
               "qtcc": "qtc_c_simplified",
               "qtcbc": "qtc_bc_simplified",
               "rcc3a": "rcc3_rectangle_bounding_boxes_2d",
               "arg_distance": "arg_relations_distance"}

    argp = argparse.ArgumentParser(description="csv to QSRlib world trace format")
    argp.add_argument("-p", "--path", required=True, help="directory path where the files are")
    argp.add_argument("-q", "--qsr", required=True, help="QSR")
    argp.add_argument("--skeleton", help="skeleton filename")
    argp.add_argument("-l", "--load", help="pickle filename to load")
    argp.add_argument("-s", "--save")
    argp.add_argument("--skel_world", action="store_true", help="skeleton is in world coordinates (else assumed to be in pixels coordinates)")
    args = argp.parse_args()

    try:
        qsr = options[args.qsr]
    except KeyError:
        raise ValueError("qsr not found, must be one of:", options.keys())

    reader = CSV_to_QSRlib_Data_Reader(mypath=args.path, skeleton_filename=args.skeleton,
                                       skeleton_world_coords=args.skel_world,
                                       skeleton_csv_format="frame_skeleton_id",
                                       joints=["head", "left_hand", "right_hand"])

    qsrlib = QSRlib()
    keeper = QSR_Keeper(qsrlib=qsrlib, world_trace=reader.world_trace, qsr=qsr)
