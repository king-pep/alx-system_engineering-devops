from requests import get

REDDIT = "https://www.reddit.com/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}


def count_words(subreddit, word_list, after=None, word_dict=None):
    if word_dict is None:
        word_dict = {}

    if after is None:
        sorted_words = sorted(word_dict.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_words:
            if count > 0:
                print(f"{word.lower()}: {count}")
        return

    url = REDDIT + f"r/{subreddit}/hot/.json"

    params = {
        'limit': 100,
        'after': after
    }

    response = get(url, headers=HEADERS, params=params, allow_redirects=False)

    if response.status_code != 200:
        return

    try:
        data = response.json()
    except ValueError:
        return

    posts = data.get('data', {}).get('children', [])
    for post in posts:
        title = post.get('data', {}).get('title', '').lower()
        for word in word_list:
            count = title.count(word.lower())
            if count > 0:
                word_dict[word] = word_dict.get(word, 0) + count

    after = data.get('data', {}).get('after')
    count_words(subreddit, word_list, after, word_dict)

