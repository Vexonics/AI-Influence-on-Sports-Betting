# AI Influence on Sports Betting

## Overview

This project analyzes how AI tools are discussed in the r/sportsbetting Reddit community. Posts were collected via the Arctic Shift API, filtered for AI mentions, topic-modeled, scored for sentiment using VADER, and manually thematically coded.

## Data Collection

Posts from r/sportsbetting were collected using the Arctic Shift API (`collect_data.py`), which requires no authentication. Posts mentioning AI tools (ChatGPT, Claude, Gemini, Grok, or the standalone term "AI") were filtered into a working dataset for analysis.

## Text Cleaning and a Data Quality Issue

Raw post text was normalized before filtering: curly apostrophes were standardized, common contractions were expanded (e.g., "don't" → "do not"), and remaining punctuation was stripped.

This normalization step introduced an unintended bug: the contraction-expansion regex, written to catch patterns like `n't`, also matched "ain't," expanding it to "ai not." Because the AI-mention filter checked for the standalone token "ai," this generated false positives — posts using the slang term "ain't" (e.g., "this shit ain't hittin'") were incorrectly flagged as AI-related.

This was caught during manual review of topic clusters, when one cluster's most representative posts turned out to be about missed parlays rather than AI. A content-based filter (`filter_false_positives.py`) was used to identify and remove posts matching the "ai not" artifact pattern that did not also reference a real AI tool or brand name. This removed 36 posts (roughly 19% of the pre-filter dataset), leaving a final dataset of 155 verified AI-mention posts.

## Topic Modeling

Initial topic modeling used BERTopic. BERTopic's wrapper class crashed reliably in this environment, despite each of its underlying components — sentence-transformers, UMAP, and HDBSCAN — running successfully when tested independently. This was confirmed through isolated component testing rather than assumed.

Given this environment-specific incompatibility, a manual topic modeling pipeline was built directly from BERTopic's underlying components:

1. **Embedding**: Post text was embedded using `sentence-transformers` (`all-MiniLM-L6-v2`).
2. **Dimensionality reduction**: Embeddings were reduced with UMAP (`n_neighbors=15`, `n_components=5`, cosine metric).
3. **Clustering**: HDBSCAN (`min_cluster_size=8`, Euclidean metric) was used to cluster the reduced embeddings.
4. **Keyword extraction**: For each cluster, representative keywords were identified using a class-based term-frequency approach — scoring words by how much more frequently they appeared in one cluster relative to the average across all clusters, replicating the intent of BERTopic's built-in c-TF-IDF method.

On the final 155-post dataset, this pipeline identified 2 topics:

- **Topic 0** (12 posts): MLB statistics discussion (keywords: gb, bay, ops, era, pitching, preseason)
- **Topic 1** (135 posts): AI betting tools and predictions (keywords: tool, app, predictions, built, live, world cup)

8 posts were classified as outliers (not assigned to either topic).

## Sentiment Analysis

Sentiment was scored using VADER (`vaderSentiment`) on the cleaned post text, producing a compound sentiment score and a positive/neutral/negative label for each post.

## Manual Thematic Coding

To go beyond automated topic clusters, a stratified sample of 43 posts from Topic 1 (the large AI-tools/predictions cluster) was manually read and coded into themes, sampling roughly evenly across positive, neutral, and negative sentiment labels to avoid over-representing any one sentiment category.

Four themes emerged:

- **Builder/self-promotion** (~21 posts, the dominant theme): Users sharing an AI tool or prediction model they built themselves, typically seeking feedback, beta testers, or engagement (e.g., "I built an AI horse racing tool," "Looking for a few serious bettors who would be interested in beta testing").
- **Consumer use** (~16 posts): Users describing their own use of someone else's AI tool or prediction to inform bets (e.g., "asked ChatGPT which MLB teams will go under," "using AI suggestion" for pick selection).
- **Skepticism/criticism** (~4 posts): Posts expressing distrust or frustration toward AI-driven predictions or tools, often centered on perceived unfairness or unreliability rather than technical shortcomings (e.g., accusations that outcomes were "rigged," a tool labeled "FRAUD," a post questioning whether match outcomes were suspiciously scripted "or is AI psychic").
- **Balanced/reflective takes** (~1-2 posts): A small number of posts offered a more measured view of AI's role, distinguishing what it is and is not useful for (e.g., one post explicitly argued AI is valuable for research and cross-referencing information quickly, but not for generating picks outright, since it "can't reason about which factors actually caused a result versus just correlated with it").

## Findings

Sentiment toward AI in sports betting discussion on r/sportsbetting was predominantly positive:

| Sentiment | Count |
|---|---|
| Positive | 106 |
| Neutral | 33 |
| Negative | 16 |

Average compound sentiment by topic:

| Topic | Avg. Compound Score | N |
|---|---|---|
| Topic 0 (MLB stats) | 0.65 | 12 |
| Topic 1 (AI tools/predictions) | 0.39 | 135 |
| Outliers | 0.37 | 8 |

Both identified topics skewed positive, with the small MLB-stats-adjacent cluster showing the strongest positive sentiment. The larger AI-tools/predictions cluster, while still net positive, showed more spread across sentiment categories (91 positive, 31 neutral, 13 negative).

Manual thematic coding suggests this positive skew is largely explained by *who is posting*: Topic 1 is dominated by builders promoting their own AI tools and soliciting feedback, which is inherently upbeat in tone, rather than by broad community consensus that AI is effective for betting. Genuine skepticism exists but is a minority voice, and it centers on trust and legitimacy concerns (accusations of rigged or fraudulent tools) rather than on AI's technical capability.

## Limitations

- The dataset is limited to a single subreddit (r/sportsbetting) and a specific AI-mention keyword filter, which may not capture all AI-related discussion.
- The "ain't" text-cleaning artifact demonstrates that keyword-based filtering on normalized text is sensitive to regex side effects; while this instance was caught and corrected, similar undetected artifacts may remain.
- Topic modeling produced only 2 clusters plus outliers; the larger cluster (Topic 1) is broad and required manual thematic coding to meaningfully subdivide.
- Manual thematic coding was performed on a 43-post sample of Topic 1 rather than all 135 posts, given time constraints; theme proportions are estimates, not exhaustive counts.
- VADER is a lexicon-based sentiment tool and does not capture sarcasm, sports betting slang nuance, or context-dependent meaning as reliably as more sophisticated sentiment models.
