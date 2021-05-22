import discord
from discord.ext import commands, tasks
import asyncio
import datetime
from datetime import datetime, timedelta
import os
import random
import time
import keep_alive
import json
import aiohttp
import sqlite3
import aiosqlite3
import io
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import requests



intents = discord.Intents.all()
print(discord.__version__)

bot = commands.Bot(command_prefix='.', case_insensitive=True, intents=intents)






bot.remove_command("help")






@bot.event
async def on_ready():
    
    
    
    print('ready')

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(830479433503997973)
    await channel.send(f"{member.name} Just left the server ):")





@bot.event
async def on_raw_reaction_add(payload):
    if payload.guild_id is None:
        return
    
    guild = bot.get_guild(payload.guild_id)
    role = guild.get_role(800975142686687252)
    member = guild.get_member(payload.user_id)
    if payload.message_id == 830464892674375721:
        await member.add_roles(role)
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        my_file = os.path.join(THIS_FOLDER, 'image0.jpg')
        with Image.open(my_file) as background:
                        welcome = bot.get_channel(830479433503997973)
                        response = requests.get(member.avatar_url)
                        
                        str1 = f"{member}"
                        
                        font = ImageFont.truetype(r"TCB_____.TTF", 70)
                        
                        w, h = font.getsize(str1)
                        name = ImageDraw.Draw(background)
                        name.text(((1150 - w)/ 2, (800 - h)/ 2), str1, font = font, fill = "gray")
                        
                        im = Image.open(io.BytesIO(response.content))
                        im = im.resize((250, 250))
                        bigsize = (im.size[0] * 3, im.size[1] * 3)
                        mask = Image.new('L', bigsize, 0)
                        draw = ImageDraw.Draw(mask) 
                        draw.ellipse((0, 0) + bigsize, fill=255)
                        mask = mask.resize(im.size, Image.ANTIALIAS)
                        im.putalpha(mask)
                        background.paste(im, (435, 100), im)
                        imageObject = io.BytesIO()
                        background.save(imageObject, "png")
                        imageObject.seek(0)
                        await welcome.send(f"Hey {member.mention}, welcome to Empathy's World! Make sure to read the rules, then get straight into chatting! If you enjoy, make sure to subscribe to Empathy on YouTube! Thanks! ||<@&830137194882138152>||", file=discord.File(imageObject, filename="file.png"))
        return







@bot.event
async def on_member_join(member):
    guilds = bot.get_guild(800280721179541515)
    rolex = guilds.get_role(830125506749136946)
    roley = guilds.get_role(830124591870509056)
    rolez = guilds.get_role(830125863248723988)
    roleu = guilds.get_role(830125364310704218)
    list = [rolex, roley, rolez, roleu]
    for role_id in list:
        await member.add_roles(role_id)
    
    if time.time() - member.created_at.timestamp() < 604800:
        guilds = bot.get_guild(800280721179541515)
        role = guilds.get_role(829298754464120862)
        await member.add_roles(role)
        channel = bot.get_channel(829301025549713420)
        await channel.send(f"@everyone a sus habibi has joined({member.mention}), Code: `Account too young` ")
    else:
        return
       



@bot.command()
async def roleretroscan(ctx):
    member_count = bot.get_guild(800280721179541515)
    rolex = member_count.get_role(830125506749136946)
    roley = member_count.get_role(830124591870509056)
    rolez = member_count.get_role(830125863248723988)
    roleu = member_count.get_role(830125364310704218)
    list = [rolex, roley, rolez, roleu]
    for role_id in list:
        for members in member_count.members:
            await members.add_roles(role_id)
    await ctx.send("done!")
        











bot.membrs = []
bot.create = []
bot.ticket_channels = {}
bot.id_channels = {}
bot.chanels = []
bot.new_msgs = True
@bot.event

