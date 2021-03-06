# from __future__ import print_function

import os, sys
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Dense, Dropout, Input, Flatten, Lambda, Reshape, Bidirectional, LSTM
from keras.layers import Conv1D, Conv2D, MaxPooling2D, Embedding, Activation, Permute, MaxPooling1D
from keras.models import Model
from keras.layers.merge import concatenate, dot
# from keras import backend as K
from sklearn import metrics
import tensorflow as tf
from keras.optimizers import SGD, Adadelta
from keras.utils import plot_model
from keras import regularizers
from keras.callbacks import EarlyStopping, ModelCheckpoint
# from new_models.Match import *
# from new_models.MatchTensor import *
from my_metrict.my_metrict import precision2, recall2, fbeta_score2

BASE_DIR = '/home/wshong/my_first_keras_programe/'
glove_dir = BASE_DIR + 'glove.6B/'
text_data_dir = BASE_DIR + 'data/msr_paraphrase_'
max_sequence_length = 35
max_nb_words = 20000
embedding_dim = 50


# validation_split=0.2

def index_word_vectors():
    print('indexing word vectors.')

    embeddings_index = {}
    f = open(os.path.join(glove_dir, 'glove.6B.50d.txt'))
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()

    print('found %s word vectors.' % len(embeddings_index))
    return embeddings_index


def processing_text_dataset(str):
    print('processing text dataset')
    reader = open(text_data_dir + str + '.txt', 'r')
    unprocessed_data = np.array([example.split("\t") for example in reader.readlines()])[1:]
    reader.close()
    # 标签label值
    new_example = []
    # 句子1
    raw_sentence_1 = []
    # 句子2
    raw_sentence_2 = []
    for (i, example) in enumerate(unprocessed_data):
        new_example.append(float(example[0]))
        raw_sentence_1.append(example[3])
        raw_sentence_2.append(example[4])
    print('found %s sentences.' % len(raw_sentence_1) * 2)
    return new_example, raw_sentence_1, raw_sentence_2


def to_tensor(texts11, texts12, labels1, texts21, texts22, labels2):
    tokenizer = Tokenizer(num_words=max_nb_words)
    tokenizer.fit_on_texts(texts11 + texts12 + texts21 + texts22)
    sequences11 = tokenizer.texts_to_sequences(texts11)
    # tokenizer.fit_on_texts(texts2)
    sequences12 = tokenizer.texts_to_sequences(texts12)
    sequences21 = tokenizer.texts_to_sequences(texts21)
    # tokenizer.fit_on_texts(texts2)
    sequences22 = tokenizer.texts_to_sequences(texts22)
    word_index = tokenizer.word_index
    print('found %s unique tokens.' % len(word_index))
    # text11的张量
    data11 = pad_sequences(sequences11, max_sequence_length)
    # text12的张量
    data12 = pad_sequences(sequences12, max_sequence_length)
    data21 = pad_sequences(sequences21, max_sequence_length)
    # text22的张量
    data22 = pad_sequences(sequences22, max_sequence_length)
    labels1 = to_categorical(np.asarray(labels1))
    labels2 = to_categorical(np.asarray(labels2))
    # labels1 = np.asarray(labels1)
    # labels2 = np.asarray(labels2)
    print('shape of the data11 tensor:', data11.shape)
    print('shape of the data12 tensor:', data12.shape)
    print('shape of label1 tensor:', labels1.shape)
    print('shape of the data21 tensor:', data21.shape)
    print('shape of the data22 tensor:', data22.shape)
    print('shape of label2 tensor:', labels2.shape)
    return word_index, data11, data12, labels1, data21, data22, labels2


def prepare_embedding(word_index, embeddings_index):
    print('preparing embedding matrix.')
    num_words = len(word_index)
    embedding_matrix = np.zeros((num_words + 1, embedding_dim))
    for word, i in word_index.items():
        if (i >= len(word_index)):
            continue
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector
    return num_words + 1, embedding_matrix


# def share_model():
#     x1=Input(shape=(35,50),dtype='float32')
#     x2=Dense(50,activation='relu')(x1)
#     a=Match(match_type='dot')([x1,x2])
#     a=Reshape((35,35))(a)
#     #attention=Dense(35,activation='softmax',use_bias=False)(a)
#     attention = Activation(activation='softmax')(a)
#     attention=Permute((2,1))(attention)
#     attention = dot([attention,x1],axes=1)
#     #attention=MatchTensor(channel=8)([attention,x1])
#     model = Model(x1,attention,name='self_attention_model')
#     model.summary()
#     return model

