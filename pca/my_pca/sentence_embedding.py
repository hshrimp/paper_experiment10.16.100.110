#!/usr/bin/python3

#
#  Copyright 2016 Peter de Vocht
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import numpy as np
from sklearn.decomposition import PCA
from typing import List


# an embedding word with associated vector
class Word:
    def __init__(self, text, vector):
        self.text = text
        self.vector = vector


# a sentence, a list of words
class Sentence:
    def __init__(self, word_list):
        self.word_list = word_list

    # return the length of a sentence
    def len(self) -> int:
        return len(self.word_list)


# todo: get the frequency for a word in a document set
def get_word_frequency(word_text):
    return 1.0


# A SIMPLE BUT TOUGH TO BEAT BASELINE FOR SENTENCE EMBEDDINGS
# Sanjeev Arora, Yingyu Liang, Tengyu Ma
# Princeton University
# convert a list of sentence with word2vec items into a set of sentence vectors
def sentence_to_vec(sentence_list: List[Sentence], embedding_size: int, a: float = 1e-3):
    sentence_set = []
    for sentence in sentence_list:
        vs = np.zeros(embedding_size)  # add all word2vec values into one vector for the sentence
        sentence_length = sentence.len()
        for word in sentence.word_list:
            a_value = a / (a + get_word_frequency(word.text))  # smooth inverse frequency, SIF
            vs = np.add(vs, np.multiply(a_value, word.vector))  # vs += sif * word_vector

        vs = np.divide(vs, sentence_length)  # weighted average
        sentence_set.append(vs)  # add to our existing re-calculated set of sentences

    # calculate PCA of this sentence set
    pca = PCA(n_components=embedding_size)
    pca.fit(np.array(sentence_set))
    u = pca.components_[0]  # the PCA vector
    u = np.multiply(u, np.transpose(u))  # u x uT

    # pad the vector?  (occurs if we have less sentences than embeddings_size)
    if len(u) < embedding_size:
        for i in range(embedding_size - len(u)):
            u = np.append(u, 0)  # add needed extension for multiplication below

    # resulting sentence vectors, vs = vs -u x uT x vs
    sentence_vecs = []
    for vs in sentence_set:
        sub = np.multiply(u, vs)
        sentence_vecs.append(np.subtract(vs, sub))

    return sentence_vecs


#####################################################################
# test
embedding_size = 300  # dimension of the word embedding

# some random word/GloVe vectors for demo purposes of dimension 300
w1 = Word('in',
          [0.0703125, 0.0869141, 0.0878906, 0.0625, 0.0693359, -0.108887, -0.081543, -0.154297, 0.020752, 0.131836,
           -0.11377, -0.0373535, 0.0693359, 0.078125, -0.103027, -0.0976562, 0.0441895, 0.102539, -0.060791, -0.0361328,
           -0.0454102, 0.0473633, -0.120605, -0.0639648, 0.0022583, 0.0371094, -0.00291443, 0.117676, 0.0617676,
           0.0639648, 0.0810547, -0.0688477, -0.0213623, 0.0551758, -0.0854492, 0.0688477, -0.12793, -0.0332031,
           0.0986328, 0.175781, 0.11084, -0.034668, -0.0471191, -0.00848389, 0.0358887, 0.103027, 0.0269775, -0.0286865,
           -0.00512695, 0.106445, 0.0598145, 0.0942383, 0.0336914, -0.0270996, -0.0942383, 0.00102997, -0.0483398,
           0.0344238, 0.0810547, -0.113281, -0.0888672, 0.0358887, -0.145508, -0.244141, -0.0615234, 0.0529785,
           0.0568848, 0.179688, 0.0610352, 0.0869141, 0.124023, -0.0402832, 0.022583, 0.177734, -0.0296631, -0.0296631,
           0.117188, 0.0311279, -0.0961914, 0.0664062, 0.00469971, -0.0800781, 0.0629883, -0.0206299, -0.0546875,
           -0.135742, -0.0634766, 0.0834961, -0.0639648, 0.0214844, 0.0771484, -0.0371094, -0.0336914, -0.183594,
           -0.0727539, 0.0158691, 0.0932617, -0.0615234, -0.0142212, -0.00344849, 0.0111084, -0.158203, -0.0170898,
           0.00619507, -0.00872803, -0.0805664, -0.0152588, -0.0878906, 0.003479, -0.0161133, -0.0123291, 0.0976562,
           -0.139648, -0.0859375, -0.0268555, 0.0539551, 0.132812, 0.112793, 0.121094, 0.0854492, -0.0071106, 0.0446777,
           -0.145508, -0.00320435, -0.117676, -0.0654297, 0.0712891, -0.0942383, -0.0302734, 0.120117, 0.0800781,
           -0.0947266, -0.162109, -0.0776367, 0.0212402, -0.081543, 0.00393677, -0.157227, -0.0981445, 0.0397949,
           0.0393066, -0.00909424, 0.103027, 0.0678711, -0.0427246, 0.0634766, -0.0490723, 0.020874, -0.166992,
           0.0932617, 0.09375, 0.00686646, 0.0537109, 0.0524902, -0.0244141, -0.0324707, -0.0615234, -0.0055542,
           0.0961914, 0.0378418, 0.012207, -0.0439453, -0.00747681, 0.105469, 0.0203857, 0.145508, 0.0820312,
           0.00576782, 0.00457764, -0.0927734, -0.138672, -0.057373, -0.0515137, -0.130859, -0.139648, -0.0205078,
           -0.0270996, 0.0327148, 0.10498, -0.00233459, -0.022583, 0.00050354, -0.11084, 0.0849609, -0.129883,
           -0.0174561, -0.000358582, 0.10791, 0.0888672, 0.0446777, 0.0251465, 0.0238037, 0.0810547, 0.0236816,
           -0.109863, 0.00537109, -0.0177002, -0.0339355, -0.032959, -0.164062, 0.0957031, -0.0183105, 0.00531006,
           -0.0344238, -0.0441895, -0.0664062, -0.0179443, -0.0296631, -0.00759888, -0.0512695, -0.0541992, 0.0893555,
           -0.0717773, 0.0152588, -0.0825195, -0.0317383, 0.0356445, -0.0212402, -0.0593262, -0.0130615, 0.046875,
           0.0230713, 0.0209961, -0.0786133, -0.00805664, 0.0195312, -0.0055542, 0.0415039, 0.027832, 0.0136108,
           0.034668, -0.182617, 0.120117, 0.0742188, -0.0410156, -0.00994873, 0.0429688, -0.0072937, 0.123047,
           0.0576172, -0.0534668, -0.0322266, -0.00909424, -0.0466309, 0.0439453, -0.0507812, 0.0688477, 0.00299072,
           -0.00418091, -0.0441895, 0.0737305, -0.0127563, 0.0673828, 0.00628662, 0.0751953, -0.0378418, 0.00488281,
           0.0446777, -0.0673828, 0.00970459, 0.00473022, 0.0205078, 0.0712891, 0.170898, 0.173828, 0.0556641,
           0.0913086, -0.0373535, 0.0498047, -0.0393066, 0.0441895, 0.0625, 0.048584, -0.0532227, 0.0488281, -0.130859,
           -0.0289307, -0.0361328, -0.060791, -0.057373, 0.123047, -0.0825195, -0.0119019, 0.125, 0.00135803, 0.0639648,
           -0.106445, -0.143555, -0.0422363, 0.0240479, -0.168945, -0.0888672, -0.0805664, 0.0649414, 0.0612793,
           -0.0473633, -0.0588379, -0.0476074, 0.0144653, -0.0625])