async def on_message(message):
    if message.author.id == bot.user.id:
	    return
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id FROM main WHERE user_id='{message.author.id}'")
    result = cursor.fetchone()
    if result is None:
	    sql = ("INSERT INTO main(user_id, messnum) VALUES(?, ?)")
	    val = (message.author.id, 1)
	    cursor.execute(sql, val)
	    db.commit()
    else:
	    cursor.execute(f"SELECT user_id, messnum FROM main WHERE user_id = '{message.author.id}'")
	    result2 = cursor.fetchone()
	    messnum = int(result2[1])
	    sql = ("UPDATE main SET messnum = ? WHERE user_id = ?")
	    val = (messnum + 1, str(message.author.id))
	    cursor.execute(sql, val)
	    db.commit()
	    cursor.close()
	    db.close()
	    await bot.process_commands(message)
	
    if '<@&801032407309746207>' in message.content.lower():
        role = discord.utils.find(lambda r: r.name == 'sus habibi', message.guild.roles)
        if role in message.author.roles:
            await message.channel.send("No, you're sus!")
            return
        
        else:
            channel = message.channel
            m = await channel.send(f'**{message.author.mention} Do you wish to notify and ping all staff?** \nPlease use this for an emergency only.\n\nFalsely misuing this feature will get you warned and if continued a ban. If you agree with this please react with \U0001f44d.')
            await m.add_reaction('\U0001f44d')
            def check(reaction, user):	
                return user == message.author and str(reaction.emoji) == '\U0001f44d'
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                await channel.send("Aborted")
            else:
                role = discord.utils.find(lambda r: r.name == "law reinforcer", message.guild.roles)
                for user in message.guild.members:
                    if role in user.roles:
                        await user.send(f"A possible raid has been triggered\n in {channel.mention}\n triggered by {message.author.mention}")
                        await channel.send("Staff has been called, be patient.")
                        return
    a_file = open("msgs.json", "r")
    json_object = json.load(a_file)
    a_file.close()
    json_object["messages"] += 1
    a_file = open("msgs.json", "w")
    json.dump(json_object, a_file)
    a_file.close()
    server = bot.get_guild(800280721179541515)
    if not message.guild:
        if not message.author.bot:
            if message.author.id not in bot.membrs:
                await message.add_reaction('✅')
                def check(reaction, user):
                    return user.id == message.author.id and str(reaction.emoji) == '✅'
                try:
                    await message.author.send(f"Please react with ✅ to open a support ticket in **{server}**")
                    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    await message.author.send("Timeout, please try again later")
                else:
                    if message.author.id not in bot.create:
                        ticket_no = random.randint(0, 999)
                        bot.membrs.append(message.author.id)
                        bot.create.append(message.author.id)
                        admin_role = discord.utils.get(server.roles, name='law reinforcer')
                        overwrites = {
                        server.default_role: discord.PermissionOverwrite(read_messages=False),
                        server.me: discord.PermissionOverwrite(read_messages=True),
                        admin_role: discord.PermissionOverwrite(read_messages=True)
                        }
                        ticket = await server.create_text_channel(f'ticket-{ticket_no}', overwrites=overwrites, category=bot.get_channel(840742163012911104))
                        bot.ticket_channels.update({message.author.id:ticket.id})
                        bot.id_channels.update({ticket.id:message.author.id})
                        bot.chanels.append(ticket.id)
                        embed = discord.Embed(color=0x013d97)
                        embed.add_field(name = 'Support Ticket:', value = '__**Details:**__', inline=False)
                        embed.add_field(name = 'Member:', value = f"**{message.author}**", inline=False)
                        embed.add_field(name = 'Member ID:', value = message.author.id, inline=False)
                        embed.add_field(name = 'Message Content:', value = message.content, inline=False)
                        embed.add_field(name = f'How to reply to {message.author}:', value = f"!r Message Here", inline=False)
                        embed.add_field(name = f'Note:', value = f"To see all support commands, please type `!dmhelp`", inline=False)
                        embed.set_footer(text=f"{message.author} | {message.author.id}", icon_url=message.author.avatar_url)
                        embed.timestamp = datetime.utcnow()
                        await ticket.send(f"@here please type `!dmhelp` to see all available commands", embed=embed)
                        author = message.author
                        sent = discord.Embed(color=0x00ff00)
                        sent.add_field(name = "Message Sent, __**Content:**__", value = message.content)
                        sent.set_footer(text=f"{author} | {author.id}", icon_url=author.avatar_url)
                        sent.timestamp = datetime.utcnow()
                        await message.author.send(embed=sent)

            else:
                ticket_chnl = bot.get_channel(bot.ticket_channels[message.author.id])
                embed = discord.Embed(color=0x013d97)
                embed.add_field(name = 'Support Ticket:', value = '__**Details:**__', inline=False)
                embed.add_field(name = 'Member:', value = f"**{message.author}**", inline=False)
                embed.add_field(name = 'Member ID:', value = message.author.id, inline=False)
                embed.add_field(name = 'Message Content:', value = message.content, inline=False)
                embed.add_field(name = f'How to reply to {message.author}:', value = f"!r Message Here", inline=False)
                embed.add_field(name = f'Note:', value = f"To see all support commands, please type `!dmhelp`", inline=False)
                embed.set_footer(text=f"{message.author} | {message.author.id}", icon_url=message.author.avatar_url)
                embed.timestamp = datetime.utcnow()

                await ticket_chnl.send(embed=embed)

                sent = discord.Embed(color=0x00ff00)
                sent.add_field(name = "Message Sent, __**Content:**__", value = message.content)
                sent.set_footer(text=f"{message.author} | {message.author.id}", icon_url=message.author.avatar_url)
                sent.timestamp = datetime.utcnow()
                await message.author.send(embed=sent)
