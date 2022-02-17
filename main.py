from twitter import twitter

twitter.TOKEN = ''

username = 'elonmusk'

scrapper = twitter.Scrapper()

user = scrapper.createUser(username)

user.getPhotos(limit=5)

scrapper.downloadPhotos(user)
