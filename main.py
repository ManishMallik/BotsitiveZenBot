import discord
import asyncio
import random
import os
import requests
import json
from discord.ext import commands
import re
import nltk
from nltk.corpus import stopwords
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
nltk.download('stopwords')

stop_Words = stopwords.words('english')
stop_Words.pop(0)

client = commands.Bot(command_prefix = "-");

#List of text commands and their descriptions, does not show hidden commands
commandsList = [
'-tq: Provides today\'s quote of the day\n', 
'-rq: Provides a random quote from well known people\n', '-cq: Provides a random, customized quote that the creators made or found\n', 
'-aq: Adds a custom quote and the author\n', 
'-ping: Bot will say \"Pong!\"\n', 
'-hello: Bot will say \"Hello!\"\n', '-bye: Bot will say \"Goodbye!\"\n', 
'-balance: Bot will describe about good and evil in people and show Zenyatta holding light and dark orbs.\n',
'-urban \"type\" \"term\": The types are either \"name\" or \"word\". If the word you will provide is a name type, the bot will try to give the best possible description of that person using sentiment analysis. If the word given is an actual word, then the bot will try to find the most specific definition of that word.'
]

vCommands = [ 
'-zenyatta: You will hear Zenyatta\'s voice.\n', 
'-courage: Gives you courage to do it.', 
'-zuko: Hear Zuko\'s best moment', 
'-leave: Commands the bot to leave the voice channel.\n'
]
#Bad words
badWords = ['fuck', 'shit', 'penis', 'dick', 'pussy', 'bitch', 'ass', 'wanker', 'damn', 'piss', 'prick', 'cunt']

#Responses to messages containing bad words
languages = ['Mind your language', 'LANGUAGE!!!', 'Take a chill pill', 'Oh someone is having a \"good\" day', 'Take some deep breaths before saying anything more', 'https://tenor.com/view/chill-out-kevin-hart-jumanji-jumanji-movie-gif-11210111']

#Dictionary of descriptions
descriptions = {
  #My friends
  'people': ['-manish mallik', '-sandeep mishra', '-rohan springer', '-reshvar kuppurangi', '-rohit parkar', '-priyansh mewada', '-hrishi rout', '-krishna rout'],
  #Descriptions about my friends
  'facts': ['The starter and co-creator of Botsitive Zen. He is also a cross country runner and is jacked. :man_running: :muscle:', '6\' 3\", The Indian Kevin Durant :basketball:. He looks like a snack; any girl would want him. He can trash talk and beat up anyone, do not mess with him or he will throw hands :muscle:', ':man_running: :basketball:', 'Experience tranquility', 'He can be easily memed. Other than that, he is handsome and probably the cutest friend ever.', 'Genius mind and co-creator of Botsitive Zen', 'Elite chess player :trophy: :chess_pawn: . You can\'t beat him, he is like Sherlock Holmes', 'Got the beard, got the mustache, and got the hair. DO NOT SHAVE THEM!!!'],
  #Images/GIFs
  'images': ["https://tenor.com/view/boom-dude-ryan-reynolds-free-guy-pow-gif-22851757", "https://tenor.com/view/short-fight-tall-gif-21229601", "https://tenor.com/view/mom-sexy-mom-hot-momma-gif-12128762", "https://tenor.com/view/overwatch-overwatch-league-gladiators-gladiator-la-gladiators-gif-13503131", "https://tenor.com/view/josuke-pose-jjba-jojo-josuke-pose-gif-7693551", "https://tenor.com/view/troll-stick-figure-dancing-gif-5259835", "https://tenor.com/view/thanos-thanos-dance-party-vibes-gif-14138984", "https://tenor.com/view/beard-man-with-beard-men-with-beard-mustache-goatee-gif-5598626"]
}

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
  for x in descriptions['people']:
    indexNum += 1
    if x == message:
      found = True
      break
  if found:
    return descriptions['facts'][indexNum]
  else:
    return "No personality for this person"

#Returns a GIF or image that depicts a certain person
def depiction(message):
  indexNum = -1
  found = False
  for x in descriptions['people']:
    indexNum += 1
    if x == message:
      found = True
      break
  if found:
    return descriptions['images'][indexNum]
  else:
    return "" 

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

#This method will use sentiment analysis to analyze a description and calculate its score
def vader_uncleaned_score(msg):
  sentiment_score = 0
  count = 0
  text = msg
  for i in text:
    i = i.strip().replace('\n',' ')
    sentiment_score += analyzer.polarity_scores(i)['compound']
    count+=1
  return(sentiment_score/count)

#Bot will send a list of the commands and their descriptions when someone asks for the commands
@client.command()
async def commands(ctx):
  message = 'Text Commands:\n'
  for x in commandsList:
    message += x
  message += '\n\nVoice Commands:\n'
  for x in vCommands:
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

