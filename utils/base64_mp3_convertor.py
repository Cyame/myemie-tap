import base64
import os
import sys
import json
import shutil

thisUtilsPath = os.path.split(os.path.realpath(sys.argv[0]))[0]
mainJsonPath = os.path.join(thisUtilsPath, '..', 'data', 'main', 'main.json')
trackJsonPath = os.path.join(thisUtilsPath, '..', 'data', 'track',
                             'track.json')
thisMP3Path = os.path.join(thisUtilsPath, 'mp3')

main_encoded = {}
track_encoded = {}


def del_path(path):
    if not os.path.exists(path):
        return
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)


def encoder():

    for dic, _, filelist in os.walk(thisMP3Path):
        if 'main' in dic:
            for file in filelist:
                fullpath = os.path.join(dic,file)
                with open(fullpath, 'rb') as f:
                    data = f.read()
                    base64Data = base64.b64encode(data)
                    # print(base64Data)
                    main_encoded[file] = 'data:audio/mp3;base64,' + str(base64Data,encoding='utf8')
        if 'track' in dic:
            for file in filelist:
                fullpath = os.path.join(dic,file)
                with open(fullpath, 'rb') as f:
                    data = f.read()
                    base64Data = base64.b64encode(data)
                    # print(base64Data)
                    track_encoded[file] = 'data:audio/mp3;base64,' + str(base64Data,encoding='utf8')
    with open(mainJsonPath, 'w', encoding='utf8') as mainjs:
        json.dump(main_encoded, mainjs)
    with open(trackJsonPath, 'w', encoding='utf8') as trackjs:
        json.dump(track_encoded, trackjs)    


def decoder():
    mainjs = open(mainJsonPath, 'r', encoding='utf8')
    trackjs = open(trackJsonPath, 'r', encoding='utf8')
    main_encoded = dict(json.load(mainjs))
    track_encoded = dict(json.load(trackjs))
    
    del_path(os.path.join(thisMP3Path,'main'))
    del_path(os.path.join(thisMP3Path,'track'))
    os.mkdir(os.path.join(thisMP3Path,'main'))
    os.mkdir(os.path.join(thisMP3Path,'track'))

    for filename, base64coding in main_encoded.items():
        with open(os.path.join(thisMP3Path,'main',filename) , 'wb') as f:
            # print(base64coding[22:])
            f.write(base64.b64decode(base64coding[22:]))
    for filename, base64coding in track_encoded.items():
        with open(os.path.join(thisMP3Path,'track',filename) , 'wb') as f:
            # print(base64coding[22:])
            f.write(base64.b64decode(base64coding[22:]))


if __name__ == "__main__":

    assert len(sys.argv) > 1, 'Please input argv to encode/decode'

    if sys.argv[1] == 'decode':
        decoder()
        print("DECODE FINISHED")
    elif sys.argv[1] == 'encode':
        encoder()
        print("ENCODE FINISHED")
    else:
        raise IOError("Please input correct argv to encode/decode.")