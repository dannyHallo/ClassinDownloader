import os
import datetime
import pathlib
import subprocess
import shutil
from download import download, get_size


def checkCat(outputDir, vidName, subVidCount, vidsNeedToCat):
    if subVidCount == 0:
        return

    print('  patching...')

    # create new cat list
    catlist = open("temp/catlist.txt", "a")
    for subVidName in vidsNeedToCat:
        catlist.write('file \'../{}/{}.mp4\'\n'.format(outputDir, subVidName))
    catlist.close()

    if subVidCount > 0:
        if subVidCount > 1:
            subprocess.check_call('ffmpeg -f concat -safe 0 -i temp/catlist.txt -c copy {}/{}.mp4'.format(
                outputDir, vidName), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            for subVidName in vidsNeedToCat:
                os.remove('{}/{}.mp4'.format(outputDir, subVidName))

    open("temp/catlist.txt", "w").close()
    vidsNeedToCat.clear()

    print('  patched\n\n')


def main():
    urlPath = 'urls.txt'
    vidName = 'temp'
    subVidCount = 0
    vidsNeedToCat = []
    outputDir = "OUTPUT_{}".format(datetime.datetime.now().strftime("%H%M%S"))

    pathlib.Path('temp').mkdir(exist_ok=True)
    pathlib.Path(outputDir).mkdir(exist_ok=False)

    # delete '\'s and split lines into urls
    with open(urlPath, 'r') as f:
        urls = f.read().replace('\\', '').split('\n')

    open("temp/catlist.txt", "w").close()

    for url in urls:
        # setup video name
        if url.startswith('#'):
            checkCat(outputDir, vidName, subVidCount, vidsNeedToCat)
            subVidCount = 0

            vidName = url.split('#')[1].replace(' ', '_')
            if vidName.startswith('_'):
                vidName = vidName[1:]
            print(f'* starting to download {vidName}.mp4')

        # download from url
        elif url.startswith('http'):
            subVidCount += 1
            print('  downloading resource {} ({:.2f}MB)'.format(
                subVidCount, get_size(url)))
            subVidName = f'{vidName}_TEMP{subVidCount}'
            vidsNeedToCat.append(subVidName)

            download(url, f'{outputDir}/{subVidName}.mp4')

    checkCat(outputDir, vidName, subVidCount, vidsNeedToCat)
    f.close()
    shutil.rmtree('temp')


main()
