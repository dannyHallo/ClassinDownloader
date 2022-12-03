import requests
from time import time
from concurrent.futures import ThreadPoolExecutor, as_completed

num_of_tasks = 4
chunk_size = 4096


def calc_divisional_range(filesize, numTask):
    step = filesize // numTask
    result = []
    startingPoint = 0

    for _ in range(numTask-1):
        s_pos, e_pos = startingPoint, startingPoint + step
        startingPoint = startingPoint + step + 1
        result.append([s_pos, e_pos])

    result.append([startingPoint, filesize - 1])
    return result


def range_download(save_name, url, s_pos, e_pos):
    headers = {"Range": f"bytes={s_pos}-{e_pos}"}
    res = requests.get(url, headers=headers, stream=True)
    with open(save_name, "rb+") as f:
        f.seek(s_pos)
        for chunk in res.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)

def get_size(url):
    res = requests.head(url)
    filesize = int(res.headers['content-length'])
    return filesize / (1024 * 1024)

def download(url, save_path):
    res = requests.head(url)
    filesize = int(res.headers['content-length'])
    divisional_ranges = calc_divisional_range(
        filesize=filesize, numTask=num_of_tasks)

    with open(save_path, 'wb'):
        pass

    with ThreadPoolExecutor() as p:
        futures = []
        for s_pos, e_pos in divisional_ranges:
            futures.append(
                p.submit(range_download, save_path, url, s_pos, e_pos))

        as_completed(futures)
