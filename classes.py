from gevent import monkey as curious_george
from pkg_resources import resource_exists
curious_george.patch_all(thread=False, select=False)

import sqlite3, requests, hypixel

from urllib import request


class CheckSettings():
    def __init__(self):
        pass

    def keyCheck(self):
        data = sqlite3.connect("files/data.db")
        cur = data.cursor()
        self.result = cur.execute("""SELECT value FROM keys 
                                     WHERE key = 'Hypixel'""").fetchall()
        data.close()
        if self.result[0][0] != '':
            return True
        else:
            return False

    def keyValid(self, key):
        if requests.get(f"https://api.hypixel.net/key?key={key}").json()['success']:
            return True
        else:
            return False


class SetSettings():
    def setHypixelApi(key):
        if CheckSettings.keyValid:
            data = sqlite3.connect("files/data.db")
            cur = data.cursor()
            cur.execute("""UPDATE keys
                           SET value = ?
                           WHERE key = 'Hypixel'""", (key,))
            data.commit()
            data.close()

    def setDefaultNick(nick):
        data = sqlite3.connect("files/data.db")
        cur = data.cursor()
        cur.execute("""UPDATE settings
                           SET value = ?
                           WHERE name = 'nick'""", (nick,))
        data.commit()
        data.close()

    def setLang(lang):
        data = sqlite3.connect("files/data.db")
        cur = data.cursor()
        cur.execute("""UPDATE settings
                           SET value = ?
                           WHERE name = 'lang'""", (lang,))
        data.commit()
        data.close()



class GetSettings():
    def HypixelAPI():
        data = sqlite3.connect("files/data.db")
        cur = data.cursor()
        result = cur.execute("""SELECT value FROM keys 
                                WHERE key = 'Hypixel'""").fetchall()
        data.close()
        return result[0][0]

    def Nick():
        data = sqlite3.connect("files/data.db")
        cur = data.cursor()
        result = cur.execute("""SELECT value FROM settings 
                                WHERE name = 'nick'""").fetchall()
        data.close()
        return result[0][0]


class Mojang():
    def __init__(self, nick):
        self.nick = nick
        self.uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{self.nick}?at=0").json()
        self.uuid = self.uuid["id"]

    def uuid(self):
        return self.uuid

    def correct_name(self):
        nicks = requests.get(f"https://api.mojang.com/user/profiles/{self.uuid}/names").json()
        return nicks[-1]["name"]

    def old_names(self):
        return requests.get(f"https://api.mojang.com/user/profiles/{self.uuid}/names").json()

    def skin(self):
        return request.urlopen(f"https://crafatar.com/renders/body/{self.uuid}?overlay").read()


class Hypixel_main():
    def __init__(self, key, uuid):
        hypixel.setKeys([key])
        self.key = key
        self.uuid = uuid
        self.player = hypixel.Player(self.uuid)
        self.info = self.player.JSON

    def lvl(self):
        return self.player.getLevel()

    def rank(self):
        p = " "
        rank = self.player.getRank()['rank']
        if rank == 'MVP PLUS':
            return f"""<font color='#00FFFF' size = 18 >MVP</font><font color='{self.info['rankPlusColor'].replace('_', p)}' size = 18 >+</font>"""
        elif rank == 'MVP':
            return """<font color='#00FFFF' size = 18 >MVP</font>"""
        elif rank == 'VIP PLUS':
            return """<font color='green' size = 18 >VIP</font><font color='yellow' size = 18 >+</font>"""
        elif rank == 'VIP':
            return """<font color='green' size = 18 >VIP</font>"""
        elif rank == 'YOUTUBER':
            return """<font color='red' size = 18 >[</font><font color='grey' size = 18 >YOUTUBER</font><font color='red' size = 18 >]</font>"""
        if rank == 'SUPERSTAR':
            return f"""<font color='#00FFFF' size = 18 >MVP</font><font color='{self.info['rankPlusColor'].replace('_', p)}' size = 18 >++</font>"""
        
    def karma(self):
        return str(self.info['karma'])

    def achievement_points(self):
        return str(self.info['achievementPoints'])

    def guildname(self):
        try:
            p = " "
            self.ginfo = requests.get(f"https://api.hypixel.net/guild?key={self.key}&player={self.uuid}").json()
            tag = f"<font color='{self.ginfo['guild']['tagColor'].replace('_', p)}' size=18>{self.ginfo['guild']['tag']}</font>"
            return f"<font size=18>{self.ginfo['guild']['name']}</font> {tag}"
        except Exception:
            return "<font color='red' size=18>Is not in a guild</font>"

    def get_session(self):
        if requests.get(f"https://api.hypixel.net/status?key={self.key}&uuid={self.uuid}").json()['session']['online'] == False:
            return "<font color='red' size=18>Offline</font>"
        else:
            return "<font color='red' size=18>Online</font>"
        




    

        
