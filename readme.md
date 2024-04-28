## Description

Yet another subtitle file renamer program.

Key Feature

1. Simple but effective matching algorithm.
2. Fix mismatching by modifying json file directly (quick and easy)
3. Modularized code, easy to modify according to your need.

## Usage

```shell
usage: sub_renamer.py [-h] --video-src VIDEO_SRC --sub-src SUB_SRC [-u] [-n]

Copy and rename subtitle file to video file.

options:
  -h, --help            show this help message and exit
  --video-src VIDEO_SRC
                        Path to the video directory
  --sub-src SUB_SRC     Path to the sub directory, or zip,tar file
  -u, --update          read json file and rename sub
  -n, --dry_run         Only generate json file
```

example

```shell
# dry run
python sub_renamer.py --video-src '/mnt/Disk1/BT/Video/Anime/[ANK-Raws] 六花の勇者 (BDrip 1920x1080 HEVC-YUV420P10 FLAC)' --sub-src '/mnt/Disk1/[Beatrice-Raws] Rokka no Yuusha [Subs].zip' -n

# check mapping.json file for mismatching
# you can correct the result
vim mapping.json

# copy and rename subtitle file
python sub_renamer.py --video-src '/mnt/Disk1/BT/Video/Anime/[ANK-Raws] 六花の勇者 (BDrip 1920x1080 HEVC-YUV420P10 FLAC)' --sub-src '/mnt/Disk1/[Beatrice-Raws] Rokka no Yuusha [Subs].zip' -u
```
