# twitter-scraper
twitter scraper allows to download user's every photo

# basic usage

```python
from twitter.user import User
from twitter.downloader import Downloader

user = User('elonmusk')  # create user

user.getID() # get user id for endpoint calls

user.collectPhotos() # get all user photos

Downloader().download(user)  # download photos into user directory
```

# environment variables
set you environment variable "TWITTER_TOKEN" to your token for it to work
or go into [config file](twitter/config.py) and paste token there