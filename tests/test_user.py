import unittest
from twitter.user import User


class TestUser(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.username = 'test_scraper'
        self.user = User(self.username)
        self.user.getID()

    def test_username(self):
        self.assertEqual(self.user.username, self.username,
                         f'Should be {self.username}')

    def test_getID(self):
        self.assertEqual(self.user.user_id, '1495008493417422848',
                         "Should be 1495008493417422848")

    def test_getTweets(self):
        query = '?expansions=attachments.media_keys&media.fields=url'
        tweets = self.user.getTweets(query)
        print(tweets)
        tweet_photo_url = tweets['includes']['media'][1]['url']
        photo_url = 'https://pbs.twimg.com/media/FMDAgNgXIAoYJtn.png'
        self.assertEqual(tweet_photo_url, photo_url)


if __name__ == '__main__':
    unittest.main()
