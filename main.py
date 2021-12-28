import discord
import asyncio
import random
import os
import requests
import json
from discord.ext import commands

#https://coderedirect.com/questions/635075/how-can-i-get-user-input-in-a-python-discord-bot
#https://newbedev.com/how-can-i-get-user-input-in-a-python-discord-bot
#https://www.codegrepper.com/code-examples/python/discord.py+get+user+input
#https://docs.replit.com/programming-ide/storing-sensitive-information-environment-variables

#to fix the HTTP 429 error: https://replit.com/talk/ask/Discord-Bot-How-to-fix-429-rate-limit-error/121289

client = commands.Bot(command_prefix = "-");

#List of commands and their descriptions, does not show hidden commands
commandsList = ['-tq: Provides today\'s quote of the day\n', '-rq: Provides a random quote from well known people\n', '-cq: Provides a random, customized quote that the creators made or found\n', '-aq: Adds a custom quote and the author\n', '-ping: Bot will say \"Pong!\"\n', '-hello: Bot will say \"Hello!\"\n', '-bye: Bot will say \"Goodbye!\"']

#Bad words
badWords = ['fuck', 'shit', 'penis', 'dick', 'pussy', 'bitch', 'ass', 'wanker', 'damn', 'piss', 'prick', 'cunt']

#Responses to messages containing bad words
languages = ['Mind your language', 'LANGUAGE!!!', 'Take a chill pill', 'Oh someone is having a \"good\" day', 'Take some deep breaths before saying anything more']

#My friends
people = ['+manish mallik', '+sandeep mishra', '+rohan springer', '+reshvar kuppurangi', '+rohit parkar', '+priyansh mewada', '+hrishi rout']

#The descriptions of my friends
personal = ['The starter and co-creator of Botsitive Zen. He is also a cross country runner and is jacked. :man_running: :muscle:', '6\' 3\" :basketball:', ':man_running: :basketball:', 'Experience tranquility', 'He can be easily memed. Other than that, he is handsome and probably the cutest friend ever.', 'Genius mind and co-creator of Botsitive Zen', 'Elite chess player :trophy: :chess_pawn: . You can\'t beat him, he is like Sherlock Holmes']

#Will contain a list of quotes from customQuotes.txt
ownQuotes = []

#Function will read and store the custom quotes from a file
def readCustomQuotes():
  file = open('customQuotes.txt', 'r')
  for x in file:
    ownQuotes.append(x)
  file.close()

#Function will save the array of custom quotes to a file
def saveCustomQuotes():
  file = open('customQuotes.txt', 'w')
  for x in ownQuotes:
    file.write(x)
  file.close()

#Function chooses and returns a random phrase from the list of language responses when someone says a bad word
def language():
  index = random.randrange(0, len(languages))
  return languages[index]

#Returns a personality description based on what the full name of the person is from the message. If there is none, will say that there is no personality for the person
def personality(message):
  indexNum = -1
  found = False
  for x in people:
    indexNum += 1
    if x == message:
      found = True
      break
  if found:
    return personal[indexNum]
  else:
    return "No personality for this person" 

#returns a quote and author pulled from ZenQuotes API
def getQuotes(message):
  if message == 'today':
    #Gets the quote of the day
    pull = requests.get('https://zenquotes.io/api/today')
  else:
    #Gets a random quote
    pull = requests.get('https://zenquotes.io/api/random')
  #Gets the full text of the quote
  data = json.loads(pull.text)
  #Full data of the quote gets reduced to only quote and author
  quote = data[0]['q'] + '\n-' + data[0]['a']
  return quote

#Bot will send a list of the commands and their descriptions when someone asks for the commands
@client.command()
async def commands(ctx):
  message = ''
  for x in commandsList:
    message += x
  await ctx.send(message)

#Bot will send today's quote of the day from ZenQuotes
@client.command()
async def tq(ctx):
  quote = getQuotes('today')
  await ctx.send(quote)

#Bot will send a random quote from ZenQuotes
@client.command()
async def rq(ctx):
  quote = getQuotes('random')
  await ctx.send(quote)   

#Bot will respond to -ping with Pong!
@client.command()
async def ping(ctx):
  await ctx.send('Pong!')

#Bot will say Hello! if someone says -hello
@client.command()
async def hello(ctx):
  await ctx.send('Hello!')

