import os
import pathlib
import subprocess
import shutil
import download


def checkCat(outputDir, vidName, subVidCount, vidsNeedToCat):

    if subVidCount > 1:
        print('  patching...')

        # generate cat list
        catlist = open("temp/catlist.txt", "a")
        for subVidName in vidsNeedToCat:
            catlist.write(
                'file \'../{}/{}.mp4\'\n'.format(outputDir, subVidName))
        catlist.close()

        # cat vid and rename
        subprocess.check_call('lib/ffmpeg.exe -f concat -safe 0 -i temp/catlist.txt -c copy {}/{}.mp4'.format(
            outputDir, vidName), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        for subVidName in vidsNeedToCat:
            os.remove(f'{outputDir}/{subVidName}.mp4')

    else:
        os.rename(
            f'{outputDir}/{vidsNeedToCat[0]}.mp4', f'{outputDir}/{vidName}.mp4')

    # clear cat list
    open("temp/catlist.txt", "w").close()
    vidsNeedToCat.clear()
    print('  done\n')


def main():
    urlPath = ''

    # delete '\'s and split lines into urls
    try:
        urlPath = 'urls.txt'
        with open(urlPath, 'r', encoding='utf-8') as f:
            lines = f.read().replace('\\', '').split('\n')
    except FileNotFoundError:
        urlPath = '../urls.txt'
        with open(urlPath, 'r', encoding='utf-8') as f:
            lines = f.read().replace('\\', '').split('\n')

    vidName = ''
    subVidCount = 0
    vidsNeedToCat = []
    outputDir = ''

    pathlib.Path('temp').mkdir(exist_ok=True)

    open("temp/catlist.txt", "w").close()

    for line in lines:
        if line == '':
            continue

        if line.startswith('#'):
            outputFolderName = line[line.find(' ') + 1:]
            outputDir = f'downloaded/{outputFolderName}'
            pathlib.Path(outputDir).mkdir(parents=True, exist_ok=True)
            print('--------------------------------------------------------------------')
            print(f'the following classes are downloaded to: {outputDir}')
            print('--------------------------------------------------------------------')
            continue

        lineElements = line.split(' ')
        vidName = lineElements[0]   # get the video name
        subVidCount = len(lineElements) - 1  # how many subvids in this line?

        print(f'* downloading recording: {vidName}.mp4')

        # if lineElements.count == 2:

        # download all tmp videos for this vid
        for i in range(1, len(lineElements)):
            currentUrl = lineElements[i]

            print('  -> sub-source {} ({:.2f}MB)'.format(
                i, download.get_size(currentUrl)))
            subVidName = f'{vidName}_{i}'
            vidsNeedToCat.append(subVidName)

            download.download(currentUrl, f'{outputDir}/{subVidName}.mp4')

        checkCat(outputDir, vidName, subVidCount, vidsNeedToCat)

    f.close()
    shutil.rmtree('temp')


main()
