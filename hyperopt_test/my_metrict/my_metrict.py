import numpy as np
from keras.callbacks import Callback
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from keras import backend as K

def precision(y_true, y_pred):
    '''
    K.clip(y_true * y_pred, 0, 1)将小于0的变0,大于1 的变1
    K.round四舍五入
    K.epsilon()一个极小的数，防止除0

    :param y_true:
    :param y_pred:
    :return:
    '''
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def recall(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def fbeta_score(y_true, y_pred, beta=1):
    if beta < 0:
        raise ValueError('The lowest choosable beta is zero (only precision).')

    # If there are no true positives, fix the F score at 0 like sklearn.
    if K.sum(K.round(K.clip(y_true, 0, 1))) == 0:
        return 0

    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    bb = beta ** 2
    fbeta_score = (1 + bb) * (p * r) / (bb * p + r + K.epsilon())
    return fbeta_score

'''
precision2\recall2\fbeta_score2 is design for binary classification ,and its final is 
activation by 'softmax',the input y_true and y_pred's shape is like (?,2)
'''
def precision2(y_true, y_pred):
    '''
    K.clip(y_true * y_pred, 0, 1)将小于0的变0,大于1 的变1
    K.round四舍五入
    K.epsilon()一个极小的数，防止除0

    :param y_true:
    :param y_pred:
    :return:
    '''
    y_true=K.argmax(y_true,axis=1)
    y_pred=K.argmax(y_pred,axis=1)
    true_positives = K.sum(y_true * y_pred)
    predicted_positives = K.sum(y_pred)
    precision = K.cast(true_positives,'float32') / (K.cast(predicted_positives,'float32') + K.epsilon())
    return precision

def recall2(y_true, y_pred):
    y_true = K.argmax(y_true, axis=1)
    y_pred = K.argmax(y_pred, axis=1)
    true_positives = K.sum(y_true * y_pred)
    possible_positives = K.sum(y_true)
    recall = K.cast(true_positives,'float32') / (K.cast(possible_positives,'float32') + K.epsilon())
    return recall

def fbeta_score2(y_true, y_pred, beta=1):
    if beta < 0:
        raise ValueError('The lowest choosable beta is zero (only precision).')

    # If there are no true positives, fix the F score at 0 like sklearn.
    if K.sum(K.argmax(y_true, axis=1)) == 0:
        return 0

    p = precision2(y_true, y_pred)
    r = recall2(y_true, y_pred)
    bb = beta ** 2
    fbeta_score = (1 + bb) * (p * r) / (bb * p + r + K.epsilon())
    return fbeta_score

# def f1(y_true, y_pred):
#     def recall(y_true, y_pred):
#         """Recall metric.
#
#         Only computes a batch-wise average of recall.
#
#         Computes the recall, a metric for multi-label classification of
#         how many relevant items are selected.
#         """
#         true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
#         possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
#         recall = true_positives / (possible_positives + K.epsilon())
#         return recall
#
#     def precision(y_true, y_pred):
#         """Precision metric.
#
#         Only computes a batch-wise average of precision.
#
#         Computes the precision, a metric for multi-label classification of
#         how many selected items are relevant.
#         """
#         true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
#         predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
#         precision = true_positives / (predicted_positives + K.epsilon())
#         return precision
#     precision = precision(y_true, y_pred)
#     recall = recall(y_true, y_pred)
#     return 2*((precision*recall)/(precision+recall))
#
# class Metrics(Callback):
#     def on_train_begin(self, logs={}):
#         self.val_f1s = []
#         self.val_recalls = []
#         self.val_precisions = []
#
#
#     def on_epoch_end(self, epoch, logs={}):
#         val_predict = (np.asarray(self.model.predict(self.model.validation_data[0]))).round()
#         val_targ = self.model.validation_data[1]
#         _val_f1 = f1_score(val_targ, val_predict)
#         _val_recall = recall_score(val_targ, val_predict)
#         _val_precision = precision_score(val_targ, val_predict)
#         self.val_f1s.append(_val_f1)
#         self.val_recalls.append(_val_recall)
#         self.val_precisions.append(_val_precision)
#         print (' — val_f1: % f — val_precision: % f — val_recall % f' % (_val_f1, _val_precision, _val_recall))
#         return


#metrics = Metrics()
#on_train_begin is initialized at the beginning of the training.Here we initiate 3 lists to hold the values
# of the interested quantities, which are computed in on_epoch_end.Later on, we can access these lists as usual instance variables,
# for example:

#print(metrics.val_f1s)