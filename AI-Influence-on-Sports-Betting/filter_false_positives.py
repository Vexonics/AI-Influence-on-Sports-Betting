import pandas as pd

df = pd.read_csv("data/processed/ai_posts_with_topics_and_sentiment.csv")

before = len(df)

aint_pattern = r"\bai not\b"
is_aint_artifact = df["full_text"].str.contains(aint_pattern, case=False, na=False)

genuinely_ai_pattern = r"\b(chatgpt|claude|gemini|grok|prompt|VictoryVaultPro)\b"
mentions_real_ai = df["full_text"].str.contains(genuinely_ai_pattern, case=False, na=False)

false_positive_mask = is_aint_artifact & ~mentions_real_ai

print(f"Flagged {false_positive_mask.sum()} 'ain't' false-positive posts")
print(df.loc[false_positive_mask, "full_text"].to_string())

df_clean = df[~false_positive_mask].copy()
df_clean.to_csv("data/processed/ai_posts_final.csv", index=False)
print(f"\nFinal dataset size: {len(df_clean)} (was {before})")
