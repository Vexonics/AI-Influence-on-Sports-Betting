import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_csv("data/processed/ai_posts_cleaned.csv")
documents = df["full_text"].fillna("").tolist()

embedder = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = embedder.encode(documents, show_progress_bar=True)

umap_model = UMAP(
    n_neighbors = 15,
    n_components = 5,
    min_dist = 0.0,
    metric = "cosine",
    random_state = 42,
)
reduced_embeddings = umap_model.fit_transform(embeddings)

hdbscan_model = HDBSCAN(
    min_cluster_size = 8,
    metric="euclidean",
    cluster_selection_method="eom",
)
topics = hdbscan_model.fit_predict(reduced_embeddings)

df["topic"] = topics

def get_top_keywords_per_cluster(df, text_col="full_text", topic_col="topic", n_words=10):
    cluster_texts = (
        df[df[topic_col] != -1]
        .groupby(topic_col)[text_col]
        .apply(lambda texts: " ".join(texts))
    )

    vectorizer = CountVectorizer(stop_words="english", max_features=5000)
    doc_term_matrix = vectorizer.fit_transform(cluster_texts)
    terms = vectorizer.get_feature_names_out()

    term_freq = doc_term_matrix.toarray()
    avg_freq_across_clusters = term_freq.mean(axis=0)
    scores = term_freq / (avg_freq_across_clusters + 1e-9)

    keywords = {}
    for i, topic_id in enumerate(cluster_texts.index):
        top_indices = scores[i].argsort()[::-1][:n_words]
        keywords[topic_id] = [terms[j] for j in top_indices]

    return keywords

topic_keywords = get_top_keywords_per_cluster(df)

topic_counts = df[df["topic"] != -1]["topic"].value_counts().sort_index()

print("Topic sizes:")
for topic_id, count in topic_counts.items():
    kw = ", ".join(topic_keywords.get(topic_id, []))
    print(f"  Topic {topic_id} ({count} docs): {kw}")

print(f"\nNumber of topics found (excluding outliers): {len(topic_counts)}")
print(f"Documents classified as outliers (topic -1): {(df['topic'] == -1).sum()}")

df.to_csv("data/processed/ai_posts_with_topics.csv", index=False)