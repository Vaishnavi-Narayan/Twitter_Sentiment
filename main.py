import tweepy
from textblob import TextBlob
import datetime
import csv

def main(query, size):

    # Enter your Twitter credentials below

    consumer_key = ''
    consumer_secret = ''

    access_token = ''
    access_token_secret = ''

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Authenticates with Twitter

    api = tweepy.API(auth, wait_on_rate_limit=True)

    print("Collecting tweets...")

    tweets_array = []

    # Iterates through the collected Tweets and extracts the required info before appending them to an array

    for tweet in tweepy.Cursor(api.search,
                               q=query,
                               result_type="recent",
                               lang="en").items(size):
        userid = api.get_user(tweet.user.id)
        username = userid.screen_name

        if tweet.user.location:
            location = tweet.user.location
        else:
            location = "N/A"

        tweetText = tweet.text

        length = len(tweetText)

        analysis = TextBlob(tweet.text)
        polarity = analysis.sentiment.polarity

        datestamp = tweet.created_at
        time = datestamp.strftime("%H:%M")
        year = datestamp.strftime("%d-%m-%Y")

        if ('RT @' in tweet.text):
            retweet = "Yes"
        else:
            retweet = "No"

        tweets_array.append([username, location, tweetText, retweet, time, year, length, polarity])

    print("Done!")

    return tweets_array

def save_to_csv(tweets_list):
    print('Saving to CSV')

    # Writes out the tweets array to a CSV file

    with open("Twitter_Sentiment.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=["Username", "Location", "Tweet", "Retweet", "Time", "Year", "Length", "Polarity"], delimiter='|')
        writer.writeheader()
        writer = csv.writer(f, delimiter='|')
        writer.writerows(tweets_list)


if __name__ == '__main__':
    try:
        tweets_list = main("Trump", 100)
        save_to_csv(tweets_list)

    except KeyboardInterrupt:
        print("Bye!")