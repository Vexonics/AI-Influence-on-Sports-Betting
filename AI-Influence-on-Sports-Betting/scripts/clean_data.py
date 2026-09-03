import os
import pandas as pd
import json

with open("data/raw/posts_raw.json", "r") as f:
    posts = json.load(f)

df = pd.DataFrame(posts)

df["full_text"] = df["title"].fillna("") + " " + df["selftext"].fillna("")
df["full_text_lower"] = df["full_text"].str.lower()
keywords = "chatgpt|claude|gemini|grok| ai "
df["mentions_ai"] = df["full_text_lower"].str.contains(keywords)

ai_df = df[df["mentions_ai"]]
ai_df = ai_df[["id", "author", "title", "selftext", "created_utc", "score", "subreddit", "full_text"]]

os.makedirs("data/processed", exist_ok=True)
ai_df.to_csv("data/processed/ai_posts_cleaned.csv", index=False)

