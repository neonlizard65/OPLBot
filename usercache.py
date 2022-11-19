# -*- coding: utf-8 -*-
class UserCache:
    def __init__(self, user_id, senderinfo=None, vidobr = None, body = None, attachments = None, league_name = None, team_name = None, z_type = None, fio = None, playerdate = None, position = None, players = None, is_anon = False, is_team = False):
        self.user_id = user_id
        self.vidobr = vidobr
        self.body = body
        self.attachments = attachments
        self.senderinfo = senderinfo
        self.league_name = league_name
        self.team_name = team_name
        self.z_type = z_type
        self.fio = fio
        self.playerdate = playerdate
        self.position = position
        self.players = players
        self.is_anon = is_anon
        self.is_team = is_team
        