import requests

base_url = "https://arctic-shift.photon-reddit.com/api/posts/search"
params = {
    "subreddit": "sportsbetting",
    "limit": 100,
    "before": 1783541787,
}

response = requests.get(base_url, params=params)
print(response.status_code)
print(response.text)