w2 = Word('on',
          [0.0267334, -0.0908203, 0.027832, 0.204102, 0.00622559, -0.090332, 0.022583, -0.161133, 0.132812, 0.0610352,
           -0.0157471, 0.0883789, 0.0137939, 0.0463867, -0.0559082, -0.0668945, 0.0122681, 0.136719, 0.154297,
           -0.0461426, -0.0393066, -0.154297, -0.165039, 0.10791, 0.0332031, -0.0510254, 0.0371094, 0.101562, 0.110352,
           0.0205078, 0.0067749, 0.00118256, -0.0125122, -0.125, 0.0148315, -0.0268555, -0.0214844, 0.0150757, 0.138672,
           0.048584, -0.0766602, -0.116699, 0.106934, 0.041748, 0.0128174, -0.00946045, -0.0289307, -0.0385742,
           0.243164, 0.00952148, 0.0220947, 0.222656, 0.00915527, -0.0454102, -0.0354004, 0.140625, -0.18457, 0.0776367,
           0.0415039, -0.0849609, -0.0991211, 0.0583496, -0.0966797, -0.202148, -0.0140381, -0.00236511, 0.147461,
           0.200195, 0.0595703, 0.154297, 0.134766, 0.00527954, 0.125, 0.0854492, -0.02771, -0.0581055, 0.183594,
           0.00787354, -0.15332, 0.124023, -0.0800781, -0.143555, 0.149414, 0.0145874, 0.10791, -0.201172, -0.150391,
           0.0524902, 0.0771484, 0.0917969, -0.0380859, 0.148438, 0.0546875, -0.151367, 0.0142822, -0.10498, 0.019043,
           -0.0634766, 0.0534668, 0.0349121, 0.139648, -0.133789, 0.216797, -0.194336, -0.0583496, -0.134766, -0.265625,
           -0.104004, 0.0354004, -0.21582, 0.0825195, 0.045166, -0.0698242, -0.0432129, 0.0269775, -0.090332,
           0.00549316, 0.0498047, -0.0356445, 0.0598145, -0.149414, -0.0220947, -0.0332031, 0.175781, -0.0664062,
           -0.0183105, 0.0112915, -0.0422363, -0.0771484, 0.0174561, -0.10498, -0.104492, -0.0473633, -0.029541,
           -0.0615234, -0.0507812, -0.0256348, -0.0952148, -0.0810547, -0.101562, 0.202148, 0.118652, -0.00282288,
           -0.0603027, 0.0224609, 0.130859, 0.0805664, -0.154297, -0.0825195, 0.160156, 0.0578613, 0.0976562,
           -0.0209961, -0.045166, -0.0732422, 0.00436401, -0.0908203, 0.019165, -0.0166016, -0.050293, 0.0147095,
           -0.00415039, 0.034668, 0.057373, 0.0800781, 0.00622559, 0.0639648, 0.0245361, 0.0317383, -0.125, -0.078125,
           -0.0245361, -0.0722656, -0.0864258, -0.0771484, 0.043457, -0.000187874, -0.0114136, -0.0991211, 0.0262451,
           0.0534668, 0.0454102, -0.0712891, 0.138672, 0.0410156, 0.0111694, -0.0153198, 0.032959, 0.182617, 0.0174561,
           -0.0319824, 0.10791, 0.032959, -0.0351562, -0.217773, 0.102051, -0.0292969, -0.000946045, -0.00714111,
           -0.0263672, 0.0617676, -0.0169678, -0.0217285, -0.119141, 0.00909424, 0.103027, -0.00300598, 0.149414,
           0.105957, -0.0402832, -0.0184326, 0.0358887, -0.0380859, 0.0568848, 0.0153198, 0.0197754, 0.180664,
           0.00817871, -0.151367, 0.0322266, 0.157227, 0.0507812, -0.0289307, 0.0439453, -0.0585938, 0.00309753,
           -0.0126343, 0.161133, 0.105957, -0.0339355, 0.181641, -0.0446777, 0.0341797, -0.0378418, -0.0088501,
           -0.0368652, 0.0786133, 0.0270996, 0.0461426, 0.0688477, 0.0505371, -0.00174713, -0.136719, -0.15332,
           0.0986328, -0.161133, 0.00662231, -0.0859375, -0.0175781, 0.0407715, 0.0299072, 0.0114136, -0.0202637,
           -0.0644531, 0.0174561, -0.128906, -0.000347137, 0.0422363, 0.0032959, 0.122559, -0.0957031, 0.0922852,
           0.10498, -0.124512, 0.0358887, 0.145508, -0.105469, 0.0229492, -0.00836182, 0.00463867, 0.219727, -0.0495605,
           0.238281, -0.0583496, 0.0483398, 0.0605469, -0.0373535, -0.177734, 0.0449219, -0.0422363, 0.0825195,
           0.110352, -0.109375, 0.0942383, -0.0722656, 0.0490723, -0.158203, 0.078125, 0.029541, -0.121094, 0.0268555,
           -0.0279541, 0.0308838, 0.0405273, -0.130859, 0.0830078, 0.0157471, -0.116699, -0.0294189, -0.0708008])
