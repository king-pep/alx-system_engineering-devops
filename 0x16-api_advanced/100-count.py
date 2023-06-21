import requests

REDDIT_URL = "https://www.reddit.com/"


def count_words(subreddit, word_list, after=None, word_dict=None):
    if word_dict is None:
        word_dict = {}

    if after is None:
        sorted_words = sorted(word_dict.items(), key=lambda x: (-x[1], x[0]))
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
        for child in children:
            post = child['data']
            title = post['title']
            for word in word_list:
                lowercase_word = word.lower()
                lowercase_title = title.lower()
                if (' ' + lowercase_word + ' ') in (' ' + lowercase_title + ' '):
                    word_dict[lowercase_word] = word_dict.get(lowercase_word, 0) + 1
    except KeyError:
        return None

    return count_words(subreddit, word_list, after, word_dict)

