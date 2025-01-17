#!/usr/bin/env python3
# coding: utf8

"""
Class that correctly identifies the different components of a tweet and
assembles it into a dictionary to be added to a database.
"""

from textblob import TextBlob

def average(lst): 
    return sum(lst) / len(lst)

def calculate_sentiment(title):
    scores = list()
    blob = TextBlob(title)
    for sentence in blob.sentences:
        scores.append(sentence.sentiment.polarity)
    return average(scores)

class JSONTweetParser:
    """
    Class for transforming a tweet dictionary as defined by the twitter api and
    parsing it and extracting the information needed for the ornus database
    """
    def __init__(self, tweet: dict, stock: str):
        """
        :param tweet: dict object as gathered from the twitter api
        """
        self.tweet_json = tweet
        self.stock = stock

    def get_tweetid(self) -> int:
        """
        :return: the unique id of a tweet
        """
        return self.tweet_json["id"]
    
    def get_hashtags(self) -> list:
        """
        :return: a list of the hashtags of a tweet
        """
        return [tag["text"] for tag in self.tweet_json["entities"]["hashtags"]]

    def get_date(self) -> str:
        """
        :return: the date of which a tweet was posted
        """
        return JSONTweetParser.format_time(self.tweet_json["created_at"])

    def get_retweets(self) -> int:
        """Get the number of retweets for a specified tweet"""
        return self.tweet_json["retweet_count"]

    def get_tweet_sentiment(self) -> float:
        """
        returns a float from -1 to 1 indicating the sentiment of the tweet's
        body of text
        """
        return calculate_sentiment(self.get_tweet())

    def get_userinfo(self) -> dict:
        """
        :return dict containing all the different information about
        the user who made the tweet
        """
        user = {
            "date_created": JSONTweetParser.format_time(
                self.tweet_json["user"]["created_at"]
            ),
            "id": self.tweet_json["user"]["id"],
            "followers": self.tweet_json["user"]["followers_count"],
            "friends": self.tweet_json["user"]["friends_count"],
        }
        return user

    def get_tweet(self) -> str:
        """Get the content of a tweet"""
        return self.tweet_json["text"]

    def construct_tweet_json(self):
        """
        :return dict containing all the different information about
        a certain tweet
        """
        tweet = {
            "id": self.get_tweetid(),
            "text": self.get_tweet(),
            "hashtags": self.get_hashtags(),
            "date": self.get_date(),
            "retweets": self.get_retweets(),
            "user": self.get_userinfo(),
            "stock": self.stock,
            "sentiment": self.get_tweet_sentiment(),
        }
        return tweet

    @staticmethod
    def format_time(date: str, separator="-") -> str:
        """
        Takes a string in the format of: "Fri Apr 25 10:43:41 +0000 2014"
        and returns it in a format of: 2014-4-25
        :param date: time str of the format:
             WEEKDAY MONTH DAY TIME TIMEZONE YEAR
        :param separator: str that will separate the different components
            of the date, default is '-' so the date is seperated in the
            format of year-month-day
        """

        month_to_digit = {
            "Jan": "1",
            "Feb": "2",
            "Mar": "3",
            "Apr": "4",
            "May": "5",
            "Jun": "6",
            "Jul": "7",
            "Aug": "8",
            "Sep": "9",
            "Oct": "10",
            "Nov": "11",
            "Dec": "12",
        }

        _, month, day, _, _, year = date.split()
        return separator.join([year, month_to_digit[month], day])


if __name__ == "__main__":
    pass