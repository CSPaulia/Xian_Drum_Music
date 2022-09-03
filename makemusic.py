import imp
from logging import warning
import package.DatasetPreparation as DatasetPreparation
import tensorflow.keras as keras
from tensorflow.keras.callbacks import TensorBoard
import tensorflow
import package.compose as compose
import numpy as np
import os
import argparse
import warnings

warnings.filterwarnings("ignore")
tensorflow.compat.v1.disable_eager_execution()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

modelpath = 'model/equilong15_categorial_crossentropy_adam_interval/model.h5'
pitchespath = 'pitches/old_pitches'
outputpath = 'Composed/'
filenotenum = 15
b = 32

tagpath = 'TrainSet/tag.npy'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='train')
    parser.add_argument('--input_path', default=pitchespath, type=str, help='testing set path')
    parser.add_argument('--model_path', default=modelpath, type=str, help='model path')
    parser.add_argument('--output_path', default=outputpath, type=str, help='output path')
    parser.add_argument('--note_num', default=filenotenum, type=int, help='the length for cutting songs')
    parser.add_argument('--tag_path', default=tagpath, type=str, help='tag path')
    parser.add_argument('--batch_size', default=b, type=int, help='batch size')
    args = parser.parse_args()

    tags = np.load(args.tag_path)
    tags = list(tags)

    pitchset, pitchesfrom = compose.cutpitches_pitchesrepeated(args.input_path, args.note_num)
    batchsize = args.batch_size
    pitchset = pitchset[0:int(len(pitchset)/batchsize)*batchsize]
    pitchesfrom = pitchesfrom[0:int(len(pitchesfrom)/batchsize)*batchsize]
    pitchset_interval = DatasetPreparation.pitch2interval(pitchset)

    model = keras.models.load_model(args.model_path)

    print('\033[1;35m Compose start-------------------------------------------------\033[0m')
    y = model.predict(pitchset_interval, batch_size=batchsize)
    y = compose.onehot2tag(y, tags)
    compose.compose_newmusic_pitchesrepeated(pitchset, y, pitchesfrom, args.note_num, outputpath)