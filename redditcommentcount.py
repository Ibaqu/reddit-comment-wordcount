import praw
from pyspark import SparkContext, SparkConf
from time import time, sleep
from datetime import datetime

# Create Spark context with necessary configuration
sc = SparkContext("local", "Reddit comment count")

# Initialize the reddit client
reddit = praw.Reddit(
    client_id="client_id",
    client_secret="client_secret",
    user_agent="user_agent",
)

# Set the subreddit as r/all
subreddit = reddit.subreddit("all")

while True:

    print("-- Opening Input text file --")
    # Create an input file to store the data
    inputFile = open('input.txt', 'a')

    # Iterate thru the hot posts in the subreddit with the most activity
    for post in subreddit.hot(limit=10):
        print("-- Submission title :" + post.title + " --")

        # Sort comments by new to keep it fresh
        post.comment_sort = "new"

        # Remove all 'More Comments' instances to prevent AttributeError
        post.comments.replace_more(limit=0)

        # Get a list of comments (only top level not replies)
        top_level_comments = post.comments.list()

        # Write each comment body to the file
        for comment in top_level_comments:
            inputFile.write(comment.body)

    # Read data from the input file
    words = sc.textFile("input.txt").flatMap(lambda line: line.split(" "))

    # Count the occurrence of each word
    wordCounts = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

    # Save the counts to output
    wordCounts.saveAsTextFile("./output" + datetime.now().strftime("%H%M%S"))  # pass s3 location

    # Remove contents of input file
    inputFile.truncate(0)

    print("-- Sleeping for 120 seconds --")
    sleep(120)