def train(args):
    global num_words, embedding_matrix, x1_train, x2_train, y_train, x1_val, x2_val, y_val, num
    # weight加入glove预先训练好的向量，trainable设置成这部分参数不训练（glove预先训练好了，也可以添加自己的向量）
    embedding_layer = Embedding(num_words, embedding_dim, weights=[embedding_matrix], input_length=max_sequence_length,
                                trainable=False)
    num += 1
    print('training model.', (num))

    sequence_input = Input(shape=(max_sequence_length,), dtype='int32')
    embedded_sequences = embedding_layer(sequence_input)
    # sequence_input1 = Input(shape=(max_sequence_length,), dtype='int32')
    # sequence_input2 = Input(shape=(max_sequence_length,), dtype='int32')
    # embedded_sequences1=embedding_layer(sequence_input1)
    # embedded_sequences2=embedding_layer(sequence_input2)

    lstmf = LSTM(50, go_backwards=True, return_sequences=True, dropout=0.3)(embedded_sequences)
    lstmb = LSTM(50, return_sequences=True, dropout=0.3)(embedded_sequences)
    embedded_sequences = Reshape((max_sequence_length, embedding_dim, 1))(embedded_sequences)
    lstmf = Reshape((max_sequence_length, embedding_dim, 1))(lstmf)
    lstmb = Reshape((max_sequence_length, embedding_dim, 1))(lstmb)

    x = concatenate([embedded_sequences, lstmf, lstmb], axis=3)
    x = Conv2D(args['num'], (2, 2), activation='relu')(x)
    # x = Reshape((4, 4, 300))(x)
    x = MaxPooling2D((2, 2), strides=2, padding='same')(x)
    # x = Reshape((17, 2, 300))(x)
    x = Conv2D(args['num'], (2, 2), activation='relu')(x)
    # x = Reshape((4, 4, 300))(x)
    x = MaxPooling2D((2, 2), strides=2, padding='same')(x)
    x = Conv2D(args['num'], (2, 2), activation='relu')(x)
    x = Flatten()(x)
    mo = Model(sequence_input, x)

    sequence_input1 = Input(shape=(max_sequence_length,), dtype='int32')
    sequence_input2 = Input(shape=(max_sequence_length,), dtype='int32')
    # embedded_sequences1=embedding_layer(sequence_input1)
    # embedded_sequences2=embedding_layer(sequence_input2)
    out1 = mo(sequence_input1)
    out2 = mo(sequence_input2)
    #
    # output1=shall_model(sequence_input1)
    # output2=shall_model(sequence_input2)
    #
    x = concatenate([out1, out2])
    # x = Dense(128,activation='relu')(x)
    # x = Dropout(0.5)(x)
    # x = Dense(4, activation='relu')(x)
    x = Dropout(0.5)(x)
    preds = Dense(2, activation='softmax')(x)
    # preds=Lambda(out)(preds)
    # preds=Lambda(lambda i:1.0 if(i[0]>=0.5) else 0.0)(preds)
    # preds = Lambda(K.argmax,output_shape=(1,),dtype='float64')(preds)
    model = Model([sequence_input1, sequence_input2], preds)

    # model.summary()
    # model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['acc'])
    sgd = SGD(lr=args['eta'], decay=1e-6)
    # ada=Adadelta(lr=args['eta'])
    model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=[precision2, recall2, fbeta_score2])

    # saveBestModel = ModelCheckpoint('sa_hyper_best.h5', monitor='val_precision2', verbose=2, save_best_only=True, mode='max')
    earlystopping = EarlyStopping(monitor='val_loss', min_delta=0.0001, patience=5)
    model.fit([x1_train, x2_train], y_train, batch_size=128, epochs=100, verbose=0, callbacks=[earlystopping],
              validation_data=([x1_val, x2_val], y_val))
    # plot_model(shall_model, to_file='model_1.png', show_shapes=True)
    # plot_model(model,to_file='sa_hyper.png',show_shapes=True)

    yp = model.predict([x1_val, x2_val], batch_size=128, verbose=2)
    ypreds = np.argmax(yp, axis=1)
    y_val_metrics = np.argmax(y_val, axis=1)
    print('\n', metrics.classification_report(y_val_metrics, ypreds, digits=4))
    # model.save('sa_hyper.h5')
    precision = metrics.precision_score(y_val_metrics, ypreds)
    print('eta:', args['eta'], '  num:', args['num'], ' precision@1:', precision)
    return -precision


if __name__ == '__main__':
    num = 0
    embeddings_index = index_word_vectors()
    # texts,labels,labels_index=processing_text_dataset()
    train_label, x1text_train, x2text_train = processing_text_dataset('train')
    test_label, x1text_test, x2text_test = processing_text_dataset('test')
    word_index, x1_train, x2_train, y_train, x1_val, x2_val, y_val = to_tensor(x1text_train, x2text_train, train_label,
                                                                               x1text_test, x2text_test, test_label)
    num_words, embedding_matrix = prepare_embedding(word_index, embeddings_index)
    # train(args={'num':300})

    from hyperopt import fmin, tpe, hp, partial

    space = {"num": hp.choice("num", range(1, 100)),
             "eta": hp.uniform("eta", 0.005, 0.05)}
    algo = partial(tpe.suggest, n_startup_jobs=10)
    best = fmin(train, space, algo=algo, max_evals=100)
    print('best:', best)
    print('p', train(best))
