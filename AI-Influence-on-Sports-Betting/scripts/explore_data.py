import pandas as pd
import json

with open("data/raw/posts_raw.json", "r") as f:
    posts = json.load(f)

df = pd.DataFrame(posts)

print(df.shape)
print(df["created_utc"].min())
print(df["created_utc"].max())
print((df["selftext"] == "").sum())

df["full_text"] = df["title"].fillna("") + " " + df["selftext"].fillna("")
df["full_text_lower"] = df["full_text"].str.lower()
keywords = "chatgpt|claude|gemini|grok| ai "
df["mentions_ai"] = df["full_text_lower"].str.contains(keywords)

print(df["mentions_ai"].sum())