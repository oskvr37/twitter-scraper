from .api import api
from colorama import init, Fore
init(autoreset=True)


class Logger:
    def __init__(self, name) -> None:
        self.name = f'{Fore.MAGENTA}[ {name} ]'

    def info(self, msg: str):
        print(f'{self.name} {msg}')


class Photo:
    def __init__(self, url: str) -> None:
        self.url = url
        self.filename = url.split('/')[-1]


class User:
    def __init__(self, username) -> None:
        self.api = api
        self.logger = Logger('User')
        self.username = username
        self.user_id = None
        self.photos = []

    def getID(self):
        endpoint_url = (f'https://api.twitter.com/2'
                        f'/users/by/username/{self.username}')
        response = self.api.get(endpoint_url)
        if response.success:
            if 'errors' in response.data:
                errors = response.data['errors']
                for error in errors:
                    self.logger.info(f'{Fore.RED} {error["detail"]}')
                raise Exception('couldnt get id')
            else:
                self.user_id = response.data['data']['id']
                self.logger.info(f'{Fore.BLUE} created {Fore.GREEN}'
                                 f' {self.username} {Fore.BLUE}({self.user_id})')
        else:
            self.logger.info(f'{Fore.RED} request failed '
                             f'({response.request.status_code})')
            raise Exception(response.data['detail'])

    def getTweets(self, query):
        endpoint_url = f'https://api.twitter.com/2/users/{self.user_id}/tweets'
        response = self.api.get(endpoint_url + query)
        return response.data

    def collectPhotos(self, max_results=10, limit=0) -> list[Photo]:
        collected = 0
        media = []
        since_id = None
        while True:
            query = (f'?expansions=attachments.media_keys'
                     f'&media.fields=url&max_results={max_results}')

            if since_id:
                query += f'&until_id={since_id}'
            tweets = self.getTweets(query)

            count = tweets['meta']['result_count']
            collected += max_results

            if count == 0:
                break
            else:
                self.logger.info(f'{Fore.BLUE} got'
                                 f' {Fore.GREEN}{count} {Fore.BLUE}tweets')
                media.extend(tweets['includes']['media'])
                since_id = tweets['meta']['oldest_id']

            if limit != 0:
                left = limit - collected
                if left < max_results:
                    max_results = left

            if collected >= limit and limit != 0:
                break

        photos = [Photo(obj['url']) for obj in media if obj['type'] == 'photo']
        self.logger.info(f'{Fore.BLUE} collected {Fore.GREEN}'
                         f'{len(photos)} {Fore.BLUE}photos')
        self.photos = photos
        return photos
