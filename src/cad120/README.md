## Description
Make CAD120 data compatible with QSRlib

## Notes

### Config files

* There is a config file on `cad120/config.ini`
```ini
[cad120_data_reader]
path = /Users/yiannis/Dropbox/work_datasets/CAD120_partial
corrected_labeling_path = /Users/yiannis/Dropbox/work_datasets/CAD120_partial
; use load_from_files=True in the constructor to load from the following files
sub_sequences_filename = /Users/yiannis/Dropbox/work_datasets/CAD120_pickles/sub_sequences_corrected.p
sub_time_segmentation_filename = /Users/yiannis/Dropbox/work_datasets/CAD120_pickles/sub_time_segmentations_corrected.p
ground_truth_tracks_filename = /Users/yiannis/Dropbox/work_datasets/CAD120_pickles/ground_truth_tracks.p
```
* Also I have the following:

`collapsed_sequences.ini`
```ini
[cad120_data_reader]
; sub_sequences are collapsed resulting in no self-loops in the transitions
path = /Users/yiannis/Dropbox/work_datasets/CAD120_partial
corrected_labeling_path = /Users/yiannis/Dropbox/work_datasets/CAD120_partial
; use load_from_files=True in the constructor to load from the following files
sub_sequences_filename = /Users/yiannis/Dropbox/work_datasets/CAD120_pickles/sub_sequences_corrected_collapsed.p
sub_time_segmentation_filename = /Users/yiannis/Dropbox/work_datasets/CAD120_pickles/sub_time_segmentations_corrected.p
ground_truth_tracks_filename = /Users/yiannis/Dropbox/work_datasets/CAD120_pickles/ground_truth_tracks.p
```

`normal_sequences.ini`
```ini
[cad120_data_reader]
; sub_sequences are normal resulting in self-loops in the transitions
path = /Users/yiannis/Dropbox/work_datasets/CAD120_partial
corrected_labeling_path = /Users/yiannis/Dropbox/work_datasets/CAD120_partial
; use load_from_files=True in the constructor to load from the following files
sub_sequences_filename = /Users/yiannis/Dropbox/work_datasets/CAD120_pickles/sub_sequences_corrected.p
sub_time_segmentation_filename = /Users/yiannis/Dropbox/work_datasets/CAD120_pickles/sub_time_segmentations_corrected.p
ground_truth_tracks_filename = /Users/yiannis/Dropbox/work_datasets/CAD120_pickles/ground_truth_tracks.p
```
