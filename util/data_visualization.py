from ggplot import *
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap.umap_ as umap
import seaborn as sns
import matplotlib.pyplot as plt


def pca_visualization(data, target):
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(data)

    data_copy = data.copy()

    data_copy['pca-one'] = pca_result[:, 0]
    data_copy['pca-two'] = pca_result[:, 1]

    'Explained variation per principal component: {}'.format(pca.explained_variance_ratio_)

    chart = ggplot(data_copy, aes(x='pca-one', y='pca-two', color=target)) \
            + geom_point(size=75, alpha=0.8) \
            + ggtitle("First and Second Principal Components colored by digit")
    return chart


def tsne_visualization(data, target):
    tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
    tsne_results = tsne.fit_transform(data)

    df_tsne = data.copy()
    df_tsne['x-tsne'] = tsne_results[:, 0]
    df_tsne['y-tsne'] = tsne_results[:, 1]

    chart = ggplot(df_tsne, aes(x='x-tsne', y='y-tsne', color=target)) \
            + geom_point(size=70, alpha=0.1) \
            + ggtitle("tSNE dimensions colored by digit")
    return chart


def umap_visualization(data, target):
    reducer = umap.UMAP()
    embedding = reducer.fit_transform(data)

    plt.figure(figsize=(40, 30), dpi=80)
    plt.scatter(embedding[:, 0], embedding[:, 1], c=[sns.color_palette()[x] for x in data[target]])
    plt.gca().set_aspect('equal', 'datalim')
    plt.title('UMAP projection of the Iris dataset', fontsize=24)
