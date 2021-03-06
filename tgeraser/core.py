# coding=utf-8
"""
Tool deletes all your messages from chat/channel/dialog on Telegram.

Usage:
    tgeraser [ (session <session_name>) -cdl=NUM [ -i=FILEPATH | -j=DICT | -e ] -p=ID -t=NUM ] | [ -k ]
    tgeraser (-h | --help)
    tgeraser --version

Options:
    -i --input-file=FILEPATH    Specify YAML file that contains credentials. [default: ~/.tgeraser/credentials.yml]
    -j --json=DICT              Specify json string that contains credentials (double quotes must be escaped).
    -e --environment-variables  Get credentials from environment variables (TG_API_ID, TG_API_HASH, TG_SESSION).
    -d --dialogs                List only Dialogs (Chats by default).
    -c --channels               List only Channels (Chats by default).
    -p --peer=ID                Specify certain peer (chat/channel/dialog).
    -l --limit=NUM              Show specified number of recent chats.
    -t --time-period=NUM        Specify period for infinite loop to run messages deletion every NUM seconds.
    -k --kill                   Kill background process if you specify --time option (only for Unix-like OS).
    -h --help                   Show this screen.
    --version                   Show version.

"""

import asyncio
import os
import signal
import subprocess
import sys
import time
import traceback

from docopt import docopt

from . import Eraser
from .__version__ import __version__
from .exceptions import TgEraserException
from .utils import cast_to_int, get_credentials

loop = asyncio.get_event_loop()


def entry() -> None:
    """
    Entry function
    """
    arguments = docopt(__doc__, version=__version__)
    if arguments["--limit"]:
        arguments["--limit"] = cast_to_int(arguments["--limit"], "limit")
    if arguments["--time-period"]:
        arguments["--time-period"] = cast_to_int(arguments["--time-period"], "time")

    if arguments["--kill"]:
        if os.name != "posix":
            raise TgEraserException("You can't use '--kill' option on Windows.")
        cmd = subprocess.Popen(["ps", "-A"], stdout=subprocess.PIPE)
        out = cmd.communicate()[0]
        for line in out.splitlines():
            if "tgeraser" in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)

    try:
        credentials = get_credentials(arguments)

        kwargs = {
            **credentials,
            "dialogs": arguments["--dialogs"],
            "channels": arguments["--channels"],
            "peer": arguments["--peer"],
            "limit": arguments["--limit"],
        }

        client = Eraser(**kwargs)
        while True:
            loop.run_until_complete(client.run())
            if arguments["--time-period"]:
                print(
                    "\n({0})\tNext erasing will be in {1} seconds.".format(
                        time.strftime("%Y-%m-%d, %H:%M:%S", time.gmtime()),
                        arguments["--time-period"],
                    )
                )
                time.sleep(arguments["--time-period"])
            else:
                break
        loop.run_until_complete(client.disconnect())
        loop.close()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception:
        traceback.print_exc(file=sys.stdout)


if __name__ == "__main__":
    entry()
