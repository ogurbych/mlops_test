#!/usr/bin/python

import numpy as np

from catboost import CatBoostClassifier
from catboost import Pool
from catboost.utils import eval_metric

from sklearn.model_selection import train_test_split

# label need to be 0 to num_class -1
data = np.loadtxt('./dermatology.data', delimiter=',',
        converters={33: lambda x:int(x == '?'), 34: lambda x:int(x) - 1})

X = data[:, :33]
Y = data[:, 34]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y)

train_pool = Pool(X_train, Y_train)
test_pool = Pool(X_test, Y_test)

clf = CatBoostClassifier(
      learning_rate=0.1,
      custom_loss=['AUC', 'Accuracy'],
      iterations=500,   
)

clf.fit(train_pool,
        eval_set=test_pool,
        metric_period=10,
        plot=True,
        verbose=50)

clf.save_model("model.cbm")
