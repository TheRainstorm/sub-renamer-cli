import argparse
import json

from sub_renamer import get_videos
from mapping import get_file2ep

def get_ep2file(file2ep):
    ep2file = {}
    for file, ep in file2ep.items():
        if ep==-1:
            continue
        ep2file[ep] = file
    # sort
    ep_list = sorted(list(ep2file.keys()))
    ep2file_sorted = {k: ep2file[k] for k in ep_list}
    return ep2file_sorted
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--src',
                        required=True,
                        help='Path to the video directory')
    args = parser.parse_args()
    videos_files = get_videos(args.src)
    video2ep = get_file2ep(videos_files)
    ep2file = get_ep2file(video2ep)
    print(json.dumps(ep2file, indent=4, ensure_ascii=False))