# twitter-scraper
twitter scraper allows to download user's every photo

# basic usage

```python
from twitter import twitter

twitter.TOKEN = '' # put your twitter bearer token here

username = 'elonmusk'

scrapper = twitter.Scrapper() # create scrapper

user = scrapper.createUser(username) # create user

user.getPhotos(limit=5) # get user photos from newest with limit of 5 tweets

scrapper.downloadPhotos(user) # download photos into user directory
```

# disclaimer
it's not working in 100% for users who has got more than 100 media tweets (TODO 1.)

# TODO
- instead of using tokens for scraping tweets - use since_id (https://developer.twitter.com/en/docs/twitter-api/pagination)
- create better tweets limit
- add venv for user token
- better messages logging