#Bot will say Goodbye! if someone says -bye
@client.command()
async def bye(ctx):
  await ctx.send('Goodbye!')

#Bot will choose a random custom quote and its respective author from a list of custom quotes and their authors
@client.command()
async def cq(ctx):
  index = random.randrange(0, len(ownQuotes))
  if index % 2 == 1:
    index -= 1
  await ctx.send(ownQuotes[index] + '-' + ownQuotes[index + 1])

#Bot will add a custom quote and its author
@client.command()
async def aq(ctx):
  #Bot will ask for the quote
  await ctx.send('Add a quote')
  quote = ''
  author = ''
  #Bot makes sure that the user input is from the same author and same channel
  def check(msg):
    return msg.author == ctx.author and msg.channel == ctx.channel
  #User has 1 minute to respond. After a minute, proccess gets cancelled
  try:
    quote = await client.wait_for("message", check=check, timeout = 60)
  except asyncio.TimeoutError:
    await ctx.send('Cancelling process, you took too long')
  #Process continues if quote is not an empty string
  if(quote != ''):
    await ctx.send('Got the quote. Now add the author')
    #Bot asks for author's name and makes sure that the response is from the same user and channel
    def check(msg):
      return msg.author == ctx.author and msg.channel == ctx.channel
    #User has 1 minute to respond. After a minute, proccess gets cancelled
    try:
      author = await client.wait_for("message", check=check, timeout = 60)
    except asyncio.TimeoutError:
      await ctx.send('Cancelling process, you took too long')
    #Process continues if author is not an empty string
    if(author != ''):
      await ctx.send('Got the author!')
      #Bot will check if the quote from the user is the same exact phrase as any of the custom quotes, if the exact words of the quote is in any custom quote, or if any exact words of a quote (order matters) are in the quote provided
      similarQuote = False
      for x in range(0, len(ownQuotes), 2):
        if quote.content.lower() in ownQuotes[x].lower() or ownQuotes[x].lower() in quote.content.lower() or quote.content.lower() == ownQuotes[x].lower():
          await ctx.send('We are sorry, it looks like we found the same exact quote or a quote that contains everything you sent in the same order, so we will not add this quote. Thank you for making an effort though, we appreciate it.')
          similarQuote = True
          break
      #If the custom quote that is being added is not considered to be about the same, then the quote and author get added and saved in a list of custom quotes and a text file
      if similarQuote == False:
        ownQuotes.append("\n" + quote.content + "\n")
        ownQuotes.append(author.content)
        saveCustomQuotes()
        await ctx.send('We added your quote and credentials, thank you so much!')

@client.event
async def on_ready():
  readCustomQuotes()
  print("Running the bot")

#Hidden features are in this bot
@client.event
async def on_message(message):
  content = message.content
  if message.author == client.user:
    return
  #Bot will tell the user to not be sad if the author says "im sad"
  elif content.lower() == 'im sad':
    await message.channel.send('Do not be sad '+ message.author.mention + ', it is not the end of the world! You can do it!')
  #Bot will tell the user to not be mad if the author says "im mad"
  elif content.lower() == 'im mad':
    await message.channel.send('Stop being mad, or you are going to hurt someone.')
  elif content.lower() == 'grinch':
    await message.channel.send('Be more loveable and caring')
  #Bot will respond to bad words by telling users to be careful what they say
  if any(word in content.lower() for word in badWords):
    msg = language()
    await message.channel.send(msg)
  #Bot will respond to commands with +firstName lastName by providing descriptions of them if they exist in an array of people. This feature is hidden and currently contains my friends
  if any(word == content.lower() for word in people):
    msg = personality(content.lower())
    await message.channel.send(msg)
    if content.lower() == '+hrishi rout':
      await message.channel.send('https://tenor.com/view/thanos-thanos-dance-party-vibes-gif-14138984')
  if 'sus' == content.lower() or content.lower().startswith('sus ') or ' sus ' in content.lower() or content.lower().endswith(' sus'):
    await message.channel.send('https://tenor.com/view/caught-in-4k-caught-in4k-chungus-gif-19840038')
  #process the message to see if it contains the prefix command
  await client.process_commands(message)

my_secret = os.environ['TOKEN']
client.run(my_secret)