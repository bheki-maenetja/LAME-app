# Third-Party Imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

import plotly.graph_objects as go

import pandas as pd
import nltk

# Standard Imports
from string import punctuation

# Local Imports

# Helper Functions
def word_tokenize(text, lower_case=False):
    banned = list(punctuation) + nltk.corpus.stopwords.words("english")
    
    if lower_case:
        return [
        w.lower() for w in nltk.word_tokenize(text) 
        if w.lower() not in banned
    ]
    
    return [
        w for w in nltk.word_tokenize(text) 
        if w.lower() not in banned
    ]

# Plotting Functions
def plot_data(x=None, y=None, z=None, title="", x_label="", y_label="", name="", mode="markers", text="", **traces):
    fig = go.Figure(layout={
        "title": title,
        "xaxis": {"title": x_label},
        "yaxis": {"title": y_label}
    })
    
    if z is None:
        data = go.Scatter(
            x=x,
            y=y,
            mode=mode,
            name=name,
            text=text
        )
    else:
        data = go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode=mode,
            name=name,
            text=text
        )

    if x is not None and y is not None:
        fig.add_trace(data)
    
    for t in traces:
        fig.add_trace(traces[t])
    
    return fig

def create_trace(x=None, y=None, z=None, name="", mode="lines", text="", marker_size=None):
    if z is None:
        trace = go.Scatter(
            x=x,
            y=y,
            mode=mode,
            name=name,
            text=text,
            marker=dict(size=marker_size)
        )
    else:
        trace = go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode=mode,
            name=name,
            text=text,
            marker=dict(size=marker_size)
        )
    
    return trace

# Clustering Documents
def doc_clustering(corpus, num_clusters=2):
    # Get original documents
    docs = list(corpus.items())
    
    # Preprocess documents
    processed_docs = [
        ' '.join(word_tokenize(doc[1])) 
        for doc in docs
    ]
    
    # Extract features from documents
    vectoriser = TfidfVectorizer()
    X = vectoriser.fit_transform(processed_docs)
    
    # Cluster documents
    kmeans = KMeans(n_clusters=num_clusters, init="random", max_iter=2000)
    kmeans.fit(X)
    
    # Principal components
    min_x = min(X.shape)
    num_comps = min(min_x, 3)

    pca = PCA(n_components=num_comps)
    prin_comps = pca.fit_transform(X.toarray())
    
    # Identify Themes
    cluster_data = {
        "name": [],
        "themes": []
    }
    
    for i in range(num_clusters):
        centroid = kmeans.cluster_centers_[i]
        top_words_idx = centroid.argsort()[::-1][:5]
        top_words = [
            vectoriser.get_feature_names_out()[idx] 
            for idx in top_words_idx
        ]
        cluster_data["name"].append(i)
        cluster_data["themes"].append(" ".join(top_words))
    
    centroid_comps = pca.fit_transform(kmeans.cluster_centers_)
    
    cluster_data["x_coord"] = centroid_comps[:, 0]
    cluster_data["y_coord"] = centroid_comps[:, 1]
    if num_comps > 2: cluster_data["z_coord"] = centroid_comps[:, 2]
    
    doc_data = {
        "doc_name": [doc[0] for doc in docs],
        "x_coord": prin_comps[:, 0],
        "y_coord": prin_comps[:, 1],
        "cluster": kmeans.labels_
    }
    if num_comps > 2:
        doc_data.update({"z_coord": prin_comps[:, 2]})
    
    return pd.DataFrame.from_dict(cluster_data), pd.DataFrame.from_dict(doc_data)

def plot_clusters(doc_data, cluster_data, is_3d=True):
    traces = dict()

    for i, theme in enumerate(cluster_data['themes']):
        cluster_name = f"Cluster {i+1}: {theme}"
        cluster_points = doc_data[doc_data['cluster'] == i]
        
        z = cluster_points['z_coord'] if is_3d else None
        
        new_trace = create_trace(
            x=cluster_points['x_coord'],
            y=cluster_points['y_coord'],
            z=z,
            name=cluster_name,
            mode="markers",
            text=cluster_points['doc_name'],
            marker_size=5
        )
        traces[cluster_name] = new_trace
    
    return plot_data(**traces)