import re

def get_common_prefix(s1, s2):
    n = min(len(s1), len(s2))
    i = 0
    while i<n and s1[i]==s2[i]:
        i += 1
    prefix = s1[:i]
    # delete ending digit
    j = len(prefix) - 1
    while j>=0 and prefix[j].isdigit():
        j -= 1
    return prefix[:j+1]

def find_longest_common_prefix(file_list):
    n = len(file_list)
    if n==1:
        return "", 0, 0
    max_len, start, end = 0, 0, 0
    i, j = 0, 0
    while i < n:
        j = i + 1
        if j>=n:
            break
        prefix = get_common_prefix(file_list[i], file_list[j])
        j += 1
        while j<n and prefix==get_common_prefix(file_list[i], file_list[j]):
            j += 1
        if j - i > max_len:
            start, end = i, j-1
            max_len = j - i
        if j==i+2:  # two file section, we should also try use single file
            i = j - 1
        else:
            i = j   # S01, S02 boundary, i should jump to S02, otherwise new prefix will be S0
    # start < end
    return get_common_prefix(file_list[start], file_list[start+1]), start, end

def get_file2ep_try_prefix(file_list):
    file_list.sort()
    prefix, start, end = find_longest_common_prefix(file_list)
    if prefix=="":
        return False, {}
    file2ep = {}
    escaped_prefix = re.escape(prefix)
    success = False
    for i in range(len(file_list)):
        if start <= i <= end:
            m = re.search(rf'{escaped_prefix}(\d+)', file_list[i], flags=re.A | re.I)
            if m:
                file2ep[file_list[i]] = int(m.group(1))
                success = True
            else:
                file2ep[file_list[i]] = -1
        else:
            file2ep[file_list[i]] = -1
    if success:
        return True, file2ep
    return False, {}

def get_all_empty(file_list):
    file2ep = {}
    for file in file_list:
        file2ep[file] = -1
    return file2ep

def get_file2ep(file_list):
    success, file2ep = get_file2ep_try_prefix(file_list)
    if not success:
        return get_all_empty(file_list)
    return file2ep