w3 = Word('at',
          [-0.0585938, -0.0375977, 0.0727539, 0.108887, 0.0664062, 0.048584, 0.126953, -0.0581055, 0.0688477, 0.090332,
           -0.199219, -0.0407715, 0.0446777, -0.0869141, -0.0544434, 0.0358887, -0.0554199, 0.113281, 0.0737305,
           -0.0476074, -0.139648, -0.10498, 0.0332031, 0.00921631, -0.0476074, -0.0299072, -0.0888672, 0.0742188,
           0.0537109, 0.0111694, 0.081543, -0.0922852, -0.223633, -0.166016, -0.0419922, -0.0102539, -0.0742188,
           -0.12793, 0.0045166, 0.0893555, -0.0299072, -0.172852, -0.0712891, -0.0761719, -0.0107422, 0.0869141,
           -0.0551758, 0.225586, 0.0458984, 0.169922, -0.0168457, 0.147461, 0.0116577, -0.0167236, -0.111328, 0.0639648,
           -0.0742188, 0.112305, -0.00787354, -0.100586, -0.28125, 0.0163574, -0.0986328, -0.279297, -0.0844727,
           -0.0546875, 0.102051, 0.192383, 0.078125, 0.210938, 0.112793, 0.000145912, 0.131836, 0.0169678, 0.106445,
           -0.0230713, -0.0732422, 0.126953, -0.0957031, 0.0498047, 0.0634766, -0.00765991, 0.136719, 0.0913086,
           0.00430298, -0.0456543, 0.133789, -0.0172119, -0.12207, 0.0412598, -0.0986328, -0.0161133, -0.0162354,
           -0.100586, -0.175781, -0.050293, 0.146484, 0.0390625, -0.117676, -0.0476074, 0.0961914, 0.00366211, 0.144531,
           -0.120605, -0.0272217, 0.000968933, 0.0712891, -0.0830078, -0.0583496, -0.0834961, 0.138672, 0.0270996,
           -0.118164, -0.0854492, -0.0159912, 0.00872803, 0.151367, -0.0062561, 0.253906, 0.0566406, -0.00193787,
           0.026001, 0.0737305, -0.0583496, -0.0471191, -0.00196838, -0.0751953, -0.0556641, 0.0283203, 0.100098,
           -0.0166016, -0.251953, -0.0253906, -0.141602, -0.0027771, -0.0776367, 0.0834961, -0.0493164, -0.141602,
           0.199219, 0.0634766, 0.0246582, 0.00230408, -0.0864258, -0.0461426, 0.0135498, 0.0708008, -0.163086,
           -0.125977, 0.0571289, -0.0344238, 0.212891, -0.00160217, 0.0737305, -0.0280762, -0.0883789, -0.125977,
           0.0144043, -0.015625, 0.0756836, 0.0688477, -0.0776367, -0.0275879, 0.103516, 0.0412598, 0.117188,
           -0.0126953, 0.0415039, -0.0305176, -0.0664062, -0.0688477, -0.0664062, 0.0947266, -0.00260925, -0.172852,
           -0.202148, -0.013855, 0.103027, 0.0859375, 0.0571289, -0.036377, 0.10498, -0.0932617, 0.065918, -0.0383301,
           -0.0629883, -0.00238037, 0.111328, 0.114258, -0.0756836, -0.0361328, 0.00271606, -0.106445, 0.0703125,
           -0.271484, 0.0103149, -0.0128174, 0.0703125, -0.0111084, -0.0737305, 0.0786133, -0.0922852, -0.0216064,
           -0.0488281, 0.03125, -0.131836, -0.00088501, 0.199219, -0.111328, 0.108398, 0.0446777, -0.081543, -0.0893555,
           0.03125, -0.135742, 0.0180664, 0.0227051, -0.046875, -0.0957031, 0.110352, 0.0620117, 0.181641, 0.090332,
           -0.158203, 0.102539, -0.106934, 0.0264893, 0.0202637, 0.010376, -0.0952148, 0.043457, -0.209961,
           -0.000865936, -0.0106812, -0.00564575, -0.0737305, 0.0742188, 0.102539, 0.124023, 0.154297, 0.00445557,
           0.111328, -0.119141, -0.231445, 0.0245361, 0.00595093, 0.0195312, -0.0324707, -0.150391, -0.115234,
           -0.146484, -0.0090332, 0.0285645, -0.132812, 0.152344, -0.0593262, 0.0510254, 0.113281, -0.115723, 0.0561523,
           0.0810547, 0.0167236, 0.116211, 0.027832, 0.147461, 0.0172119, 0.090332, 0.0761719, 0.144531, -0.0245361,
           -0.052002, 0.0471191, 0.0722656, 0.0917969, 0.120117, -0.141602, -0.0228271, -0.124512, -0.0673828,
           -0.059082, -0.0375977, -0.0805664, -0.0693359, 0.0524902, 0.0820312, 0.0194092, -0.0810547, -0.0932617,
           0.0683594, -0.0212402, -0.032959, 0.0527344, -0.114258, 0.1875, 0.00296021, -0.00274658, -0.0471191,
           -0.10791, -0.0864258, -0.0319824])
