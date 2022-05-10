
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/comis)](https://pypi.python.org/pypi/comis)
[![PyPI version](https://badge.fury.io/py/comis.svg)](https://badge.fury.io/py/comis)
[![Documentation Status](https://readthedocs.org/projects/comis/badge/?version=latest)](https://comis.readthedocs.io/en/latest/?badge=latest)

# comis #
*The simplest way to create a Reddit bot*

---

## Installation
Comis can be installed with [pip](https://pip.pypa.io/en/stable/installation) or any other package manager such as [poetry](https://python-poetry.org/docs/basic-usage/#installing-dependencies) and [pipenv](https://pipenv.pypa.io/en/latest/install/#installing-packages-for-your-project).
```sh
pip install comis
```

---

## Usage

Comis makes it easy to create a bot. 
For example, the bot below pins all posts flair with `[Mod Post]` 
and posted by a moderator, while removing all posts that a not moderator posted with the flair `[Mod Post]`.

With Comis:
```python
from comis import Client, submission
from comis.filters import flair, author

class MyBot(Client):
    @author(mod=True)
    @flair(text='[Mod Post]')
    @submission()
    async def pin_mod_post(self, post, mod):
        await mod.distinguish(sticky=True)
        
    @author(mod=False)
    @flair(text='[Mod Post]')
    @submission()
    async def remove_non_mod_post(self, post, mod):
        await mod.remove()

MyBot(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="comis reddit bot by /u/YOUR_USERNAME",
    username="USERNAME",
    password="PASSWORD",
    subreddits=["your_subreddit"],
).run()

```

Same bot Without Comis:
```python

from asyncio import run
from asyncpraw import Reddit

async def main():
    subreddits = [...]
    
    reddit = Reddit(
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_CLIENT_SECRET",
        user_agent="comis reddit bot by /u/YOUR_USERNAME",
        username="USERNAME",
        password="PASSWORD",
    )

    subreddit = reddit.subreddit('+'.join(subreddits))

    async for post in subreddit.stream.submissions():
        if (
            post.author is not None and post.author.is_mod and 
            post.link_flair_text is not None and post.link_flair_text == '[Mod Post]'
        ):
            await post.mod.distinguish(sticky=True)
            
        if (
            post.author is not None and post.author.is_mod is False and 
            post.link_flair_text is not None and post.link_flair_text == '[Mod Post]'
        ):
            await post.mod.remove()
```


Under the hood, comis works by wrapping around [asyncpraw](https://ayncpraw.readthedocs.io/en/latest/) (asynchronous version of praw). 

---
With **comis** there is no need to worry about writing complex logic. Instead, the use of decorators allows you to implement simple chaining of logic by abstracting the actions typically needed which gives you more time to worry about actions on the content. 

### Why did I create comis?
As a Reddit moderator, I realised some tasks could be easily done if automated. AutoModerator was not powerful enough and directly using the API was tedious and repetitive. I created **comis** to make it easier.

