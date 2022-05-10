from re import compile

from comis import Client, comment
from comis.filters import flair

no_no_words = compile(r"(darn)|(heck)")


class MyBot(Client):
    @flair(text=no_no_words)
    @comment()
    async def filter_bad_words(self, content, mod):
        await mod.remove("Bad word detected")
        await mod.send_removal_message(
            f"Your [comment]({content.permalink}) has "
            "been removed because it contains a bad word.",
            type="private",
            title="Comment Removed",
        )
