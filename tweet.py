
import requests
from requests import get
import tweepy
import time 
import hashlib
import os

all_keys = open('/Users/bryant/Desktop/MCU Twitter Bot/twitterKeys.txt','r').read().splitlines() # opens txt file with api keys
IMG_SIZE = "/portrait_uncanny.jpg"
CHAR_ID = 1010445


#twitter keys
API_KEY = all_keys[0]
API_KEY_SECRET = all_keys[1]
BEAR_KEY = all_keys[2]
ACCESS_TOKEN = all_keys[3]
ACCESS_TOKEN_SECRET = all_keys[4]

#marvel private and public keys
MCU_PUB_KEY = all_keys[5]
MCU_PRI_KEY = all_keys[6]

#hash used in url
hash_value = hashlib.md5()

#timestamp
ts = str(time.time()) 

#converting to bytes
ts_byte = bytes(ts, 'utf-8')
mcu_pri_byte = bytes(MCU_PRI_KEY, 'utf-8')
mcu_pub_byte = bytes(MCU_PUB_KEY, 'utf-8')

#storing hash values
hash_value.update(ts_byte)
hash_value.update(mcu_pri_byte)
hash_value.update(mcu_pub_byte)

#converting hash values into hex
hasht = hash_value.hexdigest()

authenticator = tweepy.OAuthHandler(API_KEY,API_KEY_SECRET)
authenticator.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#base url for marvel api
BASE_URL = "https://gateway.marvel.com"

#twitter api
api = tweepy.API(authenticator, wait_on_rate_limit=True)

#api.update_status("")

#marvel api function
def make_api_url(action, objectId, **kwargs):

   url = BASE_URL +f"/v1/public/{action}/{objectId}?ts={ts}&apikey={MCU_PUB_KEY}&hash={hasht}" 

   for key, value in kwargs.items():
      url += f"/{key}"
   
   return url

#obtaining marvel character stats
def get_character(characterId):
   character_url = make_api_url("characters",characterId)
   response = get(character_url)
   data = response.json()["data"]   
   
   value = data["results"]

   for hero_data in value:
      info = hero_data

   return info


#loads character image assets
def character_img(size,characterId):
   char_img = get_character(characterId)['thumbnail']

   return char_img["path"] + size


def tweet_img(url, message):
   filename = 'portrait_uncanny.jpg'
   request = requests.get(url,stream=True)

   if request.status_code == 200:
      with open(filename, 'wb') as image:
         for chunk in request:
            image.write(chunk)

      api.update_status_with_media(status=message,  filename=filename)
      os.remove(filename)
      print("Image parsed successfully!")
   else:
      print("Image could\'t be found!")


character_today = get_character(1011435)

hero = get_character(CHAR_ID)["name"]
img = character_img(IMG_SIZE,CHAR_ID)

tweet_img(img, hero)