import package.DatasetPreparation as DatasetPreparation
import tensorflow.keras as keras
from tensorflow.keras.callbacks import TensorBoard
import tensorflow
import package.compose as compose
import numpy as np
import os
import warnings

warnings.filterwarnings("ignore")
tensorflow.compat.v1.disable_eager_execution()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

modelpath = '/Users/apple/Desktop/深度学习有关/2022寒假/lstm/model/equilong15_categorial_crossentropy_adam_interval/equilong_categorical_crossentropy_adam_interval.h5'
filepath = 'TrainSet/39midi/'
filenotenum = 15
batchsize = 32

tagpath = 'TrainSet/tag.npy'
tags = np.load(tagpath)
tags = list(tags)

datax, datay, datafrom = DatasetPreparation.datacut(filepath, filenotenum, tags)
datax = datax[0:int(len(datax)/batchsize)*batchsize]
datay = datay[0:int(len(datax)/batchsize)*batchsize]
datafrom = datafrom[0:int(len(datax)/batchsize)*batchsize]
datax_interval = DatasetPreparation.pitch2interval(datax)

model = keras.models.load_model(modelpath)

print('Evaluate with ' + filepath + ' -------------------------------')
score = model.evaluate(datax_interval, datay)
print('Bi-LSTM: trainloss:%f, trainacc:%f' % (score[0], score[1]))

print('Compose start' + '-------------------------------------------------')
y = model.predict(datax_interval, batch_size=batchsize)
y = compose.onehot2tag(y, tags)
compose.compose39midi(datax, y, datafrom, filenotenum)


