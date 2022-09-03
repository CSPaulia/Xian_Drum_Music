# WElCOME USING XIAN_DRUM_MUSIC

This project is based on LSTMs to help the ancient music of Xi'an Drum, where the notes just have pitches without time, to repair the time.

## Data preparation

In this project, U'd better to handle with the Dataset. Supposing there is a music, we name it as $D$. $D$ is composed by lots of notes. we can name a note as $d$, and the nth note will be named as $d_n$. So we can represent $D$ as $$D = \{d_1, d_2, \cdots, d_n\}$$ In order to input the data with the same length to the LSTM model, we have to cut $D$. Besides, in order to study the relationship between note and note as more as possible, we will cut it repeatitively. Suppose $P$ is a dataset, and $P_i$ is the ith data in the dataset. $P_i$ can represent as $$P_1 = [d_1, d_2, \cdots, d_k] $$ $$ P_2 = [d_2, d_3, \cdots, d_{k+1}] $$ $$ \cdots $$ $$ P_{n-k+1} = [d_{n-k+1}, d_{n-k+2}, \cdots, d_n] $$ $P$ can represents as $$ P = \{P_1, P_2, \cdots, P_{n-k+1}\}$$

The dataset structure should be like
> Trainset
> > Song 1($P$)
> > > Cut 1($P_1$)
Cut 2($P_2$)
$\cdots$
Cut n-k+1($P_{n-k+1}$)

## Environment preparation



## Train model

U can run the `train.py` in terminal
```
python train.py
```
U can change the parameter of the model through the command line, like this
```
python train.py --epoch 1000
```

## Plot model

U can run the `plot_models.py` in terminal
```
python plot_models.py
```
U have to appoint the model path and the graphic of model construction will be saved in the same dir with the model.

## Make music

Before we make music, we have to supply the pitch data first. U can pick up all of pitches from a song as the pitch data and save them into a txt file.
Then U can run the `makemusic.py` in terminal
```
python makemusic.py
```


