Quickstart
==========

Installation
------------

Comis is available on PyPI and supports Python 3.10 and above.

    .. code-block:: bash

        pip install comis

    .. note::

        Depending on your system you may need to use ``pip3`` instead of ``pip``.


A Quick Bot
-----------

Creating a bot with comis is simple.

    .. code-block:: python

        from comis import Client, submission

        class MyBot(Client):
            @submission()
            async def check_posts(self, post, mod):
                print(post.title)


        bot = MyBot(
            client_id="YOUR_CLIENT_ID",
            client_secret="YOUR_CLIENT_SECRET",
            user_agent="comis reddit bot by /u/YOUR_USERNAME",
            username="USERNAME",
            password="PASSWORD",
            subreddits=["your_subreddit"],
        ).

        bot.run()



