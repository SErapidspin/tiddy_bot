import asyncio
import discord
from tinydb import TinyDB, Query, where
import random
import os


db = TinyDB(r'.\tiddy.json')
tiddy_list = list(map(lambda x: x.eid, db.all()))
print(tiddy_list)
client = discord.Client()

async def tiddyhelp(ch):
    em = discord.Embed(title = "Tiddybot Help!", description = "Hello! I'm tiddybot, and I'm here to help you with your sins")
    em.add_field(name = "!tiddy", value = "Shows a random tiddy")
    em.add_field(name = "!tiddy add <url>" , value= "Adds <url> to the tiddy cause.")
    em.add_field(name = "!tiddy undo", value = "Deletes the most recent tiddy url added. This is meant as more of a quick fix if you mess up adding something. For specific deletions, please use _!tiddy delete_")
    em.add_field(name = "!tiddy delete <url>", value = "Deletes any instance of <url> in the tiddy database.")
    em.add_field(name = "!tiddy help", value = "You're looking at it!")
    em.add_field(name = "!tit", value = "It's a surprise!")
    em.set_author(name = "tiddybot")
    await client.send_message(ch, embed= em)

@client.event
async def on_ready():
    print("Logged in as:")
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(game=discord.Game(name='!tiddy help'))

#TO DO: add validation on adding, add help feature
@client.event
async def on_message(message):
    if message.content.startswith("!tiddy add"):
        inserted = db.insert({"url": message.content[11:]})
        tiddy_list.append(inserted)
        await client.send_message(message.channel, "Thank you for your contribution. Tiddy accepted.")
    elif message.content.startswith("!tiddy delete"):
        delete_url = message.content[14:].strip()
        if db.contains(where('url') == delete_url):
            removed_id = db.remove(where('url') == delete_url)
            for i in removed_id:
                tiddy_list.remove(i)
            await client.send_message(message.channel, "Tiddy URL has been deleted.")
        else:
            await client.send_message(message.channel, "Tiddy URL not found! Please double check that you've entered the URL correctly.")
    elif message.content.startswith("!tiddy undo"):
        db.remove(eids = [tiddy_list[-1]])
        tiddy_list.pop()
        await client.send_message(message.channel,"Deleting latest tiddy. Sayonara!" )
    elif message.content.strip() == "!tit":
        filelist = os.listdir("./tits")
        randfile = os.path.join("tits", filelist[random.randrange(0, len(filelist))])
        await client.send_file(message.author, randfile, content='YOU FOUND THE TIT')
    elif message.content.strip() == "!tiddy help":
        await tiddyhelp(message.channel)
    elif message.content.strip() == "!tiddy":
        await client.send_message(message.channel, db.get(eid=tiddy_list[random.randrange(0, len(tiddy_list))])['url'])        

client.run('MzUwNzM3MzgzMzU0MDA3NTUy.DKAaUg.AecaPojDQL2wfM4CR49xFZ65Kyw')


