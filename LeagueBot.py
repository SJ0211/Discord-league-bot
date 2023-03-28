import discord
from discord.ext import commands
import asyncio
from riotwatcher import LolWatcher, ApiError, TftWatcher

def Setup():
    asyncio.sleep(1.0)
    api_key = open("ApiKey.txt", 'r').read()
    lolwatcher = LolWatcher(api_key)
    open("ApiKey.txt", 'r').close()

TOKEN = "<Your Discord Bot Token>"

bot = commands.Bot(command_prefix="L.")

F = open("ApiKey.txt", 'r')
api_key = F.read()
lolwatcher = LolWatcher(api_key)
F.close()
DdragonRegiondict = {'na1': 'en_US', 'kr': 'ko_KR'}
region = 'na1'

@bot.event
async def on_ready():
    channel = bot.get_channel(966306646961823767)
    await channel.send('hello')
    await bot.change_presence(activity=discord.Game(name="League of Legends"))
    print(f'{bot.user} succesfully logged in!')


@bot.event
async def on_message(message):
    # Make sure the Bot doesn't respond to it's own messages
    if message.author == bot.user:
        return

    if message.content == 'hello':
        await message.channel.send(f'Hi {message.author}')
    if message.content == 'bye':
        await message.channel.send(f'Goodbye {message.author}')

    await bot.process_commands(message)

@bot.command()
async def search(ctx, arg):
    global ChampName
    loop = True
    Input = arg
    i = 0
    while loop == True:
        try:
            User = lolwatcher.summoner.by_name(region, Input)
        except ApiError as err:
            if err.response.status_code == 429:
                print("Retry after. Riot games don't let me do cool stuff a lot in a short time period")
                await ctx.send("Retry after. Riot games don't let me do cool stuff a lot in a short time period")
            elif err.response.status_code == 404:
                print('Summoner with that ridiculous name not found.')
                await ctx.send("Summoner with that ridiculous name not found.")
            else:
                raise
        print(User)
        print(User['id'])
        RankedStats = lolwatcher.league.by_summoner(region, User['id'])
        RankedStatsDict = {}
        RankedStatsDict = RankedStats[0]
        Text = ""
        print(RankedStatsDict)
        if RankedStatsDict['queueType'] == 'RANKED_SOLO_5x5':
            break
        elif i > 15:
            await ctx.send("This guy doesn't even play ranked solo. Too scared")
            return ctx.bot

        else:
            i += 1
            continue

    #THIS THING TOOK ME 5 HOURS TO GET IT RIGHT
    #RIOT GAMES Y YOU HAD TO GIVE ME A TRIPLE NESTED DICTIONARY?

    Mastery = lolwatcher.champion_mastery.by_summoner(region, User['id'])
    MasteryDict = {}
    MasteryDict = Mastery[0]

    print(MasteryDict)
    MasteryID = MasteryDict['championId']
    ChampMasteryLv = MasteryDict['championLevel']
    MasteryPt = MasteryDict['championPoints']

    latest = lolwatcher.data_dragon.versions_for_region(region)['n']['champion']

    # Lets get some champions static information
    static_champ_list = lolwatcher.data_dragon.champions(latest, False, 'en_US')
    print(static_champ_list)

    ChampNameDict = {}

    for key in static_champ_list['data']:
        print(key)
        ID = static_champ_list['data'][key]['key']
        Name = static_champ_list['data'][key]['name']
        ChampNameDict[str(ID)] = Name

    print(ChampNameDict)
    ChampName = ChampNameDict[str(MasteryID)]
    ChampPic = str(MasteryID) + ".png"

    if RankedStatsDict['tier'] == 'IRON':
        with open('IRON.png', 'rb') as fp:
            await ctx.send(file=discord.File(fp, 'IRON.png'))
    elif RankedStatsDict['tier'] == 'BRONZE':
        with open('BRONZE.png', 'rb') as fp:
            await ctx.send(file=discord.File(fp, 'BRONZE.png'))
    elif RankedStatsDict['tier'] == 'SILVER':
        with open('SILVER.png', 'rb') as fp:
            await ctx.send(file=discord.File(fp, 'SILVER.png'))
    elif RankedStatsDict['tier'] == 'GOLD':
        with open('GOLD.png', 'rb') as fp:
            await ctx.send(file=discord.File(fp, 'GOLD.png'))
    elif RankedStatsDict['tier'] == 'PLATINUM':
        with open('PLATINUM.png', 'rb') as fp:
            await ctx.send(file=discord.File(fp, 'PLATINUM.png'))
    elif RankedStatsDict['tier'] == 'DIAMOND':
        with open('DIAMOND.png', 'rb') as fp:
            await ctx.send(file=discord.File(fp, 'DIAMOND.png'))
    elif RankedStatsDict['tier'] == 'MASTER':
        with open('MASTER.png', 'rb') as fp:
            await ctx.send(file=discord.File(fp, 'MASTER.png'))
    elif RankedStatsDict['tier'] == 'GRANDMASTER':
        with open('GRANDMASTER.png', 'rb') as fp:
            await ctx.send(file=discord.File(fp, 'GRANDMASTER.png'))
    elif RankedStatsDict['tier'] == 'CHALLENGER':
        with open('CHALLENGER.png', 'rb') as fp:
            await ctx.send(file=discord.File(fp, 'CHALLENGER.png'))
    else:
        pass

    Text2 = ""

    Text = Text + "Name: " + RankedStatsDict['summonerName'] + "\n"
    Text = Text + "Rank: " + RankedStatsDict['tier'] + " " + RankedStatsDict['rank'] + " " + str(
    RankedStatsDict['leaguePoints']) + "LP" + "\n"
    Text = Text + "Total games played: " + str(RankedStatsDict['wins'] + RankedStatsDict['losses']) + '\n'
    Text = Text + "Wins: " + str(RankedStatsDict['wins']) + "\n"
    Text = Text + "losses: " + str(RankedStatsDict['losses']) + '\n'
    WinRate = (int(RankedStatsDict['wins']) / (int(RankedStatsDict['wins']) + int(RankedStatsDict['losses'])) * 100)
    Text = Text + "Winrate: " + str(WinRate) + '%\n'
    Text2 = Text2 + "Highest Mastery: [" + ChampName + "]\n"
    Text2 = Text2 + "Mastery Level: LV " + str(ChampMasteryLv) + "\n"
    Text2 = Text2 + "Mastery Points: " + str(MasteryPt) + " PT\n"
    print(Text)
    print(Text2)

    await ctx.send(Text)
    with open(ChampPic, 'rb') as fp:
        await ctx.send(file=discord.File(fp, ChampPic))

    await ctx.send(Text2)

