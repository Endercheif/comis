from re import compile

from comis import Client, submission
from comis.filters import Day, author, flair, time


class MyBot(Client):
    @flair(text=compile(r"\[MEME]"))
    @time(days=[Day.monday])
    @author(mod=False, admin=False)
    @submission()
    async def monday_filter(self, content, mod):
        await mod.remove(mod_note="Meme filter")
        await mod.send_removal_message(
            "Your post has been removed automatically:\n   "
            "Memes are not allowed on Monday."
        )
