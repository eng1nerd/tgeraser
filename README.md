# TgEraser

[![PyPI version](https://badge.fury.io/py/tgeraser.svg)](https://badge.fury.io/py/tgeraser) [![Build Status](https://travis-ci.org/eng1nerd/tgeraser.svg?branch=master)](https://travis-ci.org/eng1nerd/tgeraser)

Tool deletes all of your messages from chat/channel/dialog on Telegram without admin privilege. Official Telegram clients don't support deletion for all own messages from chat with one click (you need to manually select messages that you want to delete and you can delete only 100 selected meesages per time).

TgEraser decides this problem.

## Installation

```
pip install tgeraser
tgeraser
```

You need to specify own api_id and api_hash which you can get [here](https://my.telegram.org/auth?to=apps)

## Usage

```
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
```

## TO DO list

- web application based on Flask to delete all of your messages from chat/channel/dialog using tgeraser
