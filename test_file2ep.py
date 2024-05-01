import argparse
import json
import logging

from sub_renamer import get_videos

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
    parser.add_argument('-a', '--alg',
                        type=int,
                        default=2,
                        help='select mapping alg, 0: classic, 1: prefix, 2: combined')
    parser.add_argument('-v', '--verbose',
                        action="store_true",
                        help='print debug info')
    args = parser.parse_args()
    
    logging.basicConfig(
        format='[%(levelname)s]: %(message)s', 
        level=logging.DEBUG if args.verbose else logging.INFO)
    
    if args.alg==0:
        from mapping import get_file2ep
        print("Using classic mapping")
    elif args.alg==1:
        from mapping_prefix import get_file2ep
        print("Using prefix mapping")
    else:
        print("Using combined mapping")
        from mapping import get_file2ep_combined as get_file2ep
    
    videos_files = get_videos(args.src)
    video2ep = get_file2ep(videos_files)
    ep2file = get_ep2file(video2ep)
    print(json.dumps(ep2file, indent=4, ensure_ascii=False))