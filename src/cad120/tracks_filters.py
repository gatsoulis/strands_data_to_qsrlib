#!/usr/bin/env python

from __future__ import print_function
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle

from cad120_data_reader import CAD120_Data_Reader
from cad120_opencv_video_viewer.cad120_opencv_video_viewer import CAD120_OpenCV_Video_Viewer
import filters

class CAD120_Tracks_Filters(object):
    def __init__(self, reader):
        self.reader = reader


    def filter_skeleton(self, skeleton=("H", "RH", "LH"), jitter=False, lost=False):
        if jitter is None and lost is None:
            return

        all_episodes_skeleton_tracks = self.reader.world_skeleton_traces_to_dict()
        # print(all_episodes_tracks["Subject1_arranging_objects_0510175411"].keys())
        for id, tracks in all_episodes_skeleton_tracks.items():
            if jitter:
                for j in skeleton:
                    # print(j, tracks[j])
                    tracks[j] = filters.threshold_filter(tracks[j], 3)
                    tracks[j] = filters.median_filter(tracks[j], 2)
                    # print(j, tracks[j])
                    # print()

            if lost:
                raise NotImplementedError

            self.change_reader(id, tracks)
            # foo = []
            # obj = "RH"
            # world_trace = self.reader.world_traces[id]
            # sorted_timestamps = world_trace.get_sorted_timestamps()
            # for t in sorted_timestamps:
            #     world_state = world_trace.trace[t]
            #     foo.append((world_state.objects[obj].x, world_state.objects[obj].y))
            # print(foo)


    def change_reader(self, id, tracks):
        world_trace = self.reader.world_traces[id]
        sorted_timestamps = world_trace.get_sorted_timestamps()
        for j, track in tracks.items():
            if len(sorted_timestamps) != len(track):
                raise ValueError(id, j, "len(sorted_timestamps, track):", len(sorted_timestamps), len(track))

            for p, t in zip(track, sorted_timestamps):
                world_state = world_trace.trace[t]
                world_state.objects[j].x = p[0]
                world_state.objects[j].y = p[1]


    # def filter_skeleton_lost_track(self, thresholds={"H": 10, "LH": 50, "RH": 50}):
    #     for k, world_trace in self.reader.world_traces.items():
    #         print(k, world_trace)
    #         sorted_timestamps = world_trace.get_sorted_timestamps()
    #         # length_time = len(sorted_timestamps)
    #         tracks = {}
    #         for j in thresholds.keys():
    #             tracks[j] = []
    #         for i in range(len(sorted_timestamps)):
    #             t = sorted_timestamps[i]
    #             world_state = world_trace.trace[t]
    #             for j in thresholds.keys():
    #                 tracks[j].append((world_state.objects[j].x, world_state.objects[j].y))
    #         tracks_filtered = self.__filter_skeleton_lost_track(tracks, thresholds)


    def __filter_skeleton_lost_track(self, tracks, thresholds):
        # with open("/home/yiannis/tracks_for_filter")
        print()
        ret = None
        track = tracks["RH"]
        # tracks = [(int(i[0]), int(i[1])) for i in tracks]
        print(track)
        # foo = [1, 2, 3, 4]
        # for i, j in zip(foo[1:], foo):
        #     print(i, j)
        dists = [filters.euclidean(p1, p2) for p1, p2 in zip(track[1:], track)]
        print(dists)
        # plt.scatter(*zip(*tracks["RH"]), color="blue")
        # plt.scatter(*zip(*tracks["LH"]), color="red")
        # plt.scatter(*zip(*tracks["H"]), color="green")
        # plt.show()
        return ret



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ini", help="ini file", required=True)
    parser.add_argument("-e", "--episode", help="episode")
    args = parser.parse_args()

    inis_path = os.environ.get("INIS")
    ini = os.path.join(inis_path, "strands_data_to_qsrlib", str(args.ini)) if inis_path else args.ini

    reader = CAD120_Data_Reader(config_filename=ini, episode=args.episode)
    du = reader.world_skeleton_traces_to_dict()
    filename = os.path.join(os.environ.get("CLOUD"), "work_datasets/CAD120_pickles/filters_data", "unfiltered_tracks.p")
    with open(filename, "wb") as f:
        pickle.dump(du, f)


    smoother = CAD120_Tracks_Filters(reader=reader)
    smoother.filter_skeleton(jitter=True)

    # viewer = CAD120_OpenCV_Video_Viewer("/home/yiannis/datasets/CAD120", reader)
    # viewer.show_videos("all", fps=100)

    df = reader.world_skeleton_traces_to_dict()
    filename = os.path.join(os.environ.get("CLOUD"), "work_datasets/CAD120_pickles/filters_data", "filtered_tracks.p")
    with open(filename, "wb") as f:
        pickle.dump(df, f)
