
import re

def get_file2ep(file_list):
    file2ep = {}
    for file in file_list:
        m = re.search(r'(\b|E|EP|#)(\d+)\b', file, flags=re.A | re.I)
        if m:
            file2ep[file] = int(m.group(2))
        else:
            file2ep[file] = -1

    return file2ep

def mapping_alg(video_files, files):
    # subtile filename is usually tidy, simply re.search
    file2ep = get_file2ep(files)
    video2ep = get_file2ep(video_files)
    
    return file2ep, video2ep