w4 = Word('not',
          [0.0849609, -0.0952148, 0.119141, 0.111816, -0.111328, 0.0498047, 0.114258, -0.0986328, 0.0996094, -0.0415039,
           0.0128784, -0.181641, -0.116211, 0.0238037, -0.164062, 0.126953, 0.120605, 0.00946045, 0.0415039, -0.0952148,
           -0.129883, -0.115234, 0.0751953, -0.0498047, 0.065918, -0.0290527, -0.0898438, 0.0844727, -0.0478516,
           -0.0270996, -0.103027, 0.11084, 0.0142212, -0.0986328, 0.0412598, 0.0722656, 0.109863, 0.0113525, -0.0148315,
           0.0456543, 0.140625, 0.146484, 0.259766, -0.167969, -0.00145721, -0.0214844, 0.0189209, 0.0400391, 0.0559082,
           0.0380859, 0.00202942, 0.0712891, -0.0524902, -0.027832, 0.111328, 0.119141, -0.0524902, -0.0791016,
           0.103027, -0.118164, 0.0366211, 0.136719, -0.090332, -0.0703125, -0.0390625, -0.0174561, -0.081543, 0.242188,
           -0.180664, 0.0957031, 0.090332, 0.199219, 0.0473633, -0.0551758, -0.222656, -0.0742188, 0.161133, 0.104004,
           0.11377, 0.112793, 0.00497437, -0.0510254, 0.0395508, 0.0490723, -0.139648, -0.0888672, -0.113281, 0.136719,
           -0.032959, -0.234375, 0.109863, -0.0214844, -0.176758, -0.0308838, 0.0603027, -0.173828, 0.122559, 0.106934,
           -0.0854492, 0.0600586, -0.0791016, 0.0515137, 0.0250244, 0.0883789, -0.0932617, -0.00817871, -0.0991211,
           -0.154297, 0.0319824, -0.0272217, -0.177734, -0.0458984, -0.0878906, -0.00209045, 0.133789, -0.0888672,
           0.0908203, -0.128906, -0.000522614, 0.0986328, -0.130859, 0.02771, 0.0490723, 0.0893555, -0.113281,
           -0.0410156, -0.0917969, -0.108398, 0.0402832, -0.253906, -0.0292969, -0.106445, -0.0766602, -0.074707,
           -0.133789, -0.211914, 0.0289307, 0.0766602, 0.0551758, 0.0189209, 0.0512695, -0.207031, 0.196289, -0.0917969,
           -0.026123, 0.0292969, 0.02771, -0.200195, 0.103027, 0.0615234, 0.0795898, 0.116699, -0.0415039, -0.0551758,
           0.0932617, 0.0737305, -0.0917969, -0.0424805, -0.0966797, 0.059082, 0.0957031, 0.155273, 0.0908203,
           0.0517578, 0.0874023, -0.0893555, 0.0952148, 0.0820312, 0.134766, -0.0908203, -0.0961914, -0.0390625,
           -0.118652, -0.0791016, -0.0883789, 0.00372314, 0.202148, -0.0834961, -0.081543, -0.11084, -0.11084,
           -0.0593262, 0.102539, 0.0534668, 0.0109863, -0.0078125, -0.0378418, 0.0483398, -0.0634766, 0.205078,
           -0.0153809, -0.0211182, 0.00436401, 0.108398, 0.123047, -0.026001, -0.00346375, -0.0125732, -0.0200195,
           -0.116211, 0.0810547, 0.0952148, -0.060791, 0.202148, -0.0317383, 0.0693359, -0.0654297, 0.0205078,
           0.0290527, -0.0515137, -0.0598145, 0.0142822, -0.0153198, -0.00619507, -0.236328, -0.00689697, 0.183594,
           -0.11377, -0.11377, -0.0727539, -0.0478516, -0.0839844, -0.217773, -0.0354004, 0.125977, -0.081543, 0.170898,
           0.0708008, -0.0106812, 0.0996094, 0.120117, -0.0158691, -0.097168, 0.0140991, 0.105469, -0.0922852,
           -0.00302124, -0.164062, 0.0698242, -0.147461, 0.0419922, 0.00708008, 0.10498, -0.115234, 0.0197754,
           -0.0332031, 0.00909424, 0.00823975, -0.00151825, -0.0996094, 0.0339355, -0.0037384, 0.277344, 0.00643921,
           0.188477, 0.0432129, 0.0947266, 0.0546875, -0.138672, -0.074707, 0.0373535, -0.0644531, -0.251953, 0.142578,
           -0.0473633, 0.125977, -0.041748, -0.0566406, -0.00921631, -0.0235596, 0.188477, 0.110352, 0.351562,
           0.0776367, -0.0981445, -0.0537109, -0.0358887, -0.166016, 0.0324707, -0.0810547, 0.0961914, -0.0135498,
           -0.0143433, 0.129883, 0.019165, 0.00421143, -0.00360107, -0.174805, -0.0869141, 0.0732422, -0.0664062,
           0.0344238, -0.00570679, -0.0332031, -0.000938416, 0.0319824, 0.0634766, -0.108887, 0.0488281, -0.130859])
