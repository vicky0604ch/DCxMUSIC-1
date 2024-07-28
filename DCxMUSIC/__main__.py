import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from DCxMUSIC import LOGGER, app, userbot
from DCxMUSIC.core.call import DC
from DCxMUSIC.misc import sudo
from DCxMUSIC.plugins import ALL_MODULES
from DCxMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("DCxMUSIC.plugins" + all_module)
    LOGGER("DCxMUSIC.plugins").info("Successfully Imported Modules...")
    await userbot.start()
    await DC.start()
    try:
        await DC.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("DCxMUSIC").error(
            "Please turn on the videochat of your log group\channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass
    await DC.decorators()
    LOGGER("DCxMUSIC").info(
        " \u1d423\u1d42c \u1d415\u1d41c\u1d429\u1d420 \u1d421\u1d41e\u1d422 \u1d429\u1d422\u1d41a\u1d427\u1d41e\u1d42d \u1d429\u1d41c\u1d420\u1d41c\u1d41e\u1d429\u1d425\u1d41f\u1d41c\u1d41b\u1d41f
"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("DCxMUSIC").info("Stopping DC Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
