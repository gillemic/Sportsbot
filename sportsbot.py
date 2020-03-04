import os
import datetime
import asyncio
#from dateutil.parser import parse

import discord
from dotenv import load_dotenv
from sportsreference.nba.boxscore import Boxscores

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


bot = discord.Client()

def contains(message, text):
	if message.find(text) > -1:
		return True
	else:
		return False

def lookup_games(date):
	if date == "today":
		today = datetime.datetime.now()
		return Boxscores(datetime.date(today.year, today.month, today.day))
	elif date == "yesterday":
		today = datetime.datetime.now()
		return Boxscores(datetime.date(today.year, today.month, today.day-1))
	else:
		day = datetime.datetime.strptime(date, '%m/%d/%Y')
		return Boxscores(datetime.date(day.year, day.month, day.day))

@bot.event
async def on_ready():
	print(f'{bot.user} has connected to Discord')

@bot.event
async def on_message(message):
	channel = message.channel

	if message.author == bot.user:
		return

	text = message.content.lower()
	args = text.split()

	if contains(text, 'games'):
		date = args[1]

		try:
			datetime.datetime.strptime(date, '%m/%d/%Y')
		except ValueError:
			if date == "today" or date == "yesterday":
				pass
			else:
				print('The date {} is invalid'.format(date))
				await channel.send('The date {} is invalid'.format(date))
				return

		games = lookup_games(date)

		for x in games.games:
			games_list = games.games[x]
		reply = ""

		if not games_list:
			await channel.send("There is currently no game data for the given date")
			return

		for i in range(len(games_list)):
			home_team = games_list[i]['home_name']
			away_team = games_list[i]['away_name']
			home_score = games_list[i]['home_score']
			away_score = games_list[i]['away_score']
			reply = reply + home_team + "  " + str(home_score) + "     " + away_team + "  " + str(away_score) + "\n"

		#if not reply:
		#	await channel.send("There is currently no game data for the given date")
		#	return

		await channel.send(reply[:-1])


bot.run(TOKEN)
