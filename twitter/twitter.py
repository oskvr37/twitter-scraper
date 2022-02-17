from operator import le
from requests import get as getRequest
from os import listdir, makedirs
from wget import download
from colorama import init, Fore
init(autoreset=True)

from .threader import Threader


TOKEN = ''


def get(url):
    headers = {"Authorization": f"Bearer {TOKEN}", "content-type": "application/json"}
    request = getRequest(url, headers=headers)
    status_code = request.status_code
    data = request.json()
    if status_code == 200:
        print(f'{Fore.GREEN}{status_code} | {url}')
        return data
    else:
        print(f'{Fore.RED}{status_code} | {url}')
        return None


class Photo:
    def __init__(self, url: str) -> None:
        self.url = url
        self.filename = self.url.split('/')[-1]


class User:
    def __init__(self, username: str) -> None:
        self.username = username
        self.user_id = self.getID()
        self.photos: list[Photo] = []

    def getID(self):
        endpoint_url = f'https://api.twitter.com/2/users/by/username/{self.username}'
        data = get(endpoint_url)
        if data: return data['data']['id']
        else: return None

    def getTweets(self, token=''):
        query = f'max_results=30&expansions=attachments.media_keys&media.fields=url'
        if token: query += f'&pagination_token={token}'
        endpoint_url = f'https://api.twitter.com/2/users/{self.user_id}/tweets?{query}'
        tweets = get(endpoint_url)
        if tweets:
            result_count = tweets['meta']['result_count']
            print(f'{Fore.MAGENTA}got {result_count} tweets')
            print(tweets)
            return tweets
        else: return None

    def getPhotos(self, limit=0):
        if not self.user_id:
            return
        tweets_list = []
        next_token = ''
        while True:
            if limit != 0 and len(tweets_list) > limit: break
            tweets = self.getTweets(next_token)
            if tweets:
                try: tweets_list.extend(tweets["includes"]["media"])
                except: None
                try: next_token = tweets['meta']['next_token']
                except KeyError: break
        photos = [Photo(tweet["url"]) for tweet in tweets_list if tweet["type"] == 'photo']
        self.photos = photos[0:limit]


class Scrapper:
    def __init__(self, download_dir='downloads') -> None:
        self.users = []
        self.download_dir = download_dir

    def createUser(self, username: str):
        user = User(username)
        if user.user_id: self.users.append(user)
        return user

    def downloadPhotos(self, user: User, limit=0):
        if not user.user_id:
            return
        path = f'{self.download_dir}/{user.username}'
        try:
            makedirs(path)
            args = user.photos
        except:
            downloaded = listdir(path)
            args = [photo for photo in user.photos if photo.filename not in downloaded]

        def downloadFunction(arg: Photo):
            download(arg.url, f'{path}/{arg.filename}', None)

        if args:
            print(f'{Fore.YELLOW} downloading {len(args)} photos')
            time = Threader(10, downloadFunction, args).run()
            print(f'{Fore.GREEN} downloaded in {time} s')
