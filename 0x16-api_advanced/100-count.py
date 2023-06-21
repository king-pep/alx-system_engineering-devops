import requests


def count_words(subreddit, word_list, after='', word_dict=None):
    if word_dict is None:
        word_dict = {word.lower(): 0 for word in word_list}

    if after is None:
        sorted_words = sorted(word_dict.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_words:
            if count > 0:
                print(f"{word}: {count}")
        return None

    url = f"https://www.reddit.com/r/{subreddit}/hot/.json"
    headers = {'user-agent': 'redquery'}
    parameters = {'limit': 100, 'after': after}
    response = requests.get(url, headers=headers, params=parameters, allow_redirects=False)

    if response.status_code != 200:
        return None

    try:
        data = response.json()['data']
        hot = data['children']
        aft = data['after']
        for post in hot:
            title = post['data']['title']
            lower = [word.lower() for word in title.split(' ')]

            for word in word_dict:
                if word in lower:
                    word_dict[word] += lower.count(word)

    except Exception:
        return None

    count_words(subreddit, word_list, aft, word_dict)
