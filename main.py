from twitter.user import User
from twitter.downloader import Downloader

user = User('elonmusk')

user.getID()

user.collectPhotos()

Downloader().download(user)
