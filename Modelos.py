import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from Organizar_bases import OrganizarBase
from sklearn.linear_model import (
    LogisticRegression, PassiveAggressiveClassifier, RidgeClassifier,
    Perceptron, SGDClassifier)
from sklearn.naive_bayes import BernoulliNB, ComplementNB, GaussianNB
from sklearn.neighbors import KernelDensity, KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC, NuSVC, SVC
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
import warnings
from time import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
warnings.filterwarnings('ignore')


l = OrganizarBase()
info = l.info_partida()

# Arreglo base de datos
def ganador(columna, valor):
    if valor == 1:
        resultado = columna
    else:
        resultado = ''
    return resultado

y = (
    info.apply(lambda x: ganador('0', x['bResult']), axis = 1) + 
    info.apply(lambda x: ganador('1', x['rResult']), axis = 1))
y = y.astype(int)

X = info.drop(['bResult', 'rResult', 'Address'], axis = 1)
columnas = X.columns

# Setup the pipeline steps: steps
steps = [('imputation', SimpleImputer(strategy='most_frequent')),
        ('onehotencoder', OneHotEncoder())]

# Create the pipeline: pipeline
pipeline = Pipeline(steps)
# Fit the pipeline to the train set
X = pipeline.fit_transform(X).toarray()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size = 0.25, random_state = 123)

parameters = {
    'LogisticRegression': #35
        {'C': list(np.logspace(-5,2,7)),
         'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']},
    'PassiveAggressiveClassifier': #7
        {'C': list(np.logspace(-5,2,7))},
    'Perceptron': #21
        {'penalty': ['l2','l1','elasticnet'], 
         'alpha': list(1/(2*np.logspace(-5,2,7)))},
    'RidgeClassifier': #14
        {'alpha': list(1/(2*np.logspace(-5,2,7))),
         'normalize': [True, False]},
    'SGDClassifier': #42
        {'loss': ['hinge', 'log','squared_hinge'],
         'penalty': ['l2','l1'],
         'alpha': list(1/(2*np.logspace(-5,2,7)))},
    'BernoulliNB':  #7
        {'alpha': list(np.logspace(-5,2,7))},
    'ComplementNB': #14
        {'alpha': list(np.logspace(-5,2,7)), 'norm': [True, False]},
    'GaussianNB': #7
        {'var_smoothing': list(np.logspace(-10,1,7))},
    'MLPClassifier': #72
        {'hidden_layer_sizes': [100, 512],
              'activation': ['identity', 'logistic', 'tanh', 'relu'],
              'solver': ['lbfgs', 'sgd', 'adam'],
              'learning_rate': ['constant', 'invscaling', 'adaptive']},
    'LinearSVC': #28
        {'penalty': ['l1', 'l2'],
         'loss': ['hinge', 'squared_hinge'],
         'C': list(np.logspace(-5,2,7))},
    'NuSVC': #48
        {'nu': list(np.linspace(0.001,1,3)),
         'kernel':['linear', 'poly', 'rbf', 'sigmoid'],
         'degree': list(np.arange(start = 3, stop = 5, step = 1)),
         'gamma': ['scale', 'auto']},
    'ExtraTreeClassifier': #60
        {'criterion': ['gini', 'entropy'],
         'splitter': ['best', 'random'],
         'min_samples_split': list(np.arange(2, 11, 2)),
         'max_features': [None, 'sqrt', 'log2']},
    'KNeighborsClassifier': #8
        {'n_neighbors': list(np.arange(start = 3, stop = 10, step = 2)),
         'leaf_size': [26,30]},
    'DecisionTreeClassifier': #60
        {'criterion': ['gini', 'entropy'],
         'splitter': ['best', 'random'],
         'min_samples_split': list(np.arange(2, 11, 2)),
         'max_features': [None, 'sqrt', 'log2']},
    'SVC': #32
        {'C': list(np.logspace(-3,2,4)),
         'kernel':['linear', 'poly', 'rbf', 'sigmoid'],
         'gamma': ['scale', 'auto']}
        }

my_models = {
    'best_params': [],
    'score_train': [],
    'score_test': [],
    'model': [],
    'elapsed_time': []}

#Tiempo estimado para compilar 12 horas
#Abajo se encuentran los resultados obtenidos para no correr el for
for model_init, parameter_model in parameters.items():
    try:
        model_eval = eval(str(model_init + '(random_state = 123)'))
    except TypeError: 
        model_eval = eval(str(model_init + '()'))

    modelGS = eval(
        str('GridSearchCV(estimator = {}, param_grid = {}, cv = 2, scoring = "accuracy")'.\
            format(model_eval, parameter_model)))
    
    print('Inicia modelo: {}'.format(model_init))    
    
    start_time = time()
    
    modelGS.fit(X_train, y_train)
    
    my_models['model'].append(model_init)

    my_models['best_params'].append(modelGS.best_params_)
    
    my_models['score_train'].append(modelGS.score(X_train, y_train))
    
    my_models['score_test'].append(modelGS.score(X_test, y_test))
    
    my_models['elapsed_time'].append(time() - start_time)
    
    print('Finaliza modelo: {}'.format(model_init)) 
    
