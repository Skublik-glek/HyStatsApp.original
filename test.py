import sys, re
from javascript import require, On, Once
mineflayer = require("mineflayer", "latest")
Vec3 = require("vec3").Vec3



bot = mineflayer.createBot({
  "host": 'localhost',
  "port": 25565,
  "version": "1.17.1",
  "authTitle": '00000000402b5328',
  "auth": 'microsoft'                  
})

@On(bot, "chat")
def handle(this, username, message, *args):
    return username + " " + message