import praw
import configparser


def word_count(stringVal):
    print("-- Running Word_count function --")
    counts = dict()
    words = stringVal.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts


config = configparser.ConfigParser()
config.read_file(open(r'auth.txt'))

# Initialize the reddit client
reddit = praw.Reddit(
    client_id=config.get('auth', 'client_id'),
    client_secret=config.get('auth', 'client_secret'),
    user_agent=config.get('auth', 'user_agent'),
)


# Set the subreddit as r/all
subreddit = reddit.subreddit("all")

# Maintain a list of comments
commentList = ""


# Iterate thru the hot posts in the subreddit with the most activity
for post in subreddit.hot(limit=10):
    print("-- Submission title :" + post.title + " --")

    # Sort comments by new to keep it fresh
    post.comment_sort = "new"

    # Remove all 'More Comments' instances to prevent AttributeError
    post.comments.replace_more(limit=0)

    # Get a list of comments (only top level not replies)
    top_level_comments = post.comments.list()

    # Concatenate into a single string
    for comment in top_level_comments:
        commentList += comment.body

# After concatenation feed to wordcount and print
print(word_count(commentList))