w5 = Word('be',
          [-0.228516, -0.0883789, 0.12793, 0.150391, -0.0732422, 0.0864258, 0.0639648, 0.0966797, 0.0583496, 0.143555,
           -0.0292969, -0.186523, 0.0119629, 0.0495605, 0.0732422, 0.126953, 0.0432129, 0.124023, -0.0336914,
           0.00537109, 0.0223389, -0.0605469, 0.194336, -0.0038147, 0.133789, -0.00405884, -0.205078, -0.0578613,
           0.129883, 0.017334, -0.0961914, -0.0131836, -0.210938, 0.155273, 0.289062, -0.0727539, 0.0537109, -0.0231934,
           0.0961914, 0.00479126, 0.242188, 0.141602, 0.0805664, -0.0678711, -0.0461426, -0.0913086, 0.0563965,
           0.189453, 0.00153351, 0.0917969, 0.108887, 0.131836, 0.0820312, -0.0698242, 0.0688477, 0.00124359, 0.103516,
           -0.0378418, 0.0458984, 0.015625, -0.0766602, 0.0163574, -0.0732422, 0.0908203, -0.0864258, 0.0424805,
           -0.0844727, 0.197266, -0.0732422, 0.167969, 0.0397949, 0.0898438, 0.201172, -0.0505371, 0.0456543, 0.0184326,
           0.191406, 0.078125, 0.0234375, 0.213867, 0.123047, -0.173828, 0.122559, -0.0673828, 0.065918, 0.0756836,
           -0.0366211, 0.112305, 0.105469, 0.00396729, 0.0147095, 0.020752, 0.0114746, -0.149414, 0.109863, -0.0898438,
           0.0639648, 0.0512695, -0.0444336, -0.0688477, -0.0361328, -0.0874023, 0.0976562, 0.114258, -0.216797,
           -0.10498, -0.128906, -0.161133, -0.0101929, -0.0090332, 0.0893555, 0.00570679, -0.0349121, -0.0810547,
           -0.0522461, -0.0996094, -0.0480957, -0.148438, 0.233398, 0.0839844, 0.0595703, -0.11377, -0.078125, 0.123047,
           -0.158203, 0.0610352, 0.0324707, 0.0018158, 0.164062, -0.0478516, 0.090332, -0.0180664, -0.0625, -0.126953,
           -0.0693359, -0.0722656, 0.00010252, -0.09375, -0.0441895, 0.137695, 0.143555, -0.0810547, 0.0253906,
           0.041748, 0.0195312, -0.104004, 0.0322266, -0.0976562, -0.0996094, -0.0480957, -0.191406, 0.10498,
           -0.0913086, -0.0273438, 0.032959, -0.166992, -0.0683594, -0.205078, -0.0917969, -0.0255127, 0.101074,
           0.109375, 0.0805664, -0.0179443, 0.059082, -0.0771484, -0.0412598, 0.0424805, -0.0810547, 0.0454102,
           -0.227539, -0.314453, -0.194336, -0.166992, -0.0839844, -0.124512, 0.0180664, -0.102051, 0.0683594, 0.112305,
           0.0252686, -0.103027, -0.059082, 0.213867, -0.133789, -0.0181885, -0.0126953, 0.0119019, 0.125977, 0.175781,
           -0.00692749, 0.0952148, 0.0185547, -0.0568848, -0.11377, -0.114746, -0.140625, -0.102539, 0.00714111,
           -0.0908203, 0.110352, -0.0917969, -0.0598145, -0.0179443, -0.0751953, 0.00334167, -0.108887, -0.0233154,
           0.148438, 0.0400391, -0.0800781, -0.165039, 0.101074, 0.104492, -0.220703, 0.0424805, 0.114258, -0.167969,
           -0.120605, -0.0456543, -0.0424805, -0.214844, -0.0639648, -0.157227, 0.15918, 0.0241699, 0.0422363, 0.150391,
           0.105469, 0.00230408, 0.0654297, 0.0262451, -0.12207, -0.0722656, 0.226562, 0.0189209, -0.213867, 0.0490723,
           0.0913086, -0.00909424, 0.0241699, 0.0795898, 0.138672, -0.0585938, -0.0791016, -0.0495605, -0.0554199,
           -0.0146484, -0.143555, 0.0361328, -0.0507812, -0.0454102, -0.0603027, 0.0617676, 0.136719, 0.0576172,
           0.0378418, 0.126953, -0.032959, -0.112793, 0.197266, -0.207031, -0.0996094, 0.314453, 0.0786133, 0.265625,
           0.0397949, 0.0839844, 0.015564, -0.110352, 0.191406, 0.0976562, 0.131836, 0.164062, 0.0366211, 0.0145264,
           0.00836182, -0.213867, 0.0595703, -0.0488281, 0.134766, 0.0388184, 0.065918, -0.0375977, 0.0854492,
           -0.0510254, -0.111816, -0.144531, 0.100098, 0.203125, -0.109863, 0.0649414, 0.117188, 0.0454102, 0.214844,
           0.0429688, -0.139648, -0.212891, 0.188477, -0.145508])
w6 = Word('by',
          [-0.115723, -0.0314941, 0.15918, 0.138672, -0.00506592, 0.0281982, -0.0339355, -0.115723, 0.0324707, 0.138672,
           -0.100098, -0.126953, -0.0395508, -0.0183105, 0.000234604, -0.0805664, 0.045166, 0.0981445, -0.0566406,
           0.0600586, 0.0888672, 0.050293, -0.0164795, -0.0556641, 0.213867, 0.0142822, -0.131836, 0.0319824, 0.0311279,
           0.125977, -0.003479, -0.155273, -0.168945, 0.140625, 0.160156, -0.0375977, -0.0947266, -0.0390625, 0.170898,
           -0.0512695, 0.146484, 0.0961914, -0.0266113, 0.0390625, 0.135742, 0.0527344, -0.0415039, -0.052002, 0.157227,
           0.09375, 0.00567627, 0.126953, -0.00531006, -0.0480957, 0.0541992, 0.166992, 0.0385742, 0.034668, -0.0981445,
           -0.074707, -0.133789, 0.0269775, -0.104004, -0.0249023, -0.0771484, -0.0236816, -0.0012207, 0.106445,
           0.0437012, 0.196289, -0.0220947, -0.0795898, 0.0249023, 0.0388184, -0.0108032, 0.226562, 0.0869141, 0.170898,
           0.0507812, 0.0771484, -0.00130463, 0.00643921, 0.041748, 0.0252686, 0.0917969, -0.0800781, -0.0673828,
           0.0400391, -0.0351562, -0.0703125, -0.0947266, 0.181641, -0.0756836, -0.0571289, 0.287109, 0.114258,
           -0.146484, -0.0161133, -0.00570679, -0.0432129, 0.21875, -0.10791, -0.0515137, 0.0957031, -0.0402832,
           0.115723, -0.0766602, 0.0478516, 0.0280762, -0.104004, 0.0644531, 0.048584, -0.0712891, 0.0327148,
           -0.0673828, -0.081543, 0.0437012, 0.00109863, 0.170898, 0.198242, -0.123047, 0.175781, -0.185547,
           -0.00793457, 0.0617676, 0.0334473, 0.0571289, -0.00219727, 0.199219, 0.0654297, -0.00282288, 0.0986328,
           0.00389099, -0.0878906, -0.0751953, 0.0252686, -0.0612793, -0.0551758, -0.126953, -0.00601196, 0.137695,
           -0.0334473, -0.0737305, 0.078125, 0.041748, -0.0593262, 0.0588379, 0.000926971, 0.0864258, 0.0917969,
           0.0539551, 0.0415039, 0.136719, 0.189453, 0.0844727, -0.146484, -0.0588379, -0.166016, 0.0334473, 0.00521851,
           -0.0098877, 0.0830078, 0.0495605, 0.106445, -0.123047, -0.0114136, 0.0107422, -0.074707, -0.0314941,
           0.0123901, -0.146484, -0.207031, -0.0688477, -0.157227, -0.194336, -0.0878906, -0.0454102, 0.0854492,
           -0.0556641, -0.0834961, -0.0512695, -0.164062, -0.117188, 0.112793, -0.0605469, 0.0178223, -0.0341797,
           0.105957, 0.0839844, 0.0517578, 0.0605469, 0.0127563, -0.0101318, 0.0294189, -0.0805664, -0.0976562,
           -0.00479126, 0.0153198, -0.0216064, -0.032959, 0.125, -0.0351562, -0.0786133, -0.015625, -0.012085, 0.160156,
           0.0664062, 0.0595703, 0.0834961, -0.0869141, -0.0544434, -0.164062, 0.097168, 0.101562, 0.00958252,
           0.0235596, 0.0839844, -0.0419922, -0.0407715, 0.0483398, -0.0246582, -0.0678711, 0.0610352, -0.176758,
           0.0351562, 0.0471191, 0.0274658, 0.140625, 0.267578, -0.0512695, 0.0942383, -0.0522461, 0.03125, 0.0336914,
           -0.0874023, -0.0908203, 0.010376, 0.111328, -0.0878906, 0.0101318, -0.183594, -0.0625, 0.201172, -0.00891113,
           0.0239258, 0.130859, 0.3125, 0.0917969, -0.104492, 0.0220947, 0.0583496, -0.144531, -0.104492, 0.0981445,
           0.0722656, -0.180664, 0.115723, -0.0290527, 0.0864258, -0.0908203, 0.0751953, 0.0673828, 0.015564, 0.112793,
           -0.0120239, 0.128906, -0.0157471, 0.138672, 0.173828, 0.00634766, 0.0737305, 0.0668945, -0.119141, 0.0913086,
           0.0174561, -0.0888672, -0.0551758, -0.118652, 0.123047, 0.00561523, 0.0341797, 0.145508, -0.0583496,
           -0.0419922, 0.157227, 0.0693359, -0.142578, -0.0393066, 0.081543, 0.0603027, -0.121582, -0.074707,
           -0.0693359, 0.0351562, -0.0322266, 0.0476074, -0.212891, 0.0262451, -0.0625, -0.0415039])
