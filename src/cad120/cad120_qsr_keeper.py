# -*- coding: utf-8 -*-
"""
CAD120 data reader that is compatible with QSRlib.

:Author: Yiannis Gatsoulis <y.gatsoulis@leeds.ac.uk>
:Organization: University of Leeds
"""

from __future__ import print_function, division
import sys
import argparse
import timeit
import ConfigParser
import os
try:
    import cPickle as pickle
except ImportError:
    import pickle
from cad120_data_reader import CAD120_Data_Reader
from qsrlib.qsrlib import QSRlib, QSRlib_Request_Message


class CAD120_QSR_Keeper(object):
    def __init__(self, description="", reader=None, qsrlib=None, which_qsr="", load_from_file=""):
        start = timeit.default_timer()
        print("\n--", self.__class__.__name__)
        print("Generating QSRs...")

        cloud_path = os.environ.get("CLOUD")

        self.description = description
        self.reader = reader
        self.qsrlib = qsrlib
        self.which_qsr = which_qsr
        self.world_qsr_traces = {}

        if load_from_file is not None and load_from_file != "":
            if cloud_path is not None:
                load_from_file = os.path.join(cloud_path, load_from_file)
            self.load(load_from_file)
        else:
            if type(self.reader) is not CAD120_Data_Reader:
                raise TypeError("Provide a CAD120_Data_Reader object")
            if type(self.qsrlib) is not QSRlib:
                raise TypeError("Provide a QSRlib object")
            if self.which_qsr == "":
                raise ValueError("Provide an appropriate QSR")
            self.make()

        stop = timeit.default_timer()
        print("QSRs generated in: %.2f secs" % (stop - start))

    def make(self, qsrlib=None):
        if qsrlib:
            self.qsrlib = qsrlib
        if self.qsrlib is None:
            raise TypeError("Pass a QSRlib object")
        for k, world_trace in zip(self.reader.world_traces.keys(), self.reader.world_traces.values()):
            request_message = QSRlib_Request_Message(which_qsr=self.which_qsr, input_data=world_trace, include_missing_data=True)
            # out = self.qsrlib.request_qsrs(request_message=request_message)
            self.world_qsr_traces[k] = self.qsrlib.request_qsrs(request_message=request_message)

    def save(self, filename):
        print("Saving...")
        foo = {"description": self.description, "which_qsr": self.which_qsr, "world_qsr_traces": self.world_qsr_traces}
        with open(filename, "wb") as f:
            pickle.dump(foo, f)
        print("\t\tdone")

    def load(self, filename):
        print("Loading QSRs from", filename, end="")
        with open(filename, "rb") as f:
            foo = pickle.load(f)
        self.description = foo["description"]
        self.which_qsr = foo["which_qsr"]
        self.world_qsr_traces = foo["world_qsr_traces"]
        print("\t\tdone")


if __name__ == '__main__':
    start = timeit.default_timer()

    options = {"sg1": "sg1",
               "rcc3": "rcc3_rectangle_bounding_boxes_2d"}
    parser = argparse.ArgumentParser(description="CAD120 QSR keeper in QSRlib format")
    parser.add_argument("-i", "--ini", help="ini file", required=True)
    parser_group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument("-s", "--save", help="filename to save qsrs", type=str)
    # parser_group.add_argument("-l", "--load", help="ini file that holds the qsrs filename, qsrs loaded from that file instead of being created from data", type=str)
    parser_group.add_argument("-l", "--load", dest="load", action="store_true", help="load the data qsrs the file in 'config.ini'")
    parser_group.add_argument("--qsr", help="choose qsr: %s" % options.keys(), type=str)
    args = parser.parse_args()

    cfg = ConfigParser.SafeConfigParser()
    if len(cfg.read(args.ini)) == 0:
        raise ValueError("config file not found")

    if not args.load:
        try:
            reader_load = cfg.getboolean("cad120_data_keeper", "reader_load")
        except ConfigParser.NoOptionError:
            raise

        try:
            which_qsr = options[args.qsr]
        except (IndexError, KeyError) as e:
            parser.print_help()
            sys.exit(1)

        qsrlib = QSRlib()
        reader = CAD120_Data_Reader(config_filename=args.ini, load_from_files=reader_load)
        print()
        keeper = CAD120_QSR_Keeper(description="description", reader=reader, qsrlib=qsrlib, which_qsr=which_qsr)
        # optional saving
        if args.save:
            keeper.save(filename=args.save)
    else:
        try:
            qsrs_filename = cfg.get("cad120_data_keeper", "qsrs_filename")
        except ConfigParser.NoOptionError:
            raise
        keeper = CAD120_QSR_Keeper(load_from_file=qsrs_filename)

    stop = timeit.default_timer()
    print("Total execution time: %.2f secs" % (stop - start))
