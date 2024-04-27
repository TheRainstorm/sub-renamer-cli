
import json
import re
import difflib
import logging

cnt = 0
def print_json(data):
    global cnt
    data_new = {k : list(v) for k, v in data.items()}
    cnt += 1
    with open(f'data-{cnt}.json', 'w', encoding='utf-8') as f:
        json.dump(data_new, f, indent=4, ensure_ascii=False)

def get_set_first(s):
    for x in s:
        return x
    
def get_possible_eps(filename):
    # S01E01, #01, 01
    m = re.search(r'(\b|E|EP|#)(\d+)\b', filename, flags=re.A | re.I)
    if m:
        return [int(m.group(2))]
    return []
    # fallback to all digits
    ep_list = re.findall(r'\d+\b', filename)
    ep_list = [int(ep) for ep in ep_list]
    return ep_list

def find_longest_roughly_continuous_range(nums, k=2):
    nums.sort()
    max_len, start, end = 0, 0, 0
    n = len(nums)
    i, j = 0, 0
    while i < n:
        j = i + 1
        while j<n and nums[j] - nums[j-1] <= k:
            j += 1
        if j - i > max_len:
            start, end = nums[i], nums[j-1]
            max_len = j - i
        i = j
    return start, end

def filter_invalid_ep(ep2files, k=2):
    invalid_ep = []
    # k is how many eps can be lose. 1 mean can't lose
    start_ep, end_ep = find_longest_roughly_continuous_range(list(ep2files.keys()), k=k)
    for ep in list(ep2files.keys()):
        if ep < start_ep or ep > end_ep:
            ep2files.pop(ep)
            invalid_ep.append(ep)
    logging.debug("Invalid eps:", invalid_ep)
    return ep2files

    # for each ep, we find the corresponding files.
def get_ep2files(file2eps):
    # we than keep track of each ep and the corresponding files.
    ep2files = {}
    for file, eps in file2eps.items():
        for ep in eps:
            if ep not in ep2files:
                ep2files[ep] = set()
            ep2files[ep].add(file)
    return ep2files

def get_ref(ep2files):
    ref_files = set()
    for ep, files in ep2files.items():
        if len(files)==1:
            ref_files.add(get_set_first(files))
    return ref_files

def clear_ref(ep2files, ref_files):
    for ep, files in ep2files.items():
        if len(files)>1:
            ep2files[ep] = files - ref_files

def get_max_score_file(files, ref_files):
    def get_score(file, ref_files):
        # caculate the sum of similarity to all reference files. bigger is better.
        score = 0
        for ref_file in ref_files:
            score += difflib.SequenceMatcher(None, file, ref_file).ratio()
        return score
    score_list = []
    for file in files:
        score_list.append(get_score(file, ref_files))
    max_idx = score_list.index(max(score_list))
    return files[max_idx]
        
def get_file2ep(file_list):
    # for each filename, we extract all possible ep.
    file2eps = {}
    for file in file_list:
        ep_list = get_possible_eps(file)
        ep_set = set(ep_list)
        file2eps[file] = ep_set
    
    # for each ep, we find the corresponding files.
    ep2files = get_ep2files(file2eps)
    
    # filter invalid ep like random number, x264, 720p, etc
    filter_invalid_ep(ep2files)
    
    # print_json(file2eps)
    # print_json(ep2files)
    
    # Since the right episode numbers is a range [ep_start, ep_end]
    # There is always some ep corresponding to only one file.
    # Then we use these reference files to find other files have simliar names.
    ref_files = get_ref(ep2files)
    # for ref_files, we remove them from other eps.
    clear_ref(ep2files, ref_files)
    
    file2ep = {}
    # for ep corresponding to many files, we choose the one with max score.
    for ep, files in ep2files.items():
        if len(files)==1:
            file2ep[get_set_first(files)] = ep
        if len(files)>1:
            file = get_max_score_file(list(files), ref_files)
            file2ep[file] = ep
    
    # for other file, we set ep to -1
    for file in file_list:
        if file not in file2ep:
            file2ep[file] = -1
    
    return file2ep

def mapping_alg(video_files, sub_files):
    sub2ep = get_file2ep(sub_files)
    video2ep = get_file2ep(video_files)
    
    return sub2ep, video2ep