fsdffsd
    if message.channel.id in bot.chanels:
        memebr = bot.get_user(bot.id_channels[message.channel.id])

        if message.content.startswith('!r '):
            try:
                embed = discord.Embed(color=0x00ffff)
                embed.add_field(name = 'Reply:', value = message.content.replace("!r", ""))
                embed.set_footer(text=f"{message.author} | {message.author.id}", icon_url=message.author.avatar_url)
                embed.timestamp = datetime.utcnow()
                await memebr.send(embed=embed)
                await message.channel.send(f"Message sent to **{memebr}** :+1:")
                await message.channel.send(embed=embed)
            except discord.errors.HTTPException:
                await message.channel.send('Please type content, e.g. `!r Hi there!`')
        
        if message.content.startswith('!w'):
            embed = discord.Embed(color=0x00ffff)
            server = bot.get_guild(769259848516763659)
            embed.add_field(name = 'Reply:', value = f"Welcome to our support system, how may I help you?")
            embed.set_footer(text=f"{message.author} | {message.author.id}", icon_url=message.author.avatar_url)
            embed.timestamp = datetime.utcnow()
            await memebr.send(embed=embed)
            await message.channel.send(f"Message sent to **{memebr}** :+1:")
            await message.channel.send(embed=embed)
# So, you basically add the snippet letter, and what does the snippet represent, in this case, !w represents Welcome to {server} support system, how may I help you?, so just typing !w, will send that message, Clear?basically an alias? Sorta, but without passing an arg, try making a snippet:Try make a snippet ok
        if message.content.startswith('!whatever'):
            e = discord.Embed(
            title= ' whatever',
            description= '\u200b',
            color = message.author.color # Btw, to send to the member, use the var memebr and NOT member, memebr.send()
            )
            await memebr.send(embed=e)
            await message.channel.send(f"Message sent to **{memebr}** :+1:")
            await message.channel.send(embed=e) # that's it, I'll try open a thread now. Use snippet !whatever
        
        if message.content.startswith('!close'):     
            await message.add_reaction('✅')
            def checka(reaction, user):
                return user.id == message.author.id and str(reaction.emoji) == '✅'
            try:
                await message.channel.send(f"Please react with ✅ to end this support ticket")
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=checka)
            except asyncio.TimeoutError:
                await message.channel.send("Timeout, please try again later")
            else: 
                try:
                    embed = discord.Embed(color=0xff0000)
                    embed.add_field(name = 'Support ended, reason:', value = message.content.replace("!close", ""))
                    embed.set_footer(text=f"{message.author} | {message.author.id}", icon_url=message.author.avatar_url)
                    embed.timestamp = datetime.utcnow()
                    await memebr.send(embed=embed)
                    await memebr.send(f"Thank you for contacting {server} support system, feel free to open another tikcet if needed")
                    await message.channel.send('Bye! This channel will be deleted in 5 seconds')
                    await asyncio.sleep(5.0)
                    bot.membrs.remove(memebr.id)
                    bot.create.remove(memebr.id)
                    bot.chanels.remove(message.channel.id)
                    del bot.ticket_channels[memebr.id]
                    del bot.id_channels[message.channel.id]
                    await message.channel.delete()
                except discord.errors.HTTPException:
                    await message.channel.send('Please type a reason, e.g. `!close Done`')
	
	
	
	
  
  


