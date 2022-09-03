from tensorflow.keras.utils import plot_model
import tensorflow.keras as keras
import warnings
import argparse

warnings.filterwarnings("ignore")

path = '/Users/apple/Desktop/深度学习有关/2022寒假/lstm/model/equilong_categorical_crossentropy_adam_interval/equilong_categorical_crossentropy_adam_interval.h5'


def modelplot(path):
    model = keras.models.load_model(path)
    plot_model(model=model, to_file=path.split('.')[0] + '.png', show_shapes=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='plot_model')
    parser.add_argument('--path', default=path, type=str, help='model path')
    modelplot(path)