#Resultados con los mejores resultados según GridSearchCV modelos
my_models = {
    'best_params': [
        {'C': 0.4641588833612782, 'solver': 'liblinear'},
        {'C': 0.00014677992676220705},
        {'alpha': 49999.99999999999, 'penalty': 'l1'},
        {'alpha': 1.0772173450159412, 'normalize': True},
        {'alpha': 0.005, 'loss': 'hinge', 'penalty': 'l2'},
        {'alpha': 0.03162277660168379},
        {'alpha': 6.812920690579622, 'norm': False},
        {'var_smoothing': 0.14677992676220675},
        {'activation': 'relu',
        'hidden_layer_sizes': 512,
        'learning_rate': 'constant',
        'solver': 'adam'},
        {'C': 0.03162277660168379, 'loss': 'squared_hinge', 'penalty': 'l2'},
        {'degree': 3, 'gamma': 'scale', 'kernel': 'poly', 'nu': 0.5005},
        {'criterion': 'gini',
        'max_features': 'sqrt',
        'min_samples_split': 6,
        'splitter': 'best'},
        {'leaf_size': 26, 'n_neighbors': 7},
        {'criterion': 'gini',
        'max_features': 'sqrt',
        'min_samples_split': 6,
        'splitter': 'best'},
        {'C': 2.1544346900318843, 'gamma': 'scale', 'kernel': 'poly'}],
    'score_train': [
        0.8082239720034996,
        0.7226596675415573,
        0.5426071741032371,
        0.8143482064741907,
        0.7522309711286089,
        0.7669291338582677,
        0.7301837270341207,
        0.7130358705161854,
        1.0,
        0.7954505686789152,
        1.0,
        0.905511811023622,
        0.736482939632546, 
        0.905511811023622, 
        1.0],
    'score_test': [
        0.6435695538057743,
        0.6267716535433071,
        0.5485564304461942,
        0.6367454068241469,
        0.6341207349081365,
        0.6272965879265092,
        0.6278215223097113,
        0.6225721784776903,
        0.6157480314960629,
        0.6414698162729658,
        0.6173228346456693,
        0.5748031496062992,
        0.6215223097112861, 
        0.5748031496062992, 
        0.6178477690288714],
    'model': [
        'LogisticRegression',
        'PassiveAggressiveClassifier',
        'Perceptron',
        'RidgeClassifier',
        'SGDClassifier',
        'BernoulliNB',
        'ComplementNB',
        'GaussianNB',
        'MLPClassifier',
        'LinearSVC',
        'NuSVC',
        'ExtraTreeClassifier',
        'KNeighborsClassifier', 
        'DecisionTreeClassifier', 
        'SVC'],
    'elapsed_time': [
        270.32518315315247,
        53.37343072891235,
        26.26744818687439,
        39.60955739021301,
        555.8103160858154,
        7.185016393661499,
        5.576895713806152,
        13.337611675262451,
        20867.987093687057,
        12.668141603469849,
        3273.4229333400726,
        412.25856614112854,
        1240.0081491470337, 
        412.70804357528687, 
        4723.841665267944],
    'number_process': [
        35,
        7,
        21,
        14,
        42,
        7,
        14,
        7,
        72,
        28,
        48,
        60,
        8,
        60,
        32]}

labels = ['LR','PAC','P','RC','SGDC','BNB','CNB','GNB','MLPC','LSVC',
          'NSVC','ETC','KNC','DTC','SVC']
s = 200*np.log(
        np.array(my_models['elapsed_time'])/np.array(my_models['number_process']) 
        + 1)
c = np.arange(1,len(my_models['model'])+1)
fig, ax = plt.subplots(figsize = (12,6.5))
scatter = ax.scatter(
    x = my_models['score_test'],
    y = my_models['score_train'],
    s = s,
    c = s,
    cmap = 'viridis',
    alpha = 0.6)
ax.set_xlabel('score test')
ax.set_ylabel('score train')
ax.set_title('Train vs Test, through time')
ax.figure.colorbar(
    scatter,
    label='200*log(elapsed time/number process + 1)')
ax.grid(True, alpha = 0.5)
for label, test,train in zip(
        labels, my_models['score_test'],my_models['score_train']):
    if label == 'ETC' or label == 'SVC':
        ax.text(test, train, label, 
                rotation = -45, 
                verticalalignment='bottom',
                horizontalalignment='left')
    elif label == 'PAC':
        ax.text(test, train, label, 
                rotation = 315, 
                verticalalignment='top',
                horizontalalignment='center')
    elif label == 'LSVC':
        ax.text(test, train, label, 
                rotation = 315,
                verticalalignment='center',
                horizontalalignment='center')
    else:
        ax.text(test, train, label, 
                rotation = 45,
                verticalalignment='center',
                horizontalalignment='center')
# plt.show()
plt.savefig('points.svg')



def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(round(height,3)),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom', rotation = 90)

width = 0.35
x = np.arange(1,len(my_models['model'])+1)
y = np.linspace(0,1.2,12)

fig, ax = plt.subplots(figsize = (12,6.5))
rects1 = ax.bar(x - width/2, my_models['score_test'], width, label='Score test')
rects2 = ax.bar(x + width/2, my_models['score_train'], width, label='Score train')
ax.set_ylabel('Scores')
ax.set_title('Scores by model')
ax.set_xticks(x)
ax.set_yticks(y)
ax.set_xticklabels(labels, rotation = 90)
ax.legend(loc='upper left')
autolabel(rects1)
autolabel(rects2)
fig.tight_layout()
ax.grid(axis = 'y', alpha = 0.5)
plt.savefig('bar.svg')




