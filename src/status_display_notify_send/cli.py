#! /usr/bin/env python
#
# cmus_desktop_notify.py: display song cmus is playing using notify-send.
# Copyright (C) 2011  Travis Poppe <tlp@lickwid.net>
#
# Version 2011.7.0
# http://tlp.lickwid.net/cmus_desktop_notify.py
#
# Usage: Run script for instructions.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# - @todo Offer some configuration
# - @todo Clean up status_data() (first iteration problem)
# - @todo Clean up notification when some data is missing
# - @todo Attempt to use filename when title is unavailable
# - @todo Make work with python 3/test/etc
#
# Why does this file exist, and why not put this in `__main__`?
#
# You might be tempted to import things from `__main__` later,
# but that will cause problems: the code will get executed twice:
#
# - When you run `python -m status_display_notify_send` python will execute
#   `__main__.py` as a script. That means there won't be any
#   `status_display_notify_send.__main__` in `sys.modules`.
# - When you import `__main__` it will get executed again (as a module) because
#   there's no `status_display_notify_send.__main__` in `sys.modules`.

"""Module that contains the command line application."""
import typer
import typing as T
import sys
import time
import subprocess
from loguru import logger


DEFAULT_CMUS_INFO = {
    "status": "",
    "file": "",
    "artist": "",
    "album": "",
    "albumartist": "",
    "musicbrainz_trackid": "",
    "discnumber": "",
    "tracknumber": "",
    "title": "",
    "date": "",
    "duration": "",
}
__version__ = "2021.12.21"


def status_data(cmus_data: T.Optional[T.List[str]]) -> T.Dict[str, str]:
    """Return the requested cmus status data."""

    # We loop through cmus status data and use each of its known data
    # types as 'delimiters', collecting data until we reach one,
    # inserting it into the dictionary -- rinse and repeat.

    if cmus_data is None:
        # cmus helper script provides our data as argv[1].
        # Split the data into an easily-parsed list.
        cmus_data = sys.argv[1:]

    # Our temporary collector list.
    collector = []

    # Dictionary that will contain our parsed-out data.
    cmus_info = DEFAULT_CMUS_INFO.copy()
    # Loop through cmus data and write it to our dictionary.
    last_found = "status"
    for value in cmus_data:
        collector.append(value)
        # Check to see if cmus value matches dictionary key.
        for key in cmus_info:
            # If a match has been found, record the data.
            if key == value:
                collector.pop()
                cmus_info[last_found] = " ".join(collector)
                collector = []
                last_found = key

    return cmus_info


def version_callback(value: bool):
    if value:
        typer.echo(f"status-display-notify-send: {__version__}")
        raise typer.Exit()


def display_song(
    args: T.List[str],
    version: T.Optional[bool] = typer.Option(None, "--version", callback=version_callback),
):
    """Display the song data using notify-send."""
    logger.add("/tmp/status_display_notify_send.log")
    logger.debug("args: {}", args)
    logger.debug("version: {}", version if version else __version__)
    data = status_data(cmus_data=args)
    logger.debug("data: {}", data)
    status_data_ = data.get
    # We only display a notification if something is playing.
    if status_data_("status", args) == "playing":

        # Check to see if title data exists before trying to display it.
        # Display "Unknown" otherwise.
        title = status_data_("title")
        notify_summary = title if title else "Unknown"

        # Check to see if album data exists before trying to
        # display it. Prevents "Artist, " if it's blank.
        album = status_data_("album")
        artist = status_data_("artist")
        notify_body = artist if artist else ""
        if album:
            notify_body += ", " + album

        # Create our temporary file if it doesn't exist yet.
        open("/tmp/cmus_desktop_last_track", "a").write("4")

        # Check to see when we got our last track from cmus.
        last_notice = open("/tmp/cmus_desktop_last_track", "r").read()

        # Write time stamp for current track from cmus.
        last_notice_time = str(time.time())
        open("/tmp/cmus_desktop_last_track", "w").write(last_notice_time)

        # Calculate seconds between track changes.
        track_change_duration = round(time.time() - float(last_notice))

        # Display current track notification only if 3 seconds have
        # elapsed since last track was chosen.
        if track_change_duration > 3:
            # Execute notify-send with our default song data.
            call_args = [
                "notify-send",
                "-u",
                "normal",
                "-t",
                "5000",
                "--app-name=cmus",
                notify_summary if notify_summary else "",
                notify_body,
            ]
            logger.debug("call args: {}", call_args)
            subprocess.call(call_args)


def main():
    """
    Run the main program.

    This function is executed when you type `status-display-notify-send` or `python -m status_display_notify_send`.

    Arguments:
        args: Arguments passed from the command line.
    """
    typer.run(display_song)


if __name__ == "__main__":
    main()
