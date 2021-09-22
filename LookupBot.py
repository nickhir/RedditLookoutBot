import praw
import time
import yaml
from datetime import datetime
import sys
import threading


def submissions_and_comments(subreddit, **kwargs):
    # monitor both comments and submissions simultaneously
    results = []
    results.extend(subreddit.new(**kwargs))
    results.extend(subreddit.comments(**kwargs))
    results.sort(key=lambda post: post.created_utc, reverse=True)
    return results


def save_entry(dictonary, yaml_file_path):
    # sys.stdout.write(f"Found a post/comment that contains one of the Keywords. Saving it to file {yaml_file_path}")
    # safe the found entry to your yaml file right away
    with open(yaml_file_path, 'r', encoding="utf-8") as yamlfile:
        cur_yaml = yaml.safe_load(yamlfile) or {}  # if it is empty load an empty dict
        cur_yaml.update(dictonary)

    with open(yaml_file_path, 'w', encoding="utf-8") as yamlfile:
        yaml.safe_dump(cur_yaml, yamlfile, sort_keys=False, allow_unicode=True)

    time.sleep(2)


def get_comment_info(comment):
    # get information about the submission to which the comment was made
    commented_submission = comment.submission
    submission_title = commented_submission.title.strip()
    submission_text = commented_submission.selftext.strip()

    # get basic information about the subreddit. Useful if you monitor several subreddits simuntaniously
    commented_subreddit = comment.subreddit
    subreddit_name = commented_subreddit.display_name

    permalink = f"https://www.reddit.com{comment.permalink}"

    body = comment.body

    # get creation date and translate it into human readable format
    created = comment.created_utc
    created_berlin = datetime.utcfromtimestamp(created).strftime('%H:%M:%S %d.%m.%y')
    yaml_dict = {f"Comment - {created_berlin}": [
        {"Subreddit": subreddit_name},
        {"Title": submission_title},
        {"Submission_text": submission_text},
        {"Comment_text": body},
        {"Link": permalink}
    ]}

    save_entry(yaml_dict, yaml_file_path=config["output_file"])


def get_submission_info(submission):
    # get information about the submission to which the comment was made
    submission_title = submission.title.strip()
    submission_text = submission.selftext.strip()

    # get basic information about the subreddit. Useful if you monitor several subreddits simuntaniously
    commented_subreddit = submission.subreddit
    subreddit_name = commented_subreddit.display_name

    permalink = f"https://www.reddit.com{submission.permalink}"

    # get creation date and translate it into human readable format
    created = submission.created_utc
    created_berlin = datetime.utcfromtimestamp(created).strftime('%H:%M:%S %d.%m.%y')
    yaml_dict = {f"Submission - {created_berlin}": [
        {"Subreddit": subreddit_name},
        {"Title": submission_title},
        {"Submission_text": submission_text},
        {"Link": permalink}
    ]}
    save_entry(yaml_dict, yaml_file_path=config["output_file"])


def running_animation():
    chars = r"|/-\\"
    while True:
        for char in chars:
            sys.stdout.write('\r' + 'Bot is running ...' + char)
            time.sleep(.5)
            sys.stdout.flush()


with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

reddit = praw.Reddit(
    client_id=config["client_id"],
    client_secret=config["client_secret"],
    user_agent="<console:LOOKUPBOT:1.0>"
)

# keywords you want to look for
keywords = config["keywords"]

# the subreddits which you want to monitor
subreddits = config["subreddits"]

subreddit = reddit.subreddit("+".join(subreddits))

stream = praw.models.util.stream_generator(
    lambda **kwargs: submissions_and_comments(subreddit, **kwargs))

sys.stdout.write("Bot is starting")

animation_process = threading.Thread(target=running_animation, daemon=True)
animation_process.start()

try:
    for i, element in enumerate(stream):
        if isinstance(element, praw.models.reddit.comment.Comment):
            # sometimes even comments have no body, so to double check:
            if hasattr(element, "body"):
                body = element.body.lower()

                # check if any of our keywords occure
                for key in keywords:
                    if key in body:
                        get_comment_info(element)
                        break


        elif isinstance(element, praw.models.reddit.submission.Submission):
            if hasattr(element, "title"):
                title = element.title.lower()

                # check if any of our keywords occure
                for key in keywords:
                    if key in title:
                        get_submission_info(element)
                        break

            elif hasattr(element, "selftext"):
                selftext = element.selftext.lower()

                # check if any of our keywords occure
                for key in keywords:
                    if key in selftext:
                        get_submission_info(element)
                        break

        # the first 200 posts are available instantly. All other submissions/comments get evaluated when they are posted.
        if i + 1 > 200:
            # we dont have to check all the time
            time.sleep(1)

except KeyboardInterrupt:
    sys.stdout.write("Stopping Bot")
    exit()
