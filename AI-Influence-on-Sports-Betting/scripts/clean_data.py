import os
import re
import pandas as pd
import json

with open("data/raw/posts_raw.json", "r") as f:
    posts = json.load(f)

df = pd.DataFrame(posts)

df["full_text"] = df["title"].fillna("") + " " + df["selftext"].fillna("")

def clean_text(text):
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = re.sub(r"n't\b", " not", text)
    text = re.sub(r"'s\b", "", text)
    text = re.sub(r"'re\b", " are", text)
    text = re.sub(r"'ve\b", " have", text)
    text = re.sub(r"'ll\b", " will", text)
    text = re.sub(r"'d\b", " would", text)
    text = re.sub(r"'m\b", " am", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["full_text"] = df["full_text"].apply(clean_text)
df["full_text_lower"] = df["full_text"].str.lower()
keywords = "chatgpt|claude|gemini|grok| ai "
df["mentions_ai"] = df["full_text_lower"].str.contains(keywords)

ai_df = df[df["mentions_ai"]]
ai_df = ai_df[["id", "author", "title", "selftext", "created_utc", "score", "subreddit", "full_text"]]

os.makedirs("data/processed", exist_ok=True)
ai_df.to_csv("data/processed/ai_posts_cleaned.csv", index=False)