w7 = Word('are', [-0.0966797, -0.0263672, 0.090332, 0.0322266, -0.245117, 0.0561523, 0.0252686, -0.00939941, 0.0549316,
                  0.0612793, -0.0952148, 0.0222168, -0.0197754, 0.22168, -0.0424805, 0.0166016, -0.0727539, 0.376953,
                  -0.209961, 0.118652, -0.203125, -0.138672, -0.0114136, 0.0175781, 0.285156, 0.114746, -0.15625,
                  0.0712891, -0.0834961, -0.201172, -0.101074, -0.0742188, -0.142578, 0.0322266, 0.192383, 0.074707,
                  -0.0314941, -0.0296631, 0.0893555, -0.0356445, 0.322266, 0.0361328, -0.00939941, 0.105469, 0.115234,
                  -0.144531, 0.000396729, 0.0583496, -0.120605, -0.108398, -0.0109253, 0.18457, -0.138672, -0.0341797,
                  0.151367, -0.0332031, 0.209961, -0.0194092, 0.0184326, 0.115234, -0.120605, 0.145508, -0.162109,
                  -0.0532227, -0.0698242, -0.109375, -0.126953, 0.249023, -0.205078, 0.0291748, 0.020874, 0.144531,
                  0.0366211, -0.0179443, -0.0600586, -0.0927734, 0.0471191, 0.010376, 0.0108643, 0.277344, 0.0441895,
                  -0.15918, 0.0952148, -0.176758, 0.10498, 0.074707, -0.251953, -0.0393066, 0.123047, 0.0256348,
                  0.0055542, 0.103516, -0.0152588, -0.144531, 0.0869141, -0.0727539, 0.104004, 0.0230713, 0.151367,
                  0.0588379, 0.0849609, -0.0849609, -0.0449219, 0.150391, 0.00558472, -0.129883, 0.0568848, -0.0178223,
                  0.164062, 0.0196533, 0.0412598, -0.00405884, -0.00274658, 0.0942383, -0.132812, 0.126953, 0.15625,
                  -0.196289, 0.106934, 0.0400391, 0.0402832, 0.179688, -0.0703125, 0.0189209, 0.0664062, 0.00044632,
                  -0.15332, 0.0507812, 0.0634766, 0.0111084, 0.204102, -0.206055, 0.0644531, -0.155273, 0.0222168,
                  0.0136719, 0.298828, -0.0585938, 0.0976562, 0.0090332, 0.020752, 0.0157471, 0.326172, 0.0284424,
                  -0.0454102, 0.0888672, 0.120605, -0.125977, -0.0598145, -0.0264893, -0.177734, 0.0913086, -0.0380859,
                  -0.0952148, 0.0273438, -0.019165, -0.110352, -0.230469, 0.00202942, 0.0603027, -0.100586, 0.222656,
                  -0.02771, 0.0336914, 0.144531, -0.0727539, -0.132812, -0.0162354, 0.164062, -0.00854492, -0.466797,
                  -0.345703, -0.111328, -0.0957031, 0.0378418, -0.137695, -0.180664, 0.0712891, 0.15332, 0.0683594,
                  -0.122559, -0.0698242, 0.0688477, 0.00878906, 0.0236816, -0.0698242, -0.0366211, 0.0878906, 0.121582,
                  0.144531, 0.0473633, -0.043457, -0.00671387, -0.121582, -0.279297, 0.144531, 0.0544434, -0.209961,
                  -0.0893555, -0.0708008, 0.176758, 0.0195312, -0.101074, -0.0664062, -0.347656, 0.100098, -0.0703125,
                  -0.214844, -0.0155029, 0.150391, 0.0942383, -0.145508, 0.11084, 0.0791016, -0.0805664, 0.150391,
                  0.145508, -0.11377, -0.259766, -0.0678711, -0.0966797, -0.227539, -0.194336, -0.179688, 0.107422,
                  0.0177002, -0.12207, 0.0539551, -0.125977, 0.0839844, 0.122559, 0.0157471, -0.0854492, 0.217773,
                  0.192383, 0.0324707, -0.078125, 0.0101318, 0.0107422, 0.041748, 0.065918, 0.164062, 0.045166,
                  0.0195312, 0.0617676, 0.124023, 0.0106812, 0.231445, -0.202148, 0.0766602, -0.0620117, -0.0795898,
                  0.170898, 0.0791016, -0.0178223, -0.0306396, 0.0507812, 0.163086, 0.00866699, 0.0546875, 0.108398,
                  -0.0825195, -0.0634766, 0.283203, -0.0185547, 0.416016, -0.261719, 0.0251465, -0.0146484, -0.114746,
                  0.164062, 0.357422, 0.074707, 0.248047, 0.0961914, 0.149414, -0.0186768, -0.271484, -0.0541992,
                  -0.0986328, 0.0771484, -0.191406, -0.0142212, -0.128906, 0.0546875, 0.0664062, -0.172852, -0.0432129,
                  0.142578, 0.0996094, 0.0241699, -0.123047, 0.0314941, 0.0393066, 0.0322266, 0.208008, -0.0559082,
                  -0.0196533, 0.213867, 0.136719])
