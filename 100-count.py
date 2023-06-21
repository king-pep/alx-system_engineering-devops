from requests import get

REDDIT = "https://www.reddit.com/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}


def count_words(subreddit, word_list, after=None, word_dic=None):
    if word_dic is None:
        word_dic = {}

    if not word_dic:
        for word in word_list:
            word_dic[word.lower()] = 0

    if after is None:
        sorted_words = sorted(word_dic.items(), key=lambda x: (-x[1], x[0]))
        results = []
        for word, count in sorted_words:
            if count > 0:
                results.append("{}: {}".format(word, count))
        return results

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
            title = post.get("title").lower()
            for word in word_list:
                word_dic[word.lower()] += title.count(' ' + word.lower() + ' ')
    except:
        return None

    return count_words(subreddit, word_list, after, word_dic)
