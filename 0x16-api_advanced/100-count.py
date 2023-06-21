import requests

REDDIT_URL = "https://www.reddit.com/"


def count_words(subreddit, word_list, after=None, word_counts=None):
    if word_counts is None:
        word_counts = {}

    if after is None:
        sorted_words = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))
        results = []
        for word, count in sorted_words:
            if count > 0:
                results.append("{}: {}".format(word, count))
        return results

    url = REDDIT_URL + "r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'Mozilla/5.0'}

    params = {
        'limit': 100,
        'after': after
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return None

    try:
        data = response.json()
    except ValueError:
        return None

    try:
        after = data['data']['after']
        children = data['data']['children']
        count_keywords_in_titles(children, word_list, word_counts)
    except KeyError:
        return None

    return count_words(subreddit, word_list, after, word_counts)


def count_keywords_in_titles(children, word_list, word_counts):
    for child in children:
        post = child['data']
        title = post['title']
        lowercase_title = title.lower()
        count_keywords(lowercase_title, word_list, word_counts)


def count_keywords(title, word_list, word_counts):
    for word in word_list:
        lowercase_word = word.lower()
        count = title.count(lowercase_word)
        if count > 0:
            word_counts[lowercase_word] = word_counts.get(lowercase_word, 0) + count
