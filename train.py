import package.DatasetPreparation as DatasetPreparation
import tensorflow.keras as keras
from tensorflow.keras.callbacks import TensorBoard
import tensorflow
import numpy as np
import os
import random
import warnings
import argparse

warnings.filterwarnings("ignore")
tensorflow.compat.v1.disable_eager_execution()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

filepath = 'TrainSet/equilong15/'
filenotenum = 15

modelsubdic = 'equilong15_categorial_crossentropy_adam_interval/'
modelname = 'equilong_categorical_crossentropy_adam_interval.h5'

EPOCHS = 100
n_fold = 8
batchsize = 32

def data_n_fold(x, y, foldnum, n):
    l = len(x)
    trainX = np.concatenate((x[0:int(l / foldnum * n)], x[int(l / foldnum * (n + 1)):]))
    trainY = np.concatenate((y[0:int(l / foldnum * n)], y[int(l / foldnum * (n + 1)):]))
    validX = x[int(l / foldnum * n):int(l / foldnum * (n + 1))]
    validY = y[int(l / foldnum * n):int(l / foldnum * (n + 1))]
    trainX = trainX[0:int(trainX.shape[0] / batchsize) * batchsize]
    trainY = trainY[0:int(trainY.shape[0] / batchsize) * batchsize]
    validX = validX[0:int(validX.shape[0] / batchsize) * batchsize]
    validY = validY[0:int(validY.shape[0] / batchsize) * batchsize]
    return trainX, trainY, validX, validY


def datacutrandom(x, y, foldnum):
    dx = []
    dy = []
    vx = []
    vy = []
    l = len(x)
    prop = 1 / foldnum
    for i in range(l):
        if random.random() > prop:
            dx.append(x[i])
            dy.append(y[i])
        else:
            vx.append(x[i])
            vy.append(y[i])
    dx = np.array(dx)
    dy = np.array(dy)
    vx = np.array(vx)
    vy = np.array(vy)
    dx = dx[0:int(dx.shape[0] / batchsize) * batchsize]
    dy = dy[0:int(dy.shape[0] / batchsize) * batchsize]
    vx = vx[0:int(vx.shape[0] / batchsize) * batchsize]
    vy = vy[0:int(vy.shape[0] / batchsize) * batchsize]
    return dx, dy, vx, vy


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='train')
    parser.add_argument('--input_path', default=filepath, type=str, help='training set path')
    parser.add_argument('--output_path', default=modelsubdic, type=str, help='model saving path')
    parser.add_argument('--model_name', default=modelname, type=str, help='model name')
    parser.add_argument('--note_num', default=filenotenum, type=int, help='the length for cutting songs')
    parser.add_argument('--epoch', default=EPOCHS, type=int, help='training epochs')
    parser.add_argument('--n_fold', default=n_fold, type=int, help='n fold')
    parser.add_argument('--batch_size', default=batchsize, type=int, help='batch size')
    args = parser.parse_args()

    # get training dataset
    print('\033[1;35m getting data-----------------------------------------------\033[0m')
    DatasetPreparation.checkdata(args.input_path, args.note_num)
    datax, datay, tags = DatasetPreparation.getdata(args.input_path)
    datax = DatasetPreparation.pitch2interval(datax)

    # build model
    print('\033[1;35m training---------------------------------------------------\033[0m')
    model = keras.models.Sequential(name='LSTM')
    model.add(keras.layers.Bidirectional(keras.layers.LSTM(128, stateful=True, use_bias=True, return_sequences=True),
                                        merge_mode='concat',
                                        batch_input_shape=(batchsize, datax.shape[1], datax.shape[2])))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.LSTM(256, stateful=True, use_bias=True, return_sequences=True))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(units=datay.shape[2], activation='softmax'))
    model.summary()
    model.compile(loss=keras.losses.categorical_crossentropy, optimizer='adam', metrics=['categorical_accuracy'])
    trainX, trainY, validX, validY = datacutrandom(datax, datay, n_fold)
    model.fit(trainX, trainY, epochs=args.epoch, shuffle=False, verbose=1, validation_data=(validX, validY),
            batch_size=args.batch_size, callbacks=[TensorBoard(log_dir='./log_dir/' + modelsubdic)])

    isExists = os.path.exists('model/' + args.output_path)
    if not isExists:
        os.makedirs('model/' + args.output_path)
    model.save('model/' + args.output_path + args.model_name)