@bot.command()
async def svrmsg(ctx):
    a_file = open("msgs.json", "r")
    json_object = json.load(a_file)
    a_file.close()
    x = json_object["messages"]
    embed = discord.Embed(
		colour=ctx.author.color,
        title=f"Server currently has `{x}` messages.",
        description=" "
    )
    embed.timestamp = datetime.now()
    await ctx.send(embed=embed)

@tasks.loop(seconds=180)
async def ff():
    
    member_count = bot.get_guild(800280721179541515)
    activitys=discord.Status.do_not_disturb
    activity = discord.Game(name=f'Dm for modmail || Entertaining {member_count.member_count} members', type=3)
    await bot.change_presence(status=activitys, activity=activity)
    channel = bot.get_channel(830728950543155230)
    await channel.edit(name=f"Member Count: {member_count.member_count}")


ff.start()



@ff.before_loop
async def before_change_status():
    await bot.wait_until_ready()









    
          
    

   


    

  
  




@bot.command()
async def msgnum(ctx, user: discord.User=None):
    user = ctx.author if not user else user
    db = await aiosqlite3.connect('main.sqlite')
    cursor = await db.cursor()
    await cursor.execute(f"SELECT user_id, messnum FROM main WHERE user_id = '{user.id}'")
    result = await cursor.fetchone()
    
    embed = discord.Embed(
		colour=ctx.author.color,
        title=f"You currently have `{str(result[1])}` messages.",
        description=" "
    )
    embed.timestamp = datetime.now()
    await ctx.send(embed=embed)
    await cursor.close()
    await db.close()










@bot.event
async def on_command_error(ctx, error):
    if isinstance(error,commands.MissingPermissions):
        embeds = discord.Embed(
            colour=discord.Colour.red(),
            title="Sorry",
            description=f"I couldn't complete the operation since you have missing priveleges"
        )
        await ctx.send(embed=embeds)
    if isinstance(error, commands.MissingRole):
        embedsz = discord.Embed(
            colour=discord.Colour.red(),
            title="Sorry",
            description=f"I couldn't complete the operation since you're not a law reinforcer"
        )
        await ctx.send(embed=embedsz)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour=discord.Colour.red(),
            title="Sorry",
            description="Missing required argument, use `.help` for more information."
        )
        await ctx.send(embed=embed)



      



@bot.command()
@commands.has_role(829371403215831070)
async def susify(ctx, member: discord.Member,*, reason="sus"):
    
    await ctx.message.delete()
    guilds = bot.get_guild(800280721179541515)
    role = guilds.get_role(829298754464120862)
    role2 = guilds.get_role(800975142686687252)
    if role in member.roles:
        await ctx.send(f"{member.mention} is already sus!")
        return   
    else:
        await member.add_roles(role)
        await member.remove_roles(role2)
        channel = bot.get_channel(829301025549713420)
        await channel.send(f"@everyone a sus habibi has joined({member.mention}), Code: `{reason}`")
    