#RIOT GAMES HAVE NO INFO FOR THIS API

#@bot.command()(brief='check if the user is on', description='chech if the user is on')
#async def check(ctx, arg):
    #try:
        #User = lolwatcher.summoner.by_name(region, arg)
    #except ApiError as err:
        #if err.response.status_code == 429:
            #print("Retry after. Riot games don't let me do cool stuff a lot in a short time period")
            #await ctx.send("Retry after. Riot games don't let me do cool stuff a lot in a short time period")
        #elif err.response.status_code == 404:
            #print('Summoner with that ridiculous name not found.')
            #await ctx.send("Summoner with that ridiculous name not found.")
        #else:
            #raise
    #print(User)
    #print(User['id'])
    #Summoner = User['id']
    #Data = lolwatcher.spectator.by_summoner('na1', Summoner)
    #print(Data)

@bot.command()
async def f2p(ctx):
    rotation = lolwatcher.champion.rotations('na1')
    print(rotation)
    ChampIdList = rotation['freeChampionIds']
    latest = lolwatcher.data_dragon.versions_for_region(region)['n']['champion']

    # Lets get some champions static information
    static_champ_list = lolwatcher.data_dragon.champions(latest, False, 'en_US')
    print(static_champ_list)
    #make Dictionary thats {champid : name}
    ChampNameDict = {}

    for key in static_champ_list['data']:
        ID = static_champ_list['data'][key]['key']
        Name = static_champ_list['data'][key]['name']
        ChampNameDict[str(ID)] = Name
    Text = "Free to Play: \n\n"



    print(ChampNameDict)
    for id in ChampIdList:
        ChampPic = str(id) + ".png"
        await ctx.trigger_typing
        with open(ChampPic, 'rb') as fp:
            await ctx.send(file=discord.File(fp, ChampPic))
        ChampName = ChampNameDict[str(id)]
        Text = ChampName + ","
        await ctx.send(Text)


    await ctx.send("That's it!")

    print(Text)



@bot.command()
async def shutdown(ctx):
    if ctx.message.author.id == <id>:
        await ctx.send("cya")
        await ctx.bot.logout()
    else:
        await ctx.send("You are not my master")

#couldn't fiqure it out (maybe could have used json)

#@bot.command()(brief='Update api key', description='Update api key')
#async def updatekey(ctx, arg):
    #if ctx.message.author.id == 338885742543765525:
        #F = open("ApiKey.txt", 'w')
        #F.write(arg)
        #Setup()
        #await ctx.send("done!")
        #return

    #else:
        #await ctx.send("You are not my master")

bot.run(TOKEN)
