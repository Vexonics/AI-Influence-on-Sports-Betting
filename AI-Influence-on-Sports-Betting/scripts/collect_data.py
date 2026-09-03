import requests
import json
import time
import os

base_url = "https://arctic-shift.photon-reddit.com/api/posts/search"
subreddit = "sportsbetting"
batch_limit = 100
total_posts_wanted = 20000
output_path = "data/raw/posts_raw.json"

def fetch_batch(before=None):
    params = {
        "subreddit": subreddit,
        "limit": batch_limit,
    }
    if before is not None:
        params["before"] = before

    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["data"]

def collect_posts():
    all_posts = []
    before = None

    while len(all_posts) < total_posts_wanted:
        batch = fetch_batch(before=before)

        if not batch:
            print("No more posts returned - stopping.")
            break

        all_posts.extend(batch)
        print(f"Collected {len(all_posts)} posts so far...")

        oldest_time = min(batch, key=lambda post: post["created_utc"])["created_utc"]
        before = oldest_time

        time.sleep(1)

    return all_posts

def save_posts(posts):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(posts, f)
    print(f"Saved {len(posts)} posts to {output_path}")

if __name__ == "__main__":
    posts = collect_posts()
    save_posts(posts)