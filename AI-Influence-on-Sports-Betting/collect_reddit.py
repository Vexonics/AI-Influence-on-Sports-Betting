import requests
import json
import os
import time

SUBREDDIT = "sportsbetting"

START_DATE = "2024-01-01"
END_DATE = "2025-01-01"

BATCH_SIZE = 100

OUTPUT_DIR = "data/raw"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "sportsbetting_posts_2024.json")

BASE_URL = "https://arctic-shift.photon-reddit.com/api/posts/search"

os.makedirs(OUTPUT_DIR, exist_ok=True)

all_posts = []
after = START_DATE

print(f"Downloading r/{SUBREDDIT}")
print(f"Date range: {START_DATE} → {END_DATE}")
print()

while True:

    params = {
        "subreddit": SUBREDDIT,
        "after": after,
        "before": END_DATE,
        "sort": "asc",
        "limit": BATCH_SIZE
    }

    print(f"Requesting posts after {after}...")

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=60
        )

        print("Status:", response.status_code)

        if response.status_code != 200:
            print("Error:", response.text)
            break

        data = response.json().get("data", [])

        if not data:
            print("No more posts found.")
            break

        print(f"Received {len(data)} posts.")

        all_posts.extend(data)

        newest_timestamp = max(
            post["created_utc"]
            for post in data
            if post.get("created_utc")
        )

        after = str(newest_timestamp + 1)

        print(f"Total collected: {len(all_posts)}")
        print()

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(all_posts, f, ensure_ascii=False, indent=2)

        time.sleep(1)

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        print("Waiting 5 seconds before retrying...")
        time.sleep(5)

print()
print("=" * 50)
print("DOWNLOAD COMPLETE")
print("=" * 50)

print("Total posts:", len(all_posts))
print("Saved to:", OUTPUT_FILE)