w8 = Word('have',
          [-0.139648, -0.034668, -0.0537109, 0.179688, -0.0368652, -0.0257568, 0.00485229, -0.0834961, 0.00817871,
           0.324219, -0.0908203, -0.147461, -0.108398, 0.057373, -0.0100708, -0.00238037, 0.207031, 0.0898438,
           -0.161133, -0.0393066, -0.103027, -0.0712891, 0.15625, -0.229492, 0.12793, 0.0742188, -0.112305, -0.11377,
           0.0322266, -0.0126343, -0.00466919, 0.074707, -0.114746, 0.0378418, 0.180664, -0.0339355, 0.133789, -0.1875,
           -0.0554199, 0.125977, 0.150391, 0.1875, -0.000602722, -0.0483398, -0.0454102, -0.131836, -0.0164795,
           0.0319824, 0.118164, -0.0639648, -0.0527344, -0.0057373, -0.146484, -0.0588379, -0.0397949, 0.0541992,
           0.0301514, -0.045166, 0.0544434, -0.121094, -0.0385742, 0.154297, -0.0184326, 0.0111084, 0.0186768,
           -0.0981445, -0.0247803, 0.152344, -0.0708008, 0.052002, -0.0244141, 0.125, 0.00228882, 0.119629, -0.102539,
           -0.0238037, 0.182617, 0.188477, -0.0522461, 0.074707, 0.0568848, -0.0505371, 0.0839844, 0.046875, -0.0483398,
           -0.0688477, -0.267578, 0.0227051, -0.158203, -0.0101929, -0.00994873, 0.125977, -0.0581055, -0.133789,
           -0.0209961, -0.109863, 0.00375366, 0.0839844, -0.065918, -0.0306396, 0.166016, -0.240234, 0.0654297,
           0.0380859, -0.0522461, -0.0534668, -0.11377, -0.09375, 0.176758, -0.0688477, -0.202148, 0.0756836, -0.045166,
           -0.0805664, 0.046875, -0.0505371, 0.0991211, -0.0849609, 0.0263672, -0.0211182, -0.0932617, -0.0388184,
           -0.0947266, 0.125977, -0.201172, -0.145508, -0.0192871, -0.112305, 0.0213623, -0.0771484, 0.112305,
           -0.145508, -0.210938, -0.111816, 0.00238037, -0.10791, 0.123535, -0.0200195, -0.050293, -0.0108643,
           -0.0449219, -0.0422363, 0.0324707, 0.00177002, 0.0266113, 0.0227051, -0.0290527, -0.117188, -0.209961,
           0.0153198, -0.0839844, -0.0922852, -0.223633, -0.0913086, 0.0703125, 0.00866699, -0.146484, -0.149414,
           -0.0142212, 0.0869141, 0.0537109, 0.100586, -0.0480957, 0.09375, 0.0883789, -0.154297, -0.0952148, -0.166992,
           -0.00156403, -0.0957031, -0.177734, -0.0429688, -0.257812, -0.0776367, -0.020874, -0.183594, -0.0849609,
           -0.0932617, 0.0551758, -0.0620117, -0.0446777, -0.137695, 0.149414, 0.0996094, 0.0356445, -0.214844,
           -0.026001, -0.0622559, 0.115723, 0.120605, 0.00769043, 0.0527344, 0.0289307, -0.0284424, -0.0407715,
           -0.117188, 0.125977, 0.00331116, 0.0339355, -0.183594, 0.11377, 0.15332, -0.0717773, -0.00643921, -0.0197754,
           -0.173828, -0.065918, -0.124512, 0.0888672, 0.0222168, -0.0410156, -0.0844727, 0.060791, 0.0986328,
           -0.131836, 0.0101318, 0.109863, -0.0820312, -0.108398, -0.0498047, -0.0668945, -0.0195312, -0.0371094,
           -0.0310059, 0.0397949, -0.00952148, 0.115723, 0.0283203, 0.0324707, -0.0383301, 0.104492, -0.162109,
           0.0527344, 0.0622559, 0.0996094, 0.0194092, -0.0556641, -0.109375, 0.0869141, -0.154297, -0.09375, 0.0800781,
           0.125, 0.000272751, 0.0976562, 0.142578, 0.0708008, 0.078125, -0.144531, 0.0229492, -0.0368652, 0.0913086,
           0.114258, 0.0493164, -0.0219727, -0.0105591, 0.0388184, 0.255859, -0.0766602, -0.12793, 0.0717773,
           -0.0361328, -0.0122681, 0.216797, 0.041748, 0.244141, -0.0825195, 0.142578, 0.0834961, 0.0032959, 0.21582,
           0.229492, 0.130859, 0.078125, -0.0883789, -0.0197754, 0.0132446, -0.192383, 0.0458984, -0.222656, -0.0180664,
           0.0493164, 0.162109, 0.0683594, 0.0505371, 0.000614166, -0.0737305, 0.020874, 0.0375977, 0.178711,
           -0.0490723, 0.0634766, 0.0805664, 0.0888672, 0.0776367, -0.0466309, -0.0717773, -0.118164, -0.00245667,
           -0.0722656])
