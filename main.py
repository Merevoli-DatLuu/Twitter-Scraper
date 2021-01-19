"""
    Scraper Tool for Twitter
    Download Images and Videos
"""
import json
import os
import urllib

from colorama import Fore
from tweepy import *

screen_name = input(">>> ")

status_onwer = False
directory = os.path.expanduser('./' + screen_name)

if not os.path.exists(directory):
    os.makedirs(directory)

print(directory)

oauth_json_file = os.path.expanduser('./oauth.json')
if not os.path.exists(oauth_json_file):
    print('no ' + oauth_json_file)
    exit(1)
    
oauth = json.loads(open(oauth_json_file, 'r').read())
auth = OAuthHandler(oauth['consumer_key'], oauth['consumer_secret'])
auth.set_access_token(oauth['access_token'], oauth['access_token_secret'])
api = API(auth)

statuses = []
for status in Cursor(api.user_timeline, screen_name=screen_name).items():
    statuses.append(status)

for status in reversed(statuses):
    status_id = str(status.id)
    date = status.created_at.strftime('%Y%m%d%H%M%S')
    if (status_onwer == True and hasattr(status, 'retweeted_status')) or not hasattr(status, 'extended_entities'):
        continue
    if 'media' in status.extended_entities:
        print('http://twitter.com/' + screen_name + '/status/' + status_id) # print uri of status
        count = 0
        for media in status.extended_entities['media']:
            count += 1
            if media['type'] == 'photo':
                image_uri = media['media_url'] + ':large'
                filename = date + '-twitter.com_' + screen_name + '-' + status_id + '-' + str(count)
                file_extension = image_uri.split(":")[-2].split(".")[-1]
                filepath = directory + '/' + filename + "." + file_extension

                urllib.request.urlretrieve(image_uri, filepath)
                print("[{}] Image: {}".format(count, image_uri))

                if not os.path.exists(filepath):
                    err = filename + ": failed to download " + image_uri

            elif media['type'] == 'video':
                video_list = list(filter(lambda x: 'bitrate' in x, media['video_info']['variants']))
                max_bitrate = max(list(map(lambda x: x['bitrate'], video_list)))
                file_extension = ""
                video_url = ""

                for video in video_list:
                    if video['bitrate'] == max_bitrate:
                        video_url = video['url']
                        file_extension = video['content_type'].split("/")[-1]

                filename = date + '-twitter.com_' + screen_name + '-' + status_id + '-' + str(count)
                filepath = directory + '/' + filename + "." + file_extension

                urllib.request.urlretrieve(video_url, filepath)
                print("[{}]Video: {}".format(count, video_url))

                if not os.path.exists(filepath):
                    err = filename + ": failed to download " + video_url



