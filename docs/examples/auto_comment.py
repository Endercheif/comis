from comis import Client, submission


class MyBot(Client):
    @submission()
    async def auto_comment(self, content, mod):
        reply = await content.reply(
            "Beep boop, this is an automated message "
            "from the mods to remember to follow the rules."
        )
        await reply.distinguish(sticky=True)