w9 = Word('he', [0.192383, 0.12793, -0.019165, -0.0292969, 0.0310059, -0.0844727, -0.0996094, -0.0534668, 0.165039,
                 -0.0336914, -0.0151978, -0.183594, 0.0605469, -0.0446777, -0.285156, 0.043457, -0.0310059, 0.0722656,
                 0.10498, -0.020874, -0.00720215, 0.124512, 0.0166016, -0.00549316, -0.0644531, -0.166992, -0.116211,
                 -0.0262451, 0.18457, 0.0371094, 0.0238037, 0.163086, -0.0140381, 0.0245361, 0.0844727, -0.0307617,
                 0.148438, -0.00891113, 0.0373535, 0.0206299, 0.283203, -0.0424805, 0.302734, 0.0109863, 0.0480957,
                 0.126953, -0.124023, 0.0290527, 0.0473633, 0.0673828, 0.134766, 0.0849609, -0.0314941, -0.108398,
                 -0.0446777, -0.0268555, -0.019043, -0.0634766, -0.027832, -0.115723, 0.212891, 0.212891, -0.0116577,
                 0.0187988, 0.0578613, 0.0664062, -0.046875, -0.0791016, -0.0123901, 0.125977, 0.065918, -0.000999451,
                 0.0291748, 0.0361328, -0.120605, -0.111328, 0.140625, 0.103027, 0.0522461, 0.00811768, 0.128906,
                 -0.140625, 0.0429688, -0.115723, -0.0585938, -0.0981445, 0.00805664, 0.150391, -0.0432129, -0.0849609,
                 -0.0888672, 0.134766, -0.0385742, -0.10498, -0.118652, -0.0551758, 0.11377, 0.03125, 0.0067749,
                 -0.141602, -0.175781, -0.0947266, 0.0244141, 0.020752, -0.078125, -0.0187988, -0.0119629, -0.108398,
                 -0.00430298, -0.101074, -0.129883, 0.0233154, -0.03125, -0.0544434, 0.0186768, -0.0461426, -0.0898438,
                 -0.105957, 0.158203, -0.0218506, -0.178711, -0.0144653, -0.0512695, 0.0703125, -0.244141, -0.177734,
                 0.0742188, -0.045166, -0.019043, -0.0683594, -0.166016, -0.0913086, -0.145508, -0.211914, -0.103027,
                 -0.0800781, -0.0585938, 0.191406, -0.0250244, 0.207031, 0.0380859, -0.00952148, 0.0419922, 0.0072937,
                 0.00772095, 0.0231934, -0.140625, -0.130859, -0.155273, 0.150391, 0.0289307, 0.12793, -0.257812,
                 0.0203857, -0.0505371, -0.00680542, -0.0820312, -0.143555, 0.0634766, 0.0375977, 0.0698242, 0.101074,
                 0.12793, 0.136719, -0.0874023, -0.00714111, 0.050293, 0.00361633, 0.212891, -0.114258, 0.010376,
                 -0.0220947, -0.169922, -0.132812, -0.00364685, -0.03125, 0.0529785, -0.150391, 0.00610352, -0.0224609,
                 -0.11377, 0.0241699, 0.0395508, -0.0339355, -0.00848389, -0.0327148, 0.0305176, 0.160156, 0.0683594,
                 -0.078125, 0.0454102, 0.222656, 0.0546875, 0.211914, 0.0444336, -0.020874, -0.160156, -0.0025177,
                 -0.0654297, -0.15918, -0.138672, -0.0120239, 0.120605, -0.013855, 0.194336, -0.115234, -0.0300293,
                 0.0654297, 0.0219727, -0.09375, 0.0722656, -0.177734, -0.00842285, -0.12793, -0.227539, 0.0336914,
                 0.0422363, 0.0375977, -0.143555, -0.0180664, 0.0527344, 0.020752, -0.0327148, -0.0250244, 0.337891,
                 -0.0986328, 0.12793, 0.0917969, 0.0913086, -0.00448608, 0.00753784, -0.0541992, 0.0299072, -0.11377,
                 0.181641, -0.00415039, -0.201172, -0.0140991, 0.0189209, -0.0932617, 0.00692749, -0.041748, -0.102539,
                 -0.0366211, -0.0305176, -0.0397949, -0.0175781, -0.0218506, 0.10791, 0.0212402, 0.118652, 0.00390625,
                 -0.0429688, -0.00023365, 0.111816, 0.114258, 0.0385742, -0.0385742, -0.146484, -0.0532227, 0.0512695,
                 -0.00576782, -0.186523, 0.103027, 0.137695, 0.0566406, 0.0020752, -0.0137329, 0.0268555, -0.0177002,
                 0.191406, 0.00415039, 0.114746, -0.0106201, -0.081543, -0.0991211, 0.0194092, -0.191406, -0.0378418,
                 -0.0771484, 0.0761719, -0.0197754, 0.164062, 0.0825195, -0.0253906, -0.00970459, 0.00294495,
                 -0.0761719, 0.0314941, 0.125, -0.0617676, -0.043457, -0.11377, -0.00872803, -0.12793, 0.107422,
                 0.00411987, -0.172852, 0.123047, -0.160156])

# create some artificial sentences using these words
sentence1 = Sentence([w1, w2, w3, w4, w5, w6, w7, w8, w9])
sentence2 = Sentence([w2, w3, w1])
sentence3 = Sentence([w3, w1, w2])

# calculate and display the result
sentence_vectors = sentence_to_vec([sentence1, sentence2, sentence3], embedding_size)
# all vectors
print(sentence_vectors)

# or just the vector for the first sentence
print(sentence_vectors[0])
