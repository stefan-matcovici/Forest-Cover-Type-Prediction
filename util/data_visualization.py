from ggplot import *
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap.umap_ as umap
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import learning_curve
from sklearn.metrics import confusion_matrix


def pca_visualization(data, target, color=None):
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(data)

    data_copy = data.copy()

    data_copy['pca-one'] = pca_result[:, 0]
    data_copy['pca-two'] = pca_result[:, 1]
    if color:
        data_copy[target] = color

    'Explained variation per principal component: {}'.format(pca.explained_variance_ratio_)

    chart = ggplot(data_copy, aes(x='pca-one', y='pca-two', color=target)) \
            + geom_point(size=75, alpha=0.8) \
            + ggtitle("First and Second Principal Components colored by digit")
    return chart


def tsne_visualization(data, target, color=None):
    tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
    tsne_results = tsne.fit_transform(data)

    df_tsne = data.copy()
    df_tsne['x-tsne'] = tsne_results[:, 0]
    df_tsne['y-tsne'] = tsne_results[:, 1]
    if color:
        df_tsne[target] = color

    chart = ggplot(df_tsne, aes(x='x-tsne', y='y-tsne', color=target)) \
            + geom_point(size=70, alpha=0.1) \
            + ggtitle("tSNE dimensions colored by digit")
    return chart


def umap_visualization(data, target, color=None):
    reducer = umap.UMAP()
    embedding = reducer.fit_transform(data)

    color_column = data[target] if not color else color

    plt.figure(figsize=(40, 30), dpi=80)
    plt.scatter(embedding[:, 0], embedding[:, 1], c=[sns.color_palette()[x] for x in color_column])
    plt.gca().set_aspect('equal', 'datalim')
    plt.title('UMAP projection of the Cover Type dataset', fontsize=24)
    
def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=None, train_sizes=np.linspace(.1, 1.0, 5)):
    plt.figure(figsize=(30, 15))
    plt.title(title, fontsize=30)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples", fontsize=25)
    plt.ylabel("Score", fontsize=25)
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best", prop={'size': 25})
    plt.tick_params(labelsize=20)
    
    return plt

def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    cm = confusion_matrix(y_true, y_pred)

    fig, ax = plt.subplots(figsize=(40, 40))
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, 
           yticklabels=classes)
    ax.set_title(title, fontsize=50)
    ax.set_ylabel('True label', fontsize=30)
    ax.set_xlabel('Predicted label', fontsize=30)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    plt.tick_params(labelsize=20)

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center", fontsize=25,
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax
    
