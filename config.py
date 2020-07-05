import os

class Config(object):
 SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xa9\x0cD\xb6\xf2\x94(\x91\x93w\xd8\xd9\xb0\xfd\xd5Z'
 


