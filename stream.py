import json
import psycopg2
import sqlite3
import tweepy


class Listener(tweepy.StreamListener):
    def insert(self, row):
        print('inserting something')
        conn = psycopg2.connect(dbname="tweets", user="postgres", password="postgres")
        cur = conn.cursor()
        cur.execute('INSERT into incidents (id, content, image, date) VALUES (%s, %s, %s, %s)', row)
        conn.commit()
        cur.close()
        conn.close()

    def on_status(self, status):
        # only counts if the handle was mentioned
        mentions = status.entities['user_mentions']
        if mentions and mentions[0]['screen_name'] == "realDonaldTrump":
            id_ = status.id
            date = status.created_at
            text = status.text
            media = status.entities.get('media')
            image = media[0].get('media_url') if media else None
            self.insert([id_, text, image, date])

    def on_error(self, status):
        print(status)


def main():
    with open('keys.json') as f:
      keys = json.load(f)

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(keys['api_key'], keys['api_key_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])

    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)

    # Stream mentions and parse to db
    stream = tweepy.Stream(auth = api.auth, listener=Listener())
    stream.filter(track=['the'])
