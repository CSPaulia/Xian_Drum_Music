import package.DatasetPreparation as DatasetPreparation
import tensorflow.keras as keras
from tensorflow.keras.callbacks import TensorBoard
import tensorflow
import package.compose as compose
import numpy as np
import os
import warnings
import pretty_midi
from sklearn.metrics import confusion_matrix, accuracy_score
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
tensorflow.compat.v1.disable_eager_execution()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

modelpath = 'model/equilong30_categorial_crossentropy_adam_interval的副本/equilong_categorical_crossentropy_adam_interval.h5'
filepath = 'TrainSet/test/'
filenotenum = 30
batchsize = 32

tagpath = 'TrainSet/tags/TrainSet_equilong30_tag.npy'
tags = np.load(tagpath)
tags = list(tags)
# print(tags)

outputpath = 'Composed/test/'

def MyEval(origin_music, new_music):
    midi_origin = pretty_midi.PrettyMIDI(origin_music)
    notes_origin = midi_origin.instruments[0].notes

    midi_new = pretty_midi.PrettyMIDI(new_music)
    notes_new = midi_new.instruments[0].notes

    dur_origin = []
    dur_new = []
    successive_cnt = 0
    for i in range(len(notes_new)):
        dur_origin.append(round(notes_origin[i].duration, 2))
        dur_new.append(round(notes_new[i].duration, 2))
        if notes_new[i].pitch == notes_origin[i].pitch:
            successive_cnt += 1
        else:
            break
    
    print('The Amount of the pitches in (' + new_music + ') is ' + str(len(notes_new)) + '.', 'And the have ' + str(successive_cnt) + ' same successive pitches with (' + origin_music + ').')

    if successive_cnt > 0.5 * len(notes_new):
        return dur_origin, dur_new
    else:
        return [], []


def tag2index(arr, tags):
    newarr = []
    for time in arr:
        newarr.append(tags.index(time))
    return newarr

if __name__ == '__main__':
    datax, datay, datafrom = DatasetPreparation.datacut(filepath, filenotenum, tags)
    datax = datax[0:int(len(datax)/batchsize)*batchsize]
    datay = datay[0:int(len(datax)/batchsize)*batchsize]
    datafrom = datafrom[0:int(len(datax)/batchsize)*batchsize]
    datax_interval = DatasetPreparation.pitch2interval(datax)

    model = keras.models.load_model(modelpath)

    print('\033[1;35m Evaluate with (' + filepath + ') -------------------------------\033[0m')
    score = model.evaluate(datax_interval, datay)
    print('Bi-LSTM: testloss:%f, testacc:%f' % (score[0], score[1]))

    print('\033[1;35m Compose start' + '-------------------------------------------------\033[0m')
    y = model.predict(datax_interval, batch_size=batchsize)
    y = compose.onehot2tag(y, tags)
    compose.compose_newmusic_pitchesrepeated(datax, y, datafrom, filenotenum, outputpath)

    print('\033[1;35m Evaluate with self design function -----------------------------\033[0m')
    dur_origin = []
    dur_new = []
    for song in os.listdir(filepath):
        if song.split('.')[-1] == 'mid':
            dur_origin_one_song, dur_new_one_song = MyEval(filepath + song, outputpath + song)
            dur_origin = dur_origin + dur_origin_one_song
            dur_new = dur_new +dur_new_one_song

    tagset_new = list(set(dur_origin + dur_new))
    dur_origin = tag2index(dur_origin, tagset_new)
    dur_new = tag2index(dur_new, tagset_new)

    acc = accuracy_score(dur_origin, dur_new)
    print('Accuracy indeed:', acc)
    cm = confusion_matrix(dur_origin, dur_new)
    plt.matshow(cm, cmap=plt.cm.Blues)
    for i in range(len(cm)):
        for j in range(len(cm)):
            if cm[j, i] > 0:
                plt.annotate(cm[j, i], xy=(i, j), horizontalalignment='center', verticalalignment='center')
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    # plt.ylabel('True label', fontdict={'family': 'Times New Roman', 'size': 20})
    # plt.xlabel('Predicted label', fontdict={'family': 'Times New Roman', 'size': 20})
    plt.xticks(range(0, len(tagset_new)), labels=tagset_new) # 将x轴或y轴坐标，刻度 替换为文字/字符
    plt.yticks(range(0, len(tagset_new)), labels=tagset_new)
    plt.show()


