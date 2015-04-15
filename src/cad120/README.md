## Description
Make CAD120 data compatible with QSRlib

## Notes

### Run
#### `cad120_data_reader.py` examples
* Loading from raw `-i config.ini`. The path to raw is specified in `config.ini`
* Loading from pickles `-i config.ini -l`. The pickles filenames are specified in `config.ini`

#### `cad120_data_keeper.py` examples
* Computing qsrs `-i config.ini --qsr rcc3`
* Loading qsrs from file: `-i config.ini -l`. The QSRs filename to load is specified in the `config.ini`

### Environment variables
* `CLOUD`: where the datafiles are, since they are usually stored in one of my cloud sharing account, hence the name
* `INIS`: path to `strands_my_inis` folder

### Config files
Pass it as `-i` argument when running the `cad120_data_reader.py` or `cad120_data_keeper.py`

```ini
[cad120_data_reader]
raw_tracks_path = /home/yiannis/datasets/CAD120
corrected_labeling_path = /home/yiannis/Dropbox/work_datasets/CAD120_partial
; use load_from_files=True in the constructor to load from the following files
sub_sequences_filename = work_datasets/CAD120_pickles/sub_sequences_corrected.p
sub_time_segmentation_filename = work_datasets/CAD120_pickles/sub_time_segmentations_corrected.p
ground_truth_tracks_filename = work_datasets/CAD120_pickles/ground_truth_tracks.p

[cad120_data_keeper]
; used if -l passed
qsrs_filename = work_datasets/CAD120_pickles/qsr_keeper_sg1.p
reader_load = true
```

### `CLOUD` environment variable
Export `CLOUD` to use relative paths in `config.ini`