@bot.command()
@commands.has_role(829371403215831070)
async def unsusify(ctx, member: discord.Member):
    await ctx.message.delete()
    guilds = bot.get_guild(800280721179541515)
    role = guilds.get_role(829298754464120862)
    role2 = guilds.get_role(800975142686687252)
    if role not in member.roles:
        await ctx.send(f"{ctx.author.mention} how am i supposed to unsus someone that isn't even sus?!")
        return
    else:
        await member.remove_roles(role)
        await member.add_roles(role2)
        channel = bot.get_channel(829301025549713420)
        await channel.send(f"Done!")

@bot.command()
async def help(ctx, page=None):
    if page == None:
      e = discord.Embed(
        color = ctx.author.color,
        title='Help',
        description='Dm for mod mail :D')
     
      e.add_field(name='suggest', value="Usage: `.suggest (suggestion)`", inline=False)
      e.add_field(name='ytsuggest', value="Usage: `.ytsuggest (suggestion)`", inline=False)
      e.add_field(name='@allstaffcall', value="Pinging that role will ping all staff members incase of a raid.", inline=False)
      e.add_field(name='msgnum', value="It checks the number of messages you currently have.", inline=False)
      e.add_field(name='svrmsg', value="It checks how many messages the server currently has", inline=False)
      e.add_field(name='subscribercount', value="It checks Empathy's sub count", inline=False)
      e.add_field(name='Mod help', value="send `.help mod` to show mod commands!")
      await ctx.send(embed=e)
  
    if page == "mod":
        role = discord.utils.find(lambda r: r.name == 'law reinforcer', ctx.message.guild.roles)
        if role in ctx.author.roles:
            e = discord.Embed(
                color = ctx.author.color,
                title='Help Mod',
                description=' ')
            e.add_field(name='Raid', value='It locks server USE ONLY IN EMERGENCIES', inline=False)
            e.add_field(name='Unraid', value='It unlocks server USE ONLY IN EMERGENCIES', inline=False)
            e.add_field(name='susify', value='sends someone to the sus cell **|** Usage: `.susify [mention someone] [reason]`', inline=False)
            e.add_field(name='unsusify', value='sends someone back to the kindom **|** Usage: `.unsusify [mention someone]`', inline=False)
            await ctx.send(embed=e)
        else:
            await ctx.send("You don't have permissions!")




    


@bot.command(aliases=['usd'])
@commands.has_role(829371403215831070)
async def unraid(ctx):



  dsds = discord.Embed(
    colour=ctx.author.color,
    title="Unlocked All channels",
    description=f"all channels are unlocked.\n\nUnlocked by : {ctx.author.mention}")
  await ctx.message.delete()
  x = bot.get_channel(800974918660522004)
  c = bot.get_channel(800280721633443863)
  b = bot.get_channel(800981203364478986)
  n = bot.get_channel(800981291116920854)
  m = bot.get_channel(800981401016991785)
  a = bot.get_channel(800981687093166100)
  p = bot.get_channel(829252267098112030)
  f = bot.get_channel(829284701189570620)
  await x.set_permissions(ctx.guild.default_role, send_messages=None)
  await c.set_permissions(ctx.guild.default_role, send_messages=None)
  await b.set_permissions(ctx.guild.default_role, send_messages=None)
  await n.set_permissions(ctx.guild.default_role, send_messages=None)
  await m.set_permissions(ctx.guild.default_role, send_messages=None)
  await a.set_permissions(ctx.guild.default_role, send_messages=None)
  await p.set_permissions(ctx.guild.default_role, send_messages=None)
  await f.set_permissions(ctx.guild.default_role, send_messages=None)
  await ctx.send(embed=dsds)

  
      



    
