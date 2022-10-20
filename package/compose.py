import sys
import pretty_midi
import numpy as np
import os
from collections import Counter


def onehot2tag(DataY, tagset):
    DataYtag = []

    tagset = list(tagset)
    tagsetlength = len(tagset)
    tagset.sort()

    timetag = []

    DataY = DataY.tolist()
    for i in range(len(DataY)):
        for j in range(len(DataY[i])):
            y = tagset[DataY[i][j].index(max(DataY[i][j]))]
            timetag.append([y])
        DataYtag.append(timetag)
        timetag = []
    DataYtag = np.array(DataYtag)

    return DataYtag


def compose39midi(pitches, time, datafrom, fnn):
    if len(pitches) != len(time) or len(pitches) != len(datafrom) or len(time) != len(datafrom) or pitches.shape[1] != \
            time.shape[1]:
        print('Pitchset has different shape with timeset. Program terminated.')
        sys.exit()

    lastsong = datafrom[0]
    lastend = 0
    cello_c_chord = pretty_midi.PrettyMIDI()
    cello_program = pretty_midi.instrument_name_to_program('Cello')
    cello = pretty_midi.Instrument(program=cello_program)
    for i in range(len(datafrom)):
        if datafrom[i] != lastsong:
            cello_c_chord.instruments.append(cello)
            cello_c_chord.write('Composed/equilong' + str(fnn) + '_39midi_recover/' + lastsong)
            lastsong = datafrom[i]
            lastend = 0
            cello_c_chord = pretty_midi.PrettyMIDI()
            cello_program = pretty_midi.instrument_name_to_program('Cello')
            cello = pretty_midi.Instrument(program=cello_program)

        for j in range(fnn):
            note = pretty_midi.Note(velocity=100, pitch=pitches[i][j][0], start=lastend, end=lastend + time[i][j][0])
            cello.notes.append(note)
            lastend = lastend + time[i][j][0]

    print('Compose finished.')


# 输入：fp为音高数据路径，fnn为音高数据切割长度
# 输出：pitchset为切割后的音高数据，pitchesfrom为对应的音高数据来源
# 特点：假设一份音高文件中有100个音高数据，根据fnn=10进行切割，可以切出一份(10,10)的音高数据和一份(10,1)的音高数据来源。
def cutpitches(fp, fnn):
    pitchset = []
    pitchesfrom = []
    for filename in os.listdir(fp):
        pitches = []
        if filename != '.DS_Store':
            with open(fp + '/' + filename) as f:
                for line in f.readlines():
                    line = line.strip('\n')
                    if line != '.':
                        if len(pitches) != fnn:
                            pitches.append([int(line)])
                        else:
                            pitchset.append(pitches)
                            pitchesfrom.append(filename)
                            pitches = []
                            pitches.append([int(line)])
    pitchset = np.array(pitchset)
    print('the shape of pitchset:', pitchset.shape)
    return pitchset, pitchesfrom


# 输入：fp为音高数据路径，fnn为音高数据切割长度
# 输出：pitchset为切割后的音高数据，pitchesfrom为对应的音高数据来源
# 特点：假设一份音高文件中有100个音高数据，根据fnn=10进行切割，可以切出一份(91,10)的音高数据和一份(91,1)的音高数据来源。
#      与上一个函数不同，每个音高都可以作为一个音高数据的起始音高。
def cutpitches_pitchesrepeated(fp, fnn):
    allpitches = []
    allpause = []
    for filename in os.listdir(fp):
        pitches = []
        pause = []
        cnt = 0
        if filename != '.DS_Store':
            with open(fp + '/' + filename) as f:
                for line in f.readlines():
                    line = line.strip('\n')
                    if line != '.':
                        pitches.append(int(line))
                        cnt += 1
                    else:
                        pause.append(cnt)
            allpitches.append((pitches, filename))
            allpause.append(pause)
    pitchset = []
    pitchesfrom = []
    for ps, f in allpitches:
        for i in range(len(ps) - fnn + 1):
            pitches = np.array(ps[i:i + 15])
            pitches = np.reshape(pitches, (15, 1))
            pitchset.append(pitches)
            pitchesfrom.append(f)
    pitchset = np.array(pitchset)
    print('the shape of pitchset:', pitchset.shape)
    return pitchset, pitchesfrom, allpause


