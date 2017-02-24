# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import time
import asyncio
from tinydb import TinyDB, Query
from classes.SourceQuery import SourceQuery
from modules.WorkerFunctions import *

Search = Query()
bot = commands.Bot(command_prefix='/')

@bot.event
async def on_ready():
	print('Logged in as {0}\n'.format(bot.user.name))
@bot.event
async def on_command_error(error, ctx):
	await bot.send_message(ctx.message.channel, ":octagonal_sign: An error occurred:\n```{0}```".format(error))

@bot.command(pass_context=True, aliases=['q'], description="Queries a server and prints some if it’s info")
async def query(context, addr: str, port=27015):
	if is_valid_ip(addr):
		oServer = SourceQuery(addr=addr, port=port, timeout=5.0); lServer = oServer.getInfo()
		if lServer is not False:
			try:
				lServer["Hostname"] = lServer["Hostname"].encode("iso-8859-1").decode("utf-8")
			except:
				pass;
			em = discord.Embed(title=":lock: "+lServer["Hostname"] if bool(lServer["Password"]) else ":unlock: "+lServer["Hostname"], description='Map: {0}'.format(lServer["Map"]), colour=0x10EE00)
			em.set_author(name='Query result ({0}):'.format(lServer["_engine_"]), icon_url=bot.user.avatar_url)
			em.add_field(name="Players", value="{0}/{1}".format(lServer["Players"], lServer["MaxPlayers"]), inline=True)
			em.add_field(name="VAC", value=("Enabled" if bool(lServer["Secure"]) else "Disabled"), inline=True)
			em.add_field(name="Running on", value=lServer["OS"], inline=True)
			em.add_field(name="Mod", value=lServer["GameDesc"], inline=False)
			em.add_field(name="Type", value=lServer["Dedicated"], inline=True)
			em.add_field(name="Version", value=lServer["Version"], inline=True)

			await bot.send_message(context.message.channel, embed=em)
		else:
			await bot.say(":warning: The server doesn’t seem to be running from here.")
	else:
		await bot.say(":warning: You’ve provided malformed IP address.")

@bot.command(pass_context=True, aliases=['a'], ignore_extra=True, description="Adds a server to your watchlist")
async def add(context, addr: str, port=27015):
	if is_valid_ip(addr):
		db = TinyDB('./database.json')
		db.insert({
			'userid': context.message.author.id,
			'server_addr': addr,
			'server_port': port,
		})
		db.close()
		await bot.say(":white_check_mark: Server added!")
	else:
		await bot.say(":warning: You’ve provided malformed IP address.")

@bot.command(pass_context=True, aliases=['r'], ignore_extra=True, description="Removes a server from your watchlist")
async def remove(context, addr: str, port=27015):
	if is_valid_ip(addr):
		db = TinyDB('./database.json')
		if db.search((Search.userid==context.message.author.id) & (Search.server_addr==addr) & (Search.server_port==port)) is not False:
			db.remove((Search.userid==context.message.author.id) & (Search.server_addr==addr) & (Search.server_port==port))
			await bot.say(":white_check_mark: Server removed!")
		else:
			await bot.say(":negative_squared_cross_mark: There are no records listing this server.")
		db.close()
	else:
		await bot.say(":warning: You’ve provided malformed IP address.")

@bot.command(pass_context=True, aliases=['c'], ignore_extra=True, description="Queries all servers from your watchlist")
async def check(context):
	db = TinyDB('./database.json'); lServers = db.search(Search.userid==context.message.author.id); db.close()
	em = discord.Embed(title="Server query results", description="Total servers: {0}".format(len(lServers)), colour=0x5677E8)
	for i in range(len(lServers)):
		full_addr = lServers[i]["server_addr"]+":"+str(lServers[i]["server_port"])
		em.add_field(name=full_addr, value=":white_check_mark: Responded" if is_alive(lServers[i]["server_addr"], lServers[i]["server_port"]) else ":warning: Didn’t respond", inline=False)
	await bot.send_message(context.message.channel, embed=em)


async def crontab():
	await bot.wait_until_ready()
	while not bot.is_closed:
		db = TinyDB('./database.json'); lServers = db.all(); db.close()
		servers = ""; mList = {};
		for i in range(len(lServers)):
			if (not is_alive(lServers[i]["server_addr"], lServers[i]["server_port"])) and (not is_alive(lServers[i]["server_addr"], lServers[i]["server_port"], 15)):
				mList.setdefault(lServers[i]["userid"],[]).extend([" * "+lServers[i]["server_addr"]+":"+str(lServers[i]["server_port"])])
			else:
				continue;
		for key, value in mList.items():
			user = discord.User(id=key)
			await bot.send_message(user, "Some servers did not respond:\n```"+"\n".join(value)+"```")
		await asyncio.sleep(120)

bot.loop.create_task(crontab())
bot.run('paste_your_token_here')