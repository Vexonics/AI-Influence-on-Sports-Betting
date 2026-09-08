import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

df = pd.read_csv("data/processed/ai_posts_with_topics.csv")

analyzer = SentimentIntensityAnalyzer()

def score_text(text):
    scores = analyzer.polarity_scores(str(text))
    return pd.Series([scores["neg"], scores["neu"], scores["pos"], scores["compound"]])

df[["vader_neg", "vader_neu", "vader_pos", "vader_compound"]] = df["full_text"].apply(score_text)

def classify_sentiment(compound):
    if compound >= 0.05:
        return "positive"
    elif compound <= -0.05:
        return "negative"
    else:
        return "neutral"

df["vader_label"] = df["vader_compound"].apply(classify_sentiment)

print("Overall sentiment distribution:")
print(df["vader_label"].value_counts())

print("\nAverage compound sentiment by topic:")
print(df.groupby("topic")["vader_compound"].mean().sort_values())

print("\nSentiment label counts by topic:")
print(df.groupby("topic")["vader_label"].value_counts())

df.to_csv("data/processed/ai_posts_with_topics_and_sentiment.csv", index=False)