# Reddit Lookout Bot
This is a very simple script for a Reddit Bot, which will constantly monitor all submissions and comments in 
user defined subreddits. If any user defined keywords occur in the post/comment the contents along with other information
of the post/comment gets saved to a [YAML](https://yaml.org/) file.

I personally use the script to save threads about internships or job interviews in relevant subreddits, but I think it will also be helpful for people who are completely new to the reddit API. 

## Installation
- [python 3.x](https://www.python.org/)
- [PyYAML](https://pypi.org/project/PyYAML/) 
- [PRAW](https://praw.readthedocs.io/en/stable/getting_started/installation.html)

All packages can be easily installed with `pip`

## Usage
To use the bot, you first have to generate a Client ID and Cleint Secret. I recommand making a new reddit account and follow the steps outlined 
[here](https://www.integromat.com/en/help/app/reddit) under the point _Generating your own Client ID and Client Secret values_
(you do not have to do anything with *Integromat*, only follow the steps until you have access to your Client ID and Client Secret).

Afterwards you can edit the `config.yaml` file, to personalize the bot.

You start the bot by simply running:
```bash
python LookupBot.py
```
The scirpt will run forever until you stop it with `ctrl+c`. 
I have it running all the time on my [Raspberry Pi](https://www.raspberrypi.org/).

## Output
A YAML-file with information about posts/comments containing the keyword. 
It might look something like this:

```bash
Submission - 02:17:45 22.09.21:
- Subreddit: datascience
- Title: McKinsey Tech Intern Test help | Summer 2022
- Submission_text: "I want to put in all my efforts and do as best as I can. So, wish me luck!"
- Link: https://www.reddit.com/r/datascience/comments/psxsuc/mckinsey_tech_intern_test_help_summer_2022/

Comment - 11:56:10 22.09.21:
- Subreddit: datascience
- Title: Annual raises- is there a typical percentage?
- Submission_text: 'So last year I got an approx 3% raise working at a Financial Services
    firm. I’m on an analytics team at one of the large non Wall-Street companies.
    My dept is not a revenue center but we met and exceeded our goals and the company
    did well too.
    Is there an expected industry standard for raises and if so where would I find
    it?'
- Comment_text: It seems like if you are able to do this you are low-balling your entry-level
    people. I’m not judging since it’s your business and you have to run it the way
    you see fit. But I don’t see how it’s otherwise sustainable if you also do bonuses
    and promotions.
- Link: https://www.reddit.com/r/datascience/comments/pso5p6/annual_raises_is_there_a_typical_percentage/hdu11wy/
```