# 输入：pitches为音高数据，time为时长数据，datafrom为数据来源，fnn为音高数据切割长度
# 输出：无
# 特点：根据音高数据和时长数据构造音乐。
def compose_newmusic(pitches, time, datafrom, fnn):
    if len(pitches) != len(time) or len(pitches) != len(datafrom) or len(time) != len(datafrom) or pitches.shape[1] != \
            time.shape[1]:
        print('Pitchset has different shape with timeset. Program terminated.')
        sys.exit()

    lastsong = datafrom[0]
    lastend = 0
    cello_c_chord = pretty_midi.PrettyMIDI()
    cello_program = pretty_midi.instrument_name_to_program('Flute')
    cello = pretty_midi.Instrument(program=cello_program)
    for i in range(len(datafrom)):
        if datafrom[i] != lastsong:
            cello_c_chord.instruments.append(cello)
            cello_c_chord.write('Composed/pitch/' + lastsong.split('.')[0] + '.mid')
            lastsong = datafrom[i]
            lastend = 0
            cello_c_chord = pretty_midi.PrettyMIDI()
            cello_program = pretty_midi.instrument_name_to_program('Flute')
            cello = pretty_midi.Instrument(program=cello_program)

        for j in range(fnn):
            note = pretty_midi.Note(velocity=100, pitch=pitches[i][j][0], start=lastend, end=lastend + time[i][j][0])
            cello.notes.append(note)
            lastend = lastend + time[i][j][0]

    print('Compose finished.')


# 输入：pitches为音高数据，time为时长数据，datafrom为数据来源，fnn为音高数据切割长度
# 输出：无
# 特点：根据音高数据和时长数据构造音乐。
def compose_newmusic_pitchesrepeated(pitches, time, datafrom, fnn, outputpath, allpause):
    if len(pitches) != len(time) or len(pitches) != len(datafrom) or len(time) != len(datafrom) or pitches.shape[1] != \
            time.shape[1]:
        print('Pitchset has different shape with timeset. Program terminated.')
        sys.exit()

    dfrange = [0]
    for i in range(1, len(datafrom)):
        if datafrom[i] != datafrom[i - 1]:
            dfrange.append(i)
    dfrange.append(len(datafrom))

    pset = []
    tset = []
    for i in range(len(dfrange) - 1):
        pitches_one_song = pitches[dfrange[i]:dfrange[i + 1]]
        time_one_song = time[dfrange[i]:dfrange[i + 1]]
        newpitches = []
        newtime = []
        for j in range(len(pitches_one_song)):
            newpitches.append(pitches_one_song[j][0][0])
            curr_time = []
            if j < fnn:
                for k in range(j, -1, -1):
                    curr_time.append(time_one_song[k][j - k][0])
            else:
                for k in range(j, j - fnn, -1):
                    curr_time.append(time_one_song[k][j - k][0])
            newtime.append(curr_time)
        for j in range(1, fnn):
            newpitches.append(pitches_one_song[-1][j][0])
            curr_time = []
            pos = -1
            for k in range(j, fnn):
                curr_time.append(time_one_song[pos][k][0])
                pos -= 1
            newtime.append(curr_time)
        pset.append(newpitches)
        tset.append(newtime)

    for song in tset:
        for i in range(len(song)):
            res = Counter(song[i])
            song[i] = res.most_common(1)[0][0]

    if len(pset) != len(allpause):
        print('\033[1;31m Pitch set has different length with pause set.\033[0m')

    for i in range(len(pset)):
        lastend = 0
        bartime_start = lastend
        cello_c_chord = pretty_midi.PrettyMIDI()
        cello_program = pretty_midi.instrument_name_to_program('Flute')
        cello = pretty_midi.Instrument(program=cello_program)
        for j in range(len(pset[i])):
            note = pretty_midi.Note(velocity=100, pitch=pset[i][j], start=lastend, end=lastend + tset[i][j])
            cello.notes.append(note)
            lastend = lastend + tset[i][j]
            '''if (j+1) in allpause[i]:
                bartime_end = lastend
                bartime_rest = 1.2 * (int((bartime_end - bartime_start) / 1.2) + 1) - (bartime_end - bartime_start)
                lastend = lastend + bartime_rest
                bartime_start = lastend'''
        cello_c_chord.instruments.append(cello)
        print('Composing ' + datafrom[dfrange[i]].split('.')[0] + '.mid')
        cello_c_chord.write(outputpath + datafrom[dfrange[i]].split('.')[0] + '.mid')

    print('Compose finished.')


if __name__ == '__main__':
    cutpitches('pitches/old_pitches', 15)
    cutpitches_pitchesrepeated('pitches/old_pitches', 15)