@bot.command(aliases=['sd'])
@commands.has_role(829371403215831070)
async def raid(ctx):

  dsds = discord.Embed(
      colour=ctx.author.color,
      title="Emergency Server Lock",
      description=
      f"A possible raid has been triggered and all channels are locked. Please do not direct message staff members during this time. You are not muted, no one can talk.\n\nLocked by : {ctx.author.mention}"
  )
  await ctx.message.delete()
  
  x = bot.get_channel(800974918660522004)
  c = bot.get_channel(800280721633443863)
  b = bot.get_channel(800981203364478986)
  n = bot.get_channel(800981291116920854)
  m = bot.get_channel(800981401016991785)
  a = bot.get_channel(800981687093166100)
  p = bot.get_channel(829252267098112030)
  f = bot.get_channel(829284701189570620)
  await x.set_permissions(ctx.guild.default_role, send_messages=False)
  await c.set_permissions(ctx.guild.default_role, send_messages=False)
  await b.set_permissions(ctx.guild.default_role, send_messages=False)
  await n.set_permissions(ctx.guild.default_role, send_messages=False)
  await m.set_permissions(ctx.guild.default_role, send_messages=False)
  await a.set_permissions(ctx.guild.default_role, send_messages=False)
  await p.set_permissions(ctx.guild.default_role, send_messages=False)
  await f.set_permissions(ctx.guild.default_role, send_messages=False)

  await ctx.send(embed=dsds)
      
  
@bot.command()
async def subscribercount(ctx):
	token = "AIzaSyAtpJBbyi7ClOyEI8Oxdsb4mCKRTauHx5s"
	url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UC1HLnJprOsUmQlS9iRaXhzQ&key={token}"
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as r:
			response = await r.json()
	x = response
	
	
	e = discord.Embed(
		color = ctx.author.color,
		title = "Subscribers",
		description =x["items"][0]["statistics"]["subscriberCount"]
	)
	e.timestamp = datetime.now()
	
	await ctx.send(embed=e)
	
@tasks.loop(seconds=500)
async def fd():
    token = "AIzaSyAtpJBbyi7ClOyEI8Oxdsb4mCKRTauHx5s"
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UC1HLnJprOsUmQlS9iRaXhzQ&key={token}"
    async with aiohttp.ClientSession() as session:
	    async with session.get(url) as r:
		    response = await r.json()
    x = response
    e = bot.get_channel(829266141906075678)
    subs = x["items"][0]["statistics"]["viewCount"]
    await e.edit(name="View Count:"+ " "+ "{:,d}".format(int(subs)))
	



fd.start()


@fd.before_loop
async def qas():
    await bot.wait_until_ready()

@tasks.loop(seconds=500)
async def ff():
    token = "AIzaSyAtpJBbyi7ClOyEI8Oxdsb4mCKRTauHx5s"
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UC1HLnJprOsUmQlS9iRaXhzQ&key={token}"
    async with aiohttp.ClientSession() as session:
	    async with session.get(url) as r:
		    response = await r.json()
    x = response
    e = bot.get_channel(801455671497064518)
    subs = x["items"][0]["statistics"]["subscriberCount"]
    await e.edit(name="Subscriber count:"+ " "+ "{:,d}".format(int(subs)))
	



ff.start()





@ff.before_loop
async def before_change_status():
    await bot.wait_until_ready()

          

            






@bot.command()
async def ytsuggest(ctx,*, suggestion):
    await ctx.message.delete()
    e = discord.Embed(
    title=f'by {ctx.author.name}',
    description=' ',
    color=ctx.author.color
    )
    e.add_field(name=suggestion, value='\u200b', inline=False)
    e.set_thumbnail(url=ctx.author.avatar_url)

  
    w = bot.get_channel(800981534508187658)
    
    
    ea = await w.send(embed=e)
    await ea.add_reaction('\U0000274c')
    await ea.add_reaction('\U00002705')

@bot.command()
async def suggest(ctx,*, suggestion):
    await ctx.message.delete()
    e = discord.Embed(
    title=f'by {ctx.author.name}',
    description=' ',
    color=ctx.author.color
    )
    e.add_field(name=suggestion, value='\u200b', inline=False)
    e.set_thumbnail(url=ctx.author.avatar_url)

  
    w = bot.get_channel(800981534508187658)
    
    
    ea = await w.send(embed=e)
    await ea.add_reaction('\U0000274c')
    await ea.add_reaction('\U00002705')
  
  
  

    





keep_alive.keep_alive()
TOKEN = os.environ.get("DISCORD_BOT_SECRET")
bot.run(TOKEN)
