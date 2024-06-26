import argparse
import json
import os
import logging
import re
import shutil
# from mapping_simple import mapping_alg
from mapping import mapping_alg

def get_videos(src_dir):
    video_files = []
    for f in os.listdir(src_dir):
        ext = os.path.splitext(f)[1]
        # video file
        if ext in ['.mkv', '.mp4']:
            video_files.append(f)
    return video_files

def extract_archive(archive_path, destination_dir):
    import zipfile
    import tarfile
    if zipfile.is_zipfile(archive_path):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(destination_dir)
    elif tarfile.is_tarfile(archive_path):
        with tarfile.open(archive_path, 'r') as tar_ref:
            tar_ref.extractall(destination_dir)
    else:
        logging.error(f"Extract {archive_path} failed. Unsupported file type.")

def get_subs(src):
    sub_files = []
    for f in os.listdir(src):
        ext = os.path.splitext(f)[1]
        # subtitle file
        if ext in ['.srt', '.ass']:
            sub_files.append(f)
    return sub_files

def sort_by_ep(file2ep):
    file_list = []
    ep_list = []
    for file, ep in file2ep.items():
        file_list.append(file)
        ep_list.append(ep)
    idx_list = list(range(len(ep_list)))
    idx_list.sort(key=lambda i: ep_list[i], reverse=True)
    return {file_list[i]: ep_list[i] for i in idx_list}

def rename(mapping_data):
    sub2ep = mapping_data['sub2ep']
    video2ep = mapping_data['video2ep']
    
    ep2video = {}
    for video_file, ep in video2ep.items():
        if ep==-1:
            continue
        if ep in ep2video:
            logging.warning(f"ep exist. {ep}: {ep2video[ep]} --> {video_file}")
        ep2video[ep] = video_file
    
    for sub_file, ep in sub2ep.items():
        if ep==-1:
            logging.error(f"sub miss ep {sub_file}")
            continue
        if ep not in ep2video:
            logging.error(f'ep {ep} match no file, {sub_file}')
            continue
        video_file = ep2video[ep]
        video_filename = os.path.splitext(video_file)[0]
        # get subtitle file language & ext
        # use \S, because it can contain general version info, like `KissSub&FZSD-TC`
        m = re.search(r'.*?(?P<lang>\.\S+)(?P<ext>\.\w+)', sub_file)
        if m:
            sub_lang = m.group('lang').lower()
            sub_ext = m.group('ext').lower()
        else:
            sub_lang = ''
            sub_ext = os.path.splitext(sub_file)[1]
        new_sub_file = f"{video_filename}{sub_lang}{sub_ext}"
        
        logging.info(f"{'Dryrun, ' if args.dry_run else ''}Copy {sub_file} to {new_sub_file}")
        if not args.dry_run:
            shutil.copy(os.path.join(args.sub_src, sub_file), os.path.join(args.video_src, new_sub_file))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Copy and rename subtitle file to video file.')
    parser.add_argument('--video-src',
                        required=True,
                        help='Path to the video directory')
    parser.add_argument('--sub-src',
                        required=True,
                        help='Path to the sub directory, or zip,tar file')
    parser.add_argument('-u', '--update',
                        action="store_true",
                        help='read json file and rename sub')
    parser.add_argument('-n', '--dry_run',
                        action="store_true",
                        help='Only generate json file')
    parser.add_argument('-v', '--verbose',
                        action="store_true",
                        help='print debug info')
    args = parser.parse_args()
    
    logging.basicConfig(
        format='[%(levelname)s]: %(message)s', 
        level=logging.DEBUG if args.verbose else logging.INFO)
    
    # check if sub_src is archive file, unzip it
    temp_path = os.path.join(os.getcwd(), 'temp')
    sub_src_is_archive = False
    if os.path.isfile(args.sub_src):
        # make temp dir
        os.makedirs(temp_path, exist_ok=True)
        extract_archive(args.sub_src, temp_path)
        files = os.listdir(temp_path)
        if len(files)==1:
            args.sub_src = os.path.join(temp_path, files[0])
        else:
            args.sub_src = os.path.join(temp_path)
        sub_src_is_archive = True
        
    mapping_json = 'mapping.json'
    if args.update:
        with open(mapping_json, encoding='utf-8') as f:
            mapping_data = json.load(f)
    else:
        video_files, sub_files = get_videos(args.video_src), get_subs(args.sub_src)
        sub2ep, video2ep = mapping_alg(video_files, sub_files)
        sub2ep = sort_by_ep(sub2ep)
        video2ep = sort_by_ep(video2ep)
        mapping_data = {'sub2ep':sub2ep, 'video2ep':video2ep}
        with open(mapping_json, 'w', encoding='utf-8') as f:
            json.dump(mapping_data, f, indent=4, ensure_ascii=False)

    rename(mapping_data)
    if sub_src_is_archive:
        shutil.rmtree(temp_path)