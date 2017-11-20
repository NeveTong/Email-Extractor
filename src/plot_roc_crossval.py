"""

Receiver Operating Characteristic (ROC) with cross validation

"""

print(__doc__)

import numpy as np
from scipy import interp
import matplotlib.pyplot as plt
from itertools import cycle

from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score
from sklearn.model_selection import StratifiedKFold
from sklearn.datasets import load_svmlight_file
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import *
from sklearn.svm import *

###############################################################################
# Data IO and generation

# import some data to play with
dataset = load_svmlight_file('svm-feature.txt')
X = dataset[0]
y = dataset[1]
n_samples, n_features = X.shape

###############################################################################
# Classification and ROC analysis

# Run classifier with cross-validation and plot ROC curves
cv = StratifiedKFold(n_splits=10)
classifier = MLPClassifier(verbose=True)
#classifier = SVC(probability=True)
#classifier = AdaBoostClassifier()

mean_tpr = 0.0
mean_fpr = np.linspace(0, 1, 100)

colors = cycle(['#FFC1C1', '#FF7F50', '#FF1493', '#FF0000', '#FFFF00', '#B22222', '#A0522D', '#00B2EE', '#A020F0', '#8B2323'])
lw = 2

i = 0
for (train, test), color in zip(cv.split(X, y), colors):
    probas_ = classifier.fit(X[train], y[train]).predict_proba(X[test])
    # Compute ROC curve and area the curve
    fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
    
    mean_tpr += interp(mean_fpr, fpr, tpr)
    mean_tpr[0] = 0.0
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, linestyle='--', lw=lw, color=color,
             label='ROC fold %d (area = %0.2f)' % (i + 1, roc_auc))

    i += 1
plt.plot([0, 1], [0, 1], lw=lw, color='#436EEE', label='Luck')

mean_tpr /= cv.get_n_splits(X, y)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
plt.plot(mean_fpr, mean_tpr, color='g', label='Mean ROC (area = %0.2f)' % mean_auc, lw=lw)

plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('MLP')
plt.legend(loc="lower right")
plt.show()
