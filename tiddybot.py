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
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)

#TO DO: add validation on adding, add help feature
@client.event
async def on_message(message):
    if message.content.startswith('!tiddy add'):
        inserted = db.insert({'url': message.content[11:]})
        tiddy_list.append(inserted)
        await client.send_message(message.channel, "Thank you for your contribution. Tiddy accepted")
    elif message.content.startswith('!tiddy undo'):
        db.remove(eids=[tiddy_list[-1]])
        tiddy_list.pop()
        await client.send_message(message.channel,"Deleting latest tiddy. Sayonara!" )
    elif message.content.strip() == '!tit':
        await client.send_file(message.channel, fp=r'C:\Users\andre\Desktop\Practice Code\tit.jpg', content='YOU FOUND THE TIT')
    elif message.content.strip() == '!tiddy help':
        await client.send_message(message.channel, 'Hello! I\'m here to help you with your \n sins')
    elif message.content.strip() == '!tiddy':
        await client.send_message(message.channel, db.get(eid=tiddy_list[random.randrange(0, len(tiddy_list))])['url'])        

client.run('MzUwNzM3MzgzMzU0MDA3NTUy.DKAaUg.AecaPojDQL2wfM4CR49xFZ65Kyw')