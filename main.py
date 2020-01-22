import client_secret
import discord
import asyncio
import socket
import glob
import json


mizDir = "C:\\Users\\Administrator\\Saved Games\\DCS.openbeta_server\\Missions\\"
clientListSrs = "C:\\Program Files\\DCS-SimpleRadio-Standalone\\clients-list.json"
client = discord.Client()

def isOpen(ip,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.connect((ip, int(port)))
      s.shutdown(2)
      return True
   except:
      return False
def filename(path):
    tmp = path.split('\\')
    if (len(tmp)==1):
        return tmp
    return tmp[-1]
@client.event
async def on_message (message):
    if (message.author==client.user):
        return

    if (message.content.startswith("!")):
        #Command
        command = message.content[1:]
        commands = command.split()
        #await message.channel.delete_messages([message])
        if (commands[0]=="status"):
            if (isOpen("127.0.0.1",10308)):
                await message.channel.send("Server is up!")
            else:
                await message.channel.send("Server is down!")
        elif(commands[0]=="tacview"):
            await message.channel.send("http://dcs.1506.se:1776/")
        elif(commands[0]=="manage"):
            await message.channel.send("https://www.digitalcombatsimulator.com/en/personal/server/")
        elif(commands[0]=="login"):
            embed = discord.Embed(title="Credentials", color=0xff0000)
            embed.add_field(name="Username", value="{}".format(client_secret.username), inline=False)
            embed.add_field(name="Password", value="{}".format(client_secret.password), inline=False)
            mess = await message.channel.send("This message will self destruct in 60 seconds...",embed=embed)
            await asyncio.sleep(60)
            await message.channel.delete_messages([mess])
        elif(commands[0]=="miz"):
            files = glob.glob(mizDir+"*.miz")
            files = map(filename,files)
            embed = discord.Embed(title="Missions", color=0x0000ff)
            for f in files:
                embed.add_field(name="{0}".format(f), value="[Download](http://miz.1506.se:1776/{0})".format(f), inline=False)
            mess = await message.channel.send(embed=embed)
            await asyncio.sleep(120)
            await message.channel.delete_messages([mess])
        elif(commands[0]=="help"):
            await message.channel.send("This command is not ready!")
        elif(commands[0]=="skins"):
            await message.channel.send("http://skins.1506.se:1776/")
        elif(commands[0]=="srs"):
            with open(clientListSrs) as json_file:
                data = json.load(json_file)
                embed = discord.Embed(title="Connected clients (dcs.1506.se:5002)", color=0x0000ff)
                for c in data["Clients"]:
                    tmp = c["RadioInfo"]
                    radios = tmp["radios"]
                    radios=filter(lambda x: x["name"]!="No Radio",radios)
                    m = ""
                    for r in radios:
                        s = "{} - {}Mhz".format(r['name'],r['freq']/1000000)
                        m = m + s + "\n"
                    embed.add_field(name="{}".format(tmp["name"]),value=m)
                await message.channel.send(embed=embed)

        


    else:        
        for att in message.attachments:
            if (att.filename.endswith(".miz")):
                await att.save(mizDir + att.filename)
                print(att.filename)
                await message.channel.send(att.filename + " saved!")




client.run(client_secret.token)
