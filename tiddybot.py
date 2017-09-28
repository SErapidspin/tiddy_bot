import asyncio
import discord
from tinydb import TinyDB, Query, where
import random


db = TinyDB(r'C:\Users\andre\Desktop\Practice Code\tiddy.json')
tiddy_list = list(map(lambda x: x.eid, db.all()))
print(tiddy_list)
client = discord.Client()


@client.event
async def on_ready():
    print("Logged in as:")
    print(client.user.name)
    print(client.user.id)

#TO DO: add validation on adding, add help feature
@client.event
async def on_message(message):
    if message.content.startswith("!tiddy add"):
        inserted = db.insert({"url": message.content[11:]})
        tiddy_list.append(inserted)
        await client.send_message(message.channel, "Thank you for your contribution. Tiddy accepted")
    elif message.content.startswith("!tiddy undo"):
        db.remove(eids = [tiddy_list[-1]])
        tiddy_list.pop()
        await client.send_message(message.channel,"Deleting latest tiddy. Sayonara!" )
    elif message.content.strip() == "!tit":
        await client.send_file(message.user, fp=r'C:\Users\andre\Desktop\Practice Code\tit.jpg', content='YOU FOUND THE TIT')
    elif message.content.strip() == "!tiddy help":
        tiddyhelp(message.channel)
    elif message.content.strip() == "!tiddy":
        await client.send_message(message.channel, db.get(eid=tiddy_list[random.randrange(0, len(tiddy_list))])['url'])        

client.run('MzUwNzM3MzgzMzU0MDA3NTUy.DKAaUg.AecaPojDQL2wfM4CR49xFZ65Kyw')


def tiddyhelp(ch):
    em = discord.embed(title = "Tiddybot Help!", description = "Hello! I'm tiddybot, and I'm here to help you with your sins", fields = f)
    em.add_field(name = "!tiddy", value = "Shows a random tiddy")
    em.add_field(name = "!tiddy add <url>" , value= "Adds <url> to the tiddy cause. Currently there's no validation to check if the url is valid, so please use _!tiddy undo_ if you mess up")
    em.add_field(name = "!tiddy undo", value = "Deletes the most recent tiddy url added. This can include urls added from a while back, so please be careful.")
    em.add_field(name = "!tiddy help", value = "You're looking at it!")
    em.add_field(name = "!tit", value = "It's a surprise!")
    em.set_author(name = "tiddybot")
    await client.send_message(ch, embed= em)