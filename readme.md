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

## Algorithm

`classic` is sophisticated and generic. `prefix` method is simple but incredible effective.

### classic

1. Extract all numbers from the filenames. This ensures that the true episode number is **not lost**.
2. Identify the episode number range **(ep_start, ep_end)** based on the assumption that ep is usually continuous.
3. Then filter out irrelevant numbers such as x265, 1080p, etc.
4. Some numbers may be common across all filenames, such as season numbers or audio formats like 5.1ch/2ch. Get this list of common numbers and sort them by frequency. For each file, **exclude the common numbers** unless it is the only number left.
5. Generate a mapping of episode numbers to all possible files. Certain episode numbers are exclusively **mapped to single files**, serving as reference files.
6. For each episode number, select the most probable file by comparing its similarity to the reference files.

drawback:

- don't work when common numbers repeat in the filename

### common prefix

1. sort filename by alphabetical order
2. find longest common prefix
3. construct the regular expression to extract episode number (`{prefix}\d+`)
