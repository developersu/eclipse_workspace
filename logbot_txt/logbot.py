#!/usr/bin/env python
# coding: utf-8

"""
   LogBot

   A minimal IRC log bot

   Written by Chris Oliver

   Includes python-irclib from http://python-irclib.sourceforge.net/

   This program is free software; you can redistribute it and/or
   modify it under the terms of the GNU General Public License
   as published by the Free Software Foundation; either version 2
   of the License, or any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA   02111-1307, USA.
"""


__author__ = "Chris Oliver <excid3@gmail.com>"
__version__ = "0.4.2"
__date__ = "08/11/2009"
__copyright__ = "Copyright (c) Chris Oliver"
__license__ = "GPL2"


import cgi
import os
import sys
import itertools
from time import strftime
try:
    from datetime import datetime
    from pytz import timezone
except: pass

try:
    from hashlib import md5
except:
    import md5

from ircbot import SingleServerIRCBot
from irclib import nm_to_n

import re

pat1 = re.compile(r"(^|[\n ])(([\w]+?://[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)", re.IGNORECASE | re.DOTALL)

#urlfinder = re.compile("(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")

def urlify2(value):
#IN CASE OF SHIT RETURN THIS ONE#    return pat1.sub(r'\1<a href="\2" target="_blank">\3</a>', value)
     return pat1.sub(r'\1 \3', value)
### Configuration options
DEBUG = False

# IRC Server Configuration
SERVER = "irc.meganet.ru"
PORT = 6660
SERVER_PASS = None
#CHANNELS=["#loper-42","#123jjj231"]
CHANNELS=["#loper-42", "#16bit"]
NICK = "Praskovia_Botovna"
NICK_PASS = ""

# The local folder to save logs
LOG_FOLDER = "/mnt/sda1/public/logs"

# The message returned when someone messages the bot
#HELP_MESSAGE = "net vremeni boltat. Zahodi na https://dryziaprakrovii.blogspot.ru/"
HELP_MESSAGE = "Майор Ботовна. Хранимые материалы расположены по адресу https://dryziaprakrovii.blogspot.ru/"


CHANNEL_LOCATIONS_FILE = os.path.expanduser("./logbot-channel_locations.conf")
DEFAULT_TIMEZONE = 'UTC'

default_format = {
    "help" : HELP_MESSAGE,
    "action" : '* %user% %message%',
    "join" : '-!- %user% [%host%] has joined %channel%',
    "kick" : '-!- %user% was kicked from %channel% by %kicker% [%reason%]',
    "mode" : '-!- mode/%channel% [%modes% %person%] by %giver%',
    "nick" : '%old% is now known as %new%',
    "part" : '-!- %user% [%host%] has parted %channel%',
    "pubmsg" : '<%user%> %message%',
    "pubnotice" : '-%user%:%channel%- %message%',
    "quit" : '-!- %user% has quit [%message%]',
    "topic" : '%user% changed topic of %channel% to: %message%',
}

# Useless code (for me)
html_header = """%title%"""


### Helper functions

def append_line(filename, line):
    data = open(filename, "rb").readlines()[:-2]
    data += [line, "\n", "\n", "\n"]
    write_lines(filename, data)

def write_lines(filename, lines):
    f = open(filename, "wb")
    f.writelines(lines)
    f.close()

def write_string(filename, string):
    f = open(filename, "wb")
    f.write(string)
    f.close()

color_pattern = re.compile(r'(\[\d{1,2}m)')
"Pattern that matches ANSI color codes and the text that follows"

def pairs(items):
    """
    Return pairs from items

    >>> list(pairs([1,2,3,4]))
    [(1, 2), (3, 4)]
    """
    items = iter(items)
    while True:
        yield next(items), next(items)
    

### Logbot class

class Logbot(SingleServerIRCBot):
    def __init__(self, server, port, server_pass=None, channels=[],
                 nick="timber", nick_pass=None, format=default_format):
        SingleServerIRCBot.__init__(self,
                                    [(server, port, server_pass)],
                                    nick,
                                    nick)

        self.chans = [x.lower() for x in channels]
        self.format = format
        self.count = 0
        self.nick_pass = nick_pass

        self.load_channel_locations()
        print "Logbot %s" % __version__
        print "Connecting to %s:%i..." % (server, port)
        print "Press Ctrl-C to quit"

    def quit(self):
        self.connection.disconnect("Some shit is happening...")

    def color(self, user):
        return "#%s" % md5(user).hexdigest()[:6]


    def format_event(self, name, event, params):
        msg = self.format[name]
        for key, val in params.iteritems():
            msg = msg.replace(key, val)

        # Always replace %user% with e.source()
        # and %channel% with e.target()
        msg = msg.replace("%user%", nm_to_n(event.source()))
        msg = msg.replace("%host%", event.source())
        try: msg = msg.replace("%channel%", event.target())
        except: pass
        msg = msg.replace("%color%", self.color(nm_to_n(event.source())))
        try:
            user_message = cgi.escape(event.arguments()[0])
            msg = msg.replace("%message%", user_message)
        except: pass

        return msg

    def write_event(self, name, event, params={}):
        # Format the event properly
        if name == 'nick' or name == 'quit':
          chans = params["%chan%"]
        else:
          chans = event.target()
        msg = self.format_event(name, event, params)
        msg = urlify2(msg)

        # In case there are still events that don't supply a channel name (like /quit and /nick did)
        if not chans or not chans.startswith("#"):
            chans = self.chans
        else:
            chans = [chans]

        for chan in chans:
            self.append_log_msg(chan, msg)

        self.count += 1

    def append_log_msg(self, channel, msg):
        print "%s >>> %s" % (channel, msg)
        #Make sure the channel is always lowercase to prevent logs with other capitalisations to be created
        channel_title = channel
        channel = channel.lower()

        # Create the channel path if necessary
        chan_path = "%s/%s" % (LOG_FOLDER, channel)
        if not os.path.exists(chan_path):
            os.makedirs(chan_path)

        # Current log
        try:
            localtime = datetime.now(timezone(self.channel_locations.get(channel,DEFAULT_TIMEZONE)))
            time = localtime.strftime("%H:%M:%S")
            date = localtime.strftime("%Y-%m-%d")
        except:
            time = strftime("%H:%M:%S")
            date = strftime("%Y-%m-%d")

        log_path = "%s/%s/%s.txt" % (LOG_FOLDER, channel, date)

        # Create the log date index if it doesnt exist
        if not os.path.exists(log_path):
            write_string(log_path, html_header.replace("%title%", "%s | Logs for %s" % (channel_title, date)))

            # Append date log
#            append_line("%s/index.html" % chan_path, '<a href="%s.html">%s</a>' % (date, date))

        # Append current message
        message = "[%s] %s" % \
                                          (time, msg)
        append_line(log_path, message)

    ### These are the IRC events

    def on_all_raw_messages(self, c, e):
        """Display all IRC connections in terminal"""
        if DEBUG: print e.arguments()[0]

    def on_welcome(self, c, e):
        """Join channels after successful connection"""
        if self.nick_pass:
          c.privmsg("nickserv", "identify %s" % self.nick_pass)

        for chan in self.chans:
            c.join(chan)

    def on_nicknameinuse(self, c, e):
        """Nickname in use"""
        c.nick(c.get_nickname() + "_")

    def on_invite(self, c, e):
        """Arbitrarily join any channel invited to"""
        c.join(e.arguments()[0])
        #TODO: Save? Rewrite config file?

    ### Loggable events

    def on_action(self, c, e):
        """Someone says /me"""
        self.write_event("action", e)

    def on_join(self, c, e):
        self.write_event("join", e)

    def on_kick(self, c, e):
        self.write_event("kick", e,
                         {"%kicker%" : e.source(),
                          "%channel%" : e.target(),
                          "%user%" : e.arguments()[0],
                          "%reason%" : e.arguments()[1],
                         })

    def on_mode(self, c, e):
        self.write_event("mode", e,
                         {"%modes%" : e.arguments()[0],
                          "%person%" : e.arguments()[1] if len(e.arguments()) > 1 else e.target(),
                          "%giver%" : nm_to_n(e.source()),
                         })

    def on_nick(self, c, e):
        old_nick = nm_to_n(e.source())
        # Only write the event on channels that actually had the user in the channel
        for chan in self.channels:
            if old_nick in [x.lstrip('~%&@+') for x in self.channels[chan].users()]:
                self.write_event("nick", e,
                             {"%old%" : old_nick,
                              "%new%" : e.target(),
                              "%chan%": chan,
                             })

    def on_part(self, c, e):
        self.write_event("part", e)

    def on_pubmsg(self, c, e):
        if e.arguments()[0].startswith(NICK):
            c.privmsg(e.target(), self.format["help"])
        self.write_event("pubmsg", e)

    def on_pubnotice(self, c, e):
        self.write_event("pubnotice", e)

    def on_privmsg(self, c, e):
        print nm_to_n(e.source()), e.arguments()
        c.privmsg(nm_to_n(e.source()), self.format["help"])

    def on_quit(self, c, e):
        nick = nm_to_n(e.source())
        # Only write the event on channels that actually had the user in the channel
        for chan in self.channels:
            if nick in [x.lstrip('~%&@+') for x in self.channels[chan].users()]:
                self.write_event("quit", e, {"%chan%" : chan})

    def on_topic(self, c, e):
        self.write_event("topic", e)

    # Loads the channel - timezone-location pairs from the CHANNEL_LOCATIONS_FILE
    # See the README for details and example
    def load_channel_locations(self):
        self.channel_locations = {}
        if os.path.exists(CHANNEL_LOCATIONS_FILE):
            f = open(CHANNEL_LOCATIONS_FILE, 'r')
            self.channel_locations = dict((k.lower(), v) for k, v in dict([line.strip().split(None,1) for line in f.readlines()]).iteritems())


def main():
    # Create the logs directory
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)

    # Start the bot
    bot = Logbot(SERVER, PORT, SERVER_PASS, CHANNELS, NICK, NICK_PASS)
    try:
        bot.start()
    except KeyboardInterrupt:

        bot.quit()


if __name__ == "__main__":
    main()
