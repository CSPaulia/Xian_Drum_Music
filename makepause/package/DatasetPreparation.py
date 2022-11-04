import os
import pretty_midi
import numpy as np
import random
import sys

filepath = 'TrainSet/equilong10/'
filenotenum = 10


def checkdata(fp, fnn):
    try:
        num = 0
        for mididic in os.listdir(fp):
            if mididic != '.DS_Store':
                for midi in os.listdir(fp + mididic):
                    if midi.split('.')[1] == 'mid':
                        midi_data = pretty_midi.PrettyMIDI(fp + mididic + '/' + midi)
                        for instrument in midi_data.instruments:
                            if not instrument.is_drum:
                                if len(instrument.notes) != fnn:
                                    print('The length of (' + midi + ') is not correct.' + ' Its length is ' + str(
                                        len(instrument.notes)))
                                    os.remove(fp + mididic + '/' + midi)
                                else:
                                    num += 1
        print('There are ' + str(num) + ' Data.')
    except NotADirectoryError:
        pass


def getdata(fp):
    DataX = []
    DataY = []
    tagset = set()
    try:
        pitches = []
        time = []
        for mididic in os.listdir(fp):
            if mididic != '.DS_Store':
                for midi in os.listdir(fp + mididic):
                    midi_data = pretty_midi.PrettyMIDI(fp + mididic + '/' + midi)
                    for instrument in midi_data.instruments:
                        if not instrument.is_drum:
                            for note in instrument.notes:
                                pitches.append([note.pitch])
                                time.append([round(note.end - note.start, 1)])
                                tagset.add(round(note.end - note.start, 1))
                            DataX.append(pitches)
                            DataY.append(time)
                        pitches = []
                        time = []
    except NotADirectoryError:
        pass
    DataX = np.array(DataX)
    DataY = np.array(DataY)
    print('the shape of training data:', DataX.shape)
    DataY = tag2onehot(DataY, tagset)
    print('the shape of training data\'s tag:', DataY.shape)
    print('the length of tag set:', len(tagset))
    print('tag set:', tagset)

    tag = list(tagset)
    tag.sort()
    tag = np.array(tag)
    np.save('TrainSet/' + fp.replace('/', '_') + 'tag.npy', tag)

    return DataX, DataY, tagset


def tag2onehot(DataY, tagset):
    DataYonehot = []

    tagset = list(tagset)
    tagsetlength = len(tagset)
    tagset.sort()

    timeonehot = []

    falsenum = 0
    for i in range(len(DataY)):
        for j in range(len(DataY[i])):
            y = [0 for k in range(tagsetlength)]
            if DataY[i][j][0] in tagset:
                y[tagset.index(DataY[i][j][0])] = 1
            else:
                falsenum += 1
                y[random.randint(0, tagsetlength - 1)] = 1
            timeonehot.append(y)
        DataYonehot.append(timeonehot)
        timeonehot = []
    DataYonehot = np.array(DataYonehot)

    print('There are ', falsenum, ' time not in tagset.')
    if falsenum > len(DataYonehot) * 0.1:
        print('There are so many time not in tagset. Program terminated.')
        sys.exit()
    return DataYonehot


def datacut(fp, fnn, tagset):
    datax = []
    datay = []
    datafrom = []
    try:
        for midi in os.listdir(fp):
            if midi != '.DS_Store':
                if midi.split('.')[1] == 'mid':
                    midi_data = pretty_midi.PrettyMIDI(fp + midi)
                    for instrument in midi_data.instruments:
                        if not instrument.is_drum:
                            for i in range(int(len(instrument.notes) / fnn)):
                                pitches = []
                                time = []
                                for j in range(i * fnn, i * fnn + fnn):
                                    pitches.append([instrument.notes[j].pitch])
                                    time.append([round(instrument.notes[j].end - instrument.notes[j].start, 1)])
                                datax.append(pitches)
                                datay.append(time)
                                datafrom.append(midi)
    except NotADirectoryError:
        pass
    datax = np.array(datax)
    datay = np.array(datay)
    print('the shape of training data:', datax.shape)
    datay = tag2onehot(datay, tagset)
    print('the shape of training data\'s tag:', datay.shape)
    return datax, datay, datafrom


def pitch2interval(traindata):
    tdata = []
    for row in traindata:
        newrow = list()
        newrow.append([row[0][0]])
        for num in range(1, len(row)):
            newrow.append([row[num][0] - row[num - 1][0]])
        tdata.append(newrow)
    tdata = np.array(tdata)

    if tdata.shape == traindata.shape:
        print('Converting pitches to intervals finished. The shape of interval array is ', tdata.shape)

    return tdata


if __name__ == '__main__':
    checkdata(filepath, filenotenum)
    datax, datay, tags = getdata(filepath)
    datax, datay, datafrom = datacut('TrainSet/39midi/', filenotenum, tags)
    datax = pitch2interval(datax)
