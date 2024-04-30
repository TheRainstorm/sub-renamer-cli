import argparse
import json
import os

from sub_renamer import get_videos
from mapping import get_file2ep
from test_file2ep import get_ep2file

def generate_benchmark(src):
    result_json = os.path.join("result.json")
    result = {}
    for file in os.listdir(src):
        file_path = os.path.join(src, file)
        if os.path.isdir(file_path):
            print(f"Processing {file}")
            video2ep = process_single_dir(file_path)
            if not video2ep:
                print(f"Empty {file}")
                continue
            # sort
            video2ep = {k: v for k, v in sorted(video2ep.items(), key=lambda item: item[1])}
            result[file] = video2ep
    with open(result_json, 'w') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

def process_single_dir(src):
    videos_files = get_videos(src)
    video2ep = get_file2ep(videos_files)
    return video2ep

def test_benchmark(src):
    with open(src, 'r') as f:
        benchmark = json.load(f)
    tv_cnt, tv_error_cnt, episode_cnt, episode_error_cnt = 0, 0, 0, 0
    
    for dir, ref_result in benchmark.items():
        tv_cnt += 1
        video_list = list(ref_result.keys())
        video2ep = get_file2ep(video_list)
        print(f"Testing {dir}")
        # compare
        tv_error_flag = False
        for video, ep in ref_result.items():
            episode_cnt += 1
            if video2ep[video] != ep:
                tv_error_flag = True
                episode_error_cnt += 1
                print(f"Error Ref: {ep:3d} Get:{video2ep[video]:3d} {video}")
        if tv_error_flag:
            tv_error_cnt += 1
    # print Summary
    print("\nSummary:")
    print(f"TV error rate:      {f'{tv_error_cnt}/{tv_cnt}':10s} {tv_error_cnt/tv_cnt*100:.2f}%")
    print(f"Episode error rate: {f'{episode_error_cnt}/{episode_cnt}':10s} {episode_error_cnt/episode_cnt*100:.2f}%")
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src',
                        required=True,
                        help='Path to the benchmark json file | episode top directory (in generate mode)')
    parser.add_argument('-g', '--generate',
                        action='store_true',
                        help='generate benchmark json file')
    args = parser.parse_args()
    if args.generate:
        generate_benchmark(args.src)
    else:
        test_benchmark(args.src)
    