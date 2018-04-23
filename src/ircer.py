#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 18:26:46 2018

@author: pseudosecret
"""

import irc.bot
from parser_musician import ParserMusician

class IRCer(irc.bot.SingleServerIRCBot):
    def __init__(self, username, server, port, channel, token):
        self.channel = channel
        self.pm = ParserMusician()
        self.oauth = token

        # Create IRC bot connection
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, self.oauth)], username, username)
        

    def on_welcome(self, c, e):
        print('Joining ' + self.channel)
        
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_nicknameinuse(self, c, e):
        print("Nickname in use. Appending \"_\" to it.")
        c.nick(c.get_nickname() + "_")

    def on_pubmsg(self, c, e):
        print("The argument " + str(e.arguments))
        self.pm.parse_string(e.arguments[0])
        # If a chat message starts with an exclamation point, try to run it as a command
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]
#            print('Received command: ' + cmd)
            self.do_command(e, cmd)
        return


    def do_command(self, e, cmd):
        c = self.connection
        
        if cmd == "faq":
            msg = "Go to https://github.com/pseudosecret/irc-music-generation for more information."
            c.privmsg(self.channel, msg)

"""
        # Poll the API to get current game.
        if cmd == "game":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' is currently playing ' + r['game'])

        # Poll the API the get the current status of the stream
        elif cmd == "title":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' channel title is currently ' + r['status'])

        # Provide basic information to viewers for specific commands
        elif cmd == "raffle":
            message = "This is an example bot, replace this text with your raffle text."
            c.privmsg(self.channel, message)
        elif cmd == "schedule":
            message = "This is an example bot, replace this text with your schedule text."            
            c.privmsg(self.channel, message)

        # The command was not recognized
        else:
            c.privmsg(self.channel, "Did not understand command: " + cmd)
"""