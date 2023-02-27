import seaborn as sns

from data_info import *
import cv2
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer, TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import confusion_matrix, classification_report
from collections import Counter
from sklearn.svm import LinearSVC, SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
import re

class Steganalysis:
    PXL_FORM = 3
    COLUMNS = ['R', 'G', 'B']

    def __init__(self, mal_tag:bool = False):
        self.basic_data = {}
        dict_load = {BENIGN_DIR: 0, MALWARE: 1} if mal_tag else SIGNS_DICT
        for atk_type in dict_load:
            type_num = dict_load[atk_type]

            self.basic_data[type_num] = []
            files_path = data_info.join_path('..', DATA_DIR, atk_type, '*', ext=EXT)
            print(files_path)
            files = glob.glob(files_path)
            i = 0
            for file in files:
                if i == 20:
                    break
                self.basic_data[type_num].append((cv2.resize(cv2.imread(file), (64, 64)) % 16) / 16.0)
                print(cv2.resize(cv2.imread(file), (64, 64)))
                i += 1
            # self.basic_data[type_num] = self.basic_data[type_num][:20]

    @staticmethod
    def get_files(mal_tag: bool = False):
        files_total, labels = [], []
        dict_load = {BENIGN_DIR: 0, MALWARE: 1} if mal_tag else SIGNS_DICT
        for atk_type in dict_load:
            type_num = dict_load[atk_type]
            files_path = data_info.join_path('..', DATA_DIR, atk_type, '*', ext=EXT)
            print(files_path)
            files = glob.glob(files_path)
            for file in files:
                files_total += [file]
                labels += [type_num]
        return files_total, labels

    def pics_countes(self):
        list_counted = []
        tags = []
        for type_num in self.basic_data:
            for img in self.basic_data[type_num]:
                list_counted += [self.count_vals_img(img)]
                tags += [type_num]
        return np.array(list_counted), np.array(tags)

    def pics_lists(self):
        list_img = []
        tags = []
        for type_num in self.basic_data:
            for img in self.basic_data[type_num]:
                list_img += [img]
                tags += [type_num]
        return list_img, np.array(tags)

    @staticmethod
    def count_vals_img(im_arr: numpy.ndarray, lsb: int = None):
        if lsb is None:
            lsb = 4
        max_num = 2 ** lsb
        im_2d = im_arr.reshape(-1, Steganalysis.PXL_FORM) % max_num   # turn to list of pixels
        df = pd.DataFrame(im_2d, columns=Steganalysis.COLUMNS)
        mm = pd.DataFrame(np.zeros((max_num, 3), dtype='int64'), columns=Steganalysis.COLUMNS)

        for col_name in df.columns.values:
            mm[col_name] = df.groupby(col_name)[col_name].count()
        mm = mm.fillna(0).astype('int64')
        list_RGB = []
        for color in Steganalysis.COLUMNS:
            list_RGB += list(mm[color])
        return list_RGB

    @staticmethod
    def data_extract(use_old: bool = False):
        if not os.path.exists('X.npy') or not os.path.exists('y.npy') or not use_old:
            steganalysis = Steganalysis()
            X, y = steganalysis.pics_countes()
            # print(X)
            # X, y = pd.DataFrame(X), pd.DataFrame(y)
            np.save('X.npy', X)
            np.save('y.npy', y)
        else:
            X, y = np.load('X.npy'), np.load('y.npy')
        return X, y


def sub_vars(X, y, filter: list = None):
    if filter is None:
        return X, y
    w = np.isin(y, np.array(filter))
    return X[w], y[w]


def value_accu(predictions, y_test):
    sns.set(rc={'figure.figsize': (15, 8)})
    true_labels = y_test

    cf_matrix = confusion_matrix(predictions, true_labels)
    clf_report = classification_report(true_labels, predictions, digits=5)
    heatmap = sns.heatmap(cf_matrix, annot=True, cmap='Blues', fmt='g',
                          xticklabels=np.unique(true_labels),
                          yticklabels=np.unique(true_labels))

    # The heatmap is cool but this is the most important result
    print(clf_report)


def run():
    X, y = Steganalysis.data_extract(use_old=True)
    X, y = sub_vars(X, y, [0, 1, 2, 3])
    X = numpy.array(X) / 255.0

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # We print the resulted datasets and count the difference
    print(X_train.shape, y_train.shape)
    print(X_test.shape, y_test.shape)

    # model = SVC(gamma='auto')
    model = LinearSVC()
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)

    value_accu(prediction, y_test)

# run()