#!/usr/bin/python3
""" Count it! """
from requests import get

REDDIT = "https://www.reddit.com/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}


def count_words(subreddit, word_list, after="", word_dict=None):
    if word_dict is None:
        word_dict = {}

    if after is None:
        sorted_words = sorted(word_dict.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_words:
            if count > 0:
                print(f"{word.lower()}: {count}")
        return None

    url = REDDIT + "r/{}/hot/.json".format(subreddit)

    params = {
        'limit': 100,
        'after': after
    }

    r = get(url, headers=HEADERS, params=params, allow_redirects=False)

    if r.status_code != 200:
        return None

    try:
        js = r.json()
    except ValueError:
        return None

    try:
        data = js.get("data")
        after = data.get("after")
        children = data.get("children")

        for child in children:
            post = child.get("data")
            title = post.get("title")
            lower = [s.lower() for s in title.split()]

            for word in word_list:
                if word.lower() in lower:
                    word_dict[word] = word_dict.get(word, 0) + lower.count(word.lower())

    except:
        return None

    count_words(subreddit, word_list, after, word_dict)