#Bot will use the Urban Dictionary API to pull a list of all the possible definitions/descriptions for a word
@client.command()
async def urban(ctx, term, msg):
  #Setup to request for a list of descriptions
  url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
  querystring = {"term":msg}
  myKey = os.environ['My Urban Key']
  headers = {
    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
    'x-rapidapi-key': myKey
  }
  
  #Get the list of definitions for the word being searched for
  response = requests.request("GET", url, headers=headers, params=querystring)
  data = json.loads(response.text)
  #1st definition of the word in that list
  definition = data['list'][0]['definition']
  
  #Two types of words: a regular word, or a name
  #The type of the word/term being searched for in the urban dictionary must be specified
  #If the word is supposed to be a name, then get the best urban dictionary description possible for the name
  if term == 'name':
    #Initial score for the 1st definition
    highestScore = vader_uncleaned_score(definition)
    for x in data['list']:
      #Get the sentiment analysis score of the next definition in the list
      newScore = vader_uncleaned_score(x['definition'])
      #If newScore is greater than the highest sentiment analysis score seen so far, replace the chosen definition with the new one before going to the next definition
      #Make newScore the new highestScore
      if highestScore < newScore:
        definition = x['definition']
        highestScore = newScore
  #The word type should just be a regular word if not a name. Get the longest definition possible
  elif term == 'word':
    for x in data['list']:
      if len(definition) < len(x['definition']):
        definition = x['definition']
  #Make sure the type of search term is either name or word; if not specified or if an invalid type is entered, the bot will not send anything
  if term == 'name' or term == 'word':
    await ctx.send(definition)

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

#Sends a message along with the yin-yang emoji and a Zenyatta, a character from Overwatch
@client.command()
async def balance(ctx):
  await ctx.send('Not everyone is either entirely good or evil. In good, there is some evil, and in evil, there is some good.')
  await ctx.send(':yin_yang:')
  await ctx.send('https://tenor.com/view/zenyatta-robot-power-gif-7313314')

#async def join(ctx):
  #vc = ctx.author.voice.channel
  #print(vc)
  #voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
  #if(voice == None):
    #await vc.connect()

#Voice command. It has the Zenyatta saying 'Experience tranquility'
@client.command()
async def zenyatta(ctx):
  #join(ctx)
  vc = ctx.author.voice.channel
  print(vc)
  voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
  if(voice == None):
    await vc.connect()
  guild = ctx.guild
  voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=guild)
  audio_source = discord.FFmpegPCMAudio('experienceTranquility.mp3')
  #if not voice_client.is_playing():
   # voice_client.play(audio_source, after = None)
  print('Time to play')
  await voice_client.play(audio_source).start()
  print('Time to leave')
  await ctx.voice_client.disconnect(force = True)
  print('Time to left')
  #player.start()
  #while not player.is_done():
   # await asyncio.sleep(1)
  #player.stop()

@client.command()
async def courage(ctx):
  vc = ctx.author.voice.channel
  print(vc)
  voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
  if(voice == None):
    await vc.connect()
  guild = ctx.guild
  voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=guild)
  audio_source = discord.FFmpegPCMAudio('doIt.mp3')
  #if not voice_client.is_playing():
   # voice_client.play(audio_source, after = None)
  voice_client.play(audio_source, after = None).start()

@client.command()
async def zuko(ctx):
  vc = ctx.author.voice.channel
  print(vc)
  voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
  if(voice == None):
    await vc.connect()
  guild = ctx.guild
  voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=guild)
  audio_source = discord.FFmpegPCMAudio('zuko.mp3')
  #if not voice_client.is_playing():
   # voice_client.play(audio_source, after = None)
  voice_client.play(audio_source, after = None).start()
  ctx.voice_client.disconnect()

@client.command()
async def leave(ctx):
  await ctx.voice_client.disconnect()
  
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
  #Bot will respond to bad words by telling users to be careful what they say
  if any(word in content.lower() for word in badWords):
    msg = language()
    if('ass' in content.lower()):
      if not('mass' in content.lower() or 'bass' in content.lower()):
        await message.channel.send(msg)
    else:
      await message.channel.send(msg)
  #Bot will respond to commands with +firstName lastName by providing descriptions of them if they exist in an array of people. This feature is hidden and currently contains my friends
  if 'manish and rohan' in content.lower() or 'rohan and manish' in content.lower():
    await message.channel.send('The real dynamic duo, not Rohit and Avirat')
  if 'sus' == content.lower() or content.lower().startswith('sus ') or ' sus ' in content.lower() or content.lower().endswith(' sus'):
    await message.channel.send('https://tenor.com/view/caught-in-4k-caught-in4k-chungus-gif-19840038')
  #process the message to see if it contains the prefix command
  if any(word == content.lower() for word in descriptions['people']):
    msg = personality(content.lower())
    await message.channel.send(msg)
    image = depiction(content.lower())
    if image != "":  
      await message.channel.send(image)
  else:
    await client.process_commands(message)

my_secret = os.environ['TOKEN']
client.run(my_secret)
