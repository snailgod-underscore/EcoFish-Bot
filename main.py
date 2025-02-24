import discord
from discord import app_commands
import random
import json
description = "A Fish that loves Economics. Made by Snailgod_. 👍"
intents = discord.Intents.default()
intents.message_content = True
guilds_leaderboards = {} #all the guild's we are in. tracks $$$.
sever_settings_per_guild = {} #self explanatory. hopefully i can think of a better name.
token = ""

async def stop(): #stop function
    with open("Money_Values.json", "w") as money_file: # open the file containg money to write
        print("saving guilds.....") #tells the console we are saving 
        json.dump(guilds_leaderboards,money_file, indent=1)
    with open("Sever_Specific_Settings.json","w") as server_settings_file:
        print("saving guilds settings...")
        json.dump(sever_settings_per_guild,server_settings_file,indent=1)
    print("done!")
    await client.close()


#below is executed once when the bot runs, and never again. it just loads all the filedata.
with open("Money_Values.json", "r") as leaderboard_save:
    guilds_leaderboards = json.load(leaderboard_save)

with open("Sever_Specific_Settings.json", "r") as settings_file:
    sever_settings_per_guild = json.load(settings_file)

with open("secret.json") as secret_file:
    token = json.load(secret_file)

class MyClient(discord.Client):
    async def on_ready(self):
        #tree.clear_commands(guild=discord.Object(id=1340567102884544532))
        await tree.sync(guild=discord.Object(id=1340567102884544532)) #syncs in its test server, otherwise it takes forever to show up.
        print(f'Logged on as {self.user}!') #message to tell me the bot started.

        for guild in client.guilds: #for every guild the bot's in.
            if not str(guild.id) in guilds_leaderboards: #if the guilds not already in our dictionary of guilds.
                guilds_leaderboards[str(guild.id)] = {} #add it with key the guild's name.
                print("added guild " + str(guild.id) + " to guild leaderboards.") #tell the console we added the guild

            if not str(guild.id) in sever_settings_per_guild: #if the guilds not already in our dictionary of guild settings.
                    sever_settings_per_guild[str(guild.id)] = {} #add it with key the guild's name.

                    sever_settings_per_guild[str(guild.id)]["money_symbol"] = "🪙"
                    sever_settings_per_guild[str(guild.id)]["starting_money"] = 100 #first setting, starting money.

                    print("added guild " + str(guild.id) + " to server-specific settings.") #tell the console we added the guild



    async def on_message(self, message):
        #print(f'Message from {message.author}: {message.content}') #logs every message.
        
        #code to send a message: await channel.send("my message") (given we have a channel)
        #to reply to a message: await message.reply("the reply",mention_author = True) (given we have a message, mention is in response to the msg.)

        #below prevents the bot from going into a infinite-message loop.
        if message.author != self.user:
            channel = message.channel #get the channel the message was sent to.
            if (" hello" in message.content or " hi" in message.content or "greetings" in message.content) and client.user.mentioned_in(message): #check if hello or hi is in the msg, as well as check if the bot is mentioned
                await message.reply("hello",mention_author = True) #reply hello, mentioning the author.
                print(message.author.name)
                

            #if message.content == "test emoji":
                #await message.reply("<:Candysnailpixel:1340906209234124920>", mention_author = False) #below was a test to see if custom emoji worked. it did. cool.

            #below is first of hopefully many brainrot detectors.
            if "sigma" in message.content: 
                await message.reply("∑(k=1 to 78) [ (1/k²) + ∑(j=1 to k) (j/k³) ] + ∑(i=1 to 3) [ (-1)ⁱ / (2i + 1) ]",mention_author = True)

            if message.author.id == 957414292687298590 and "stop" in message.content and client.user.mentioned_in(message): #check if i commanded it to stop
                await message.reply("stopping, creator.",mention_author=False) #tells me it's stopping
                await stop() #calls the stop function
                

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                               COMMANDS BABY WHOOO
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



#await interaction.response.send_message("this works.") #used to send a message replying to the command.




client = MyClient(intents=intents) #does... something. all i know is that its how we run and stop the bot. changed form MyClient to discord.
tree = app_commands.CommandTree(client) #establishes the command tree. intents is defined above, but its the last thing we need in this step. its defined before client.

@tree.command(name="start", description="Adds you to the bot. this is the working one.", guild=discord.Object(id=1340567102884544532))
async def start(interaction):
    if not interaction.user.name in guilds_leaderboards[str(interaction.guild.id)]:

        guilds_leaderboards[str(interaction.guild.id)][interaction.user.name] = 100


        print("added starting money to: " + str(interaction.user) + " in guild: " + str(interaction.guild) + " and added them to the bot.")

        embed = discord.Embed(
            colour=discord.Color.brand_green(), 
            description="You are all set up now, "+str(interaction.user)+"! " + sever_settings_per_guild[str(interaction.guild.id)]["money_symbol"] + str(sever_settings_per_guild[str(interaction.guild.id)]["starting_money"]) + " has been added to your balance!",
            #description="added starting money: " + sever_settings_per_guild[str(interaction.guild.id)]["money_symbol"] + str(sever_settings_per_guild[str(interaction.guild.id)]["starting_money"]) + " to " + str(interaction.user) + ". you are all set up!",
            title= "Transaction Completed!"
        )   
    else:
        embed = discord.Embed(
            colour=discord.Color.brand_red(),
            description="You are already added to the bot!",
        )
    await interaction.response.send_message(embed=embed)
    
@tree.command(
        name="balance",
        description="shows your balance.",
        guild=discord.Object(id=1340567102884544532)
)
async def bal(interaction,user: discord.User=None):
    if user == interaction.user:
        waself = True
    else:
        waself = False
    if user == None:
            user = interaction.user
    try:
        embed = discord.Embed(
                colour=discord.Color.blurple(),
                title="Balance of Account: " + str(user),
                description=sever_settings_per_guild[str(interaction.guild.id)]["money_symbol"] + str(guilds_leaderboards[str(interaction.guild.id)][user.name])
            )
        
    except KeyError:
        if not waself:
            embed = discord.Embed(
                title="ERROR:",
                colour=discord.Color.brand_red(),
                description="That user doesnt have an account!"
            )
        if waself:
            embed = discord.Embed(
                title="ERROR:",
                colour=discord.Color.brand_red(),
                description="looks like you dont have an account! add one with the /start command! (make sure its the right one!)"
            )
    await interaction.response.send_message(embed=embed)

@tree.command(
    name="add-money",
    description="adds money to a certain user/account.",
    guild=discord.Object(id=1340567102884544532)
)
async def addm(interaction,user: discord.User,amount: int):
    if user == interaction.user:
        waself = True
    else:
        waself = False
    try:
        print("added " + str(sever_settings_per_guild[str(interaction.guild.id)]["money_symbol"]) + str(amount) + " to " + str(user.name) + "'s account." + " in guild: " + str(interaction.guild.name))
        guilds_leaderboards[str(interaction.guild.id)][user.name] += int(amount)
        embed = discord.Embed( 
                title="Transaction Completed!",
                colour=discord.Color.brand_green(),
                description="Added " + sever_settings_per_guild[str(interaction.guild.id)]["money_symbol"] + str(amount) + " to " + user.name + "'s account."
            )
    except KeyError:
        if not waself:
            embed = discord.Embed(
                title="ERROR:",
                colour=discord.Color.brand_red(),
                description="That user doesnt have an account!"
            )
        if waself:
            embed = discord.Embed(
                title="ERROR:",
                colour=discord.Color.brand_red(),
                description="looks like you dont have an account! add one with the /start command! (make sure its the right one!)"
            )
    await interaction.response.send_message(embed=embed)

@tree.command(
    name="remove-money",
    description="removes money from a certain user/account.",
    guild=discord.Object(id=1340567102884544532)
)
async def removem(interaction,user: discord.User,amount: int):
    if user == interaction.user:
        waself = True
    else:
        waself = False
    try:
        print("removed " + str(sever_settings_per_guild[str(interaction.guild.id)]["money_symbol"]) + str(amount) + " from " + str(user.name) + "'s account." + " in guild: " + str(interaction.guild.name))
        guilds_leaderboards[str(interaction.guild.id)][user.name] -= int(amount) #raises a "cant conaconate int to str execpttion"
        embed = discord.Embed( 
                title="Transaction Completed!",
                colour=discord.Color.brand_red(),
                description="Removed " + sever_settings_per_guild[str(interaction.guild.id)]["money_symbol"] + str(amount) + " from " + user.name + "'s account."
            )
    except KeyError:
        if not waself:
            embed = discord.Embed(
                title="ERROR:",
                colour=discord.Color.brand_red(),
                description="That user doesnt have an account!"
            )
        if waself:
            embed = discord.Embed(
                title="ERROR:",
                colour=discord.Color.brand_red(),
                description="looks like you dont have an account! add one with the /start command! (make sure its the right one!)"
            )
    await interaction.response.send_message(embed=embed)

@tree.command(
    name="pay",
    description="pays a certain ammount of money from your account(or one you own) into another.",
    guild=discord.Object(id=1340567102884544532)
)
async def paym(interaction,user: discord.User,amount: int):
    try:
        if guilds_leaderboards[str(interaction.guild.id)][interaction.user.name] - amount >= 0 and not interaction.user == user:
            print("Paid " + sever_settings_per_guild[str(interaction.guild.id)]["money_symbol"] + str(amount) + " from " + interaction.user.name + "'s account to " + user.name + "'s account." + " in guild: " + str(interaction.guild.name))
            guilds_leaderboards[str(interaction.guild.id)][interaction.user.name] -= int(amount)
            guilds_leaderboards[str(interaction.guild.id)][user.name] += int(amount)
            embed = discord.Embed( 
                    title="Transaction Completed!",
                    colour=discord.Color.dark_green(),
                    description="Paid " + sever_settings_per_guild[str(interaction.guild.id)]["money_symbol"] + str(amount) + " from " + interaction.user.name + "'s account to " + user.name + "'s account."
                )
        elif guilds_leaderboards[str(interaction.guild.id)][interaction.user.name] - amount < 0:
            embed = discord.Embed(
                title="Transaction Failed!",
                colour=discord.Color.brand_red(),
                description="Looks like you dont have enough money for that!"
            )
        elif interaction.user == user:
            embed = discord.Embed(
                title="Transaction Failed!",
                colour=discord.Color.brand_red(),
                description="You can't pay yourself!"
            )
    except KeyError:
        try:
            print("Error test: " + str(guilds_leaderboards[str(interaction.guild.id)][user.name]))
            
            print("hihihih")
            embed = discord.Embed(
                title="ERROR:",
                colour=discord.Color.brand_red(),
                description="looks like you dont have an account! add one with the /start command! (make sure its the right one!)"
            )
        except KeyError:
            embed = discord.Embed(
                title="ERROR:",
                colour=discord.Color.brand_red(),
                description="That user doesnt have an account!"
            )
            
    await interaction.response.send_message(embed=embed)

@tree.command(
    name="leaderboard",
    description="shows a leaderboard of all the people in the server.",
    guild=discord.Object(id=1340567102884544532)
)


async def list_leaderboard(interaction):
    leaderboard = []
    for player in guilds_leaderboards[str(interaction.guild.id)]:
        leaderboard.append(guilds_leaderboards[str(interaction.guild.id)][player])

    leaderboard.sort()
    leaderboard.reverse()
    published_leaderboard = []
    for i in range(len(leaderboard)):
        for player in guilds_leaderboards[str(interaction.guild.id)]:
            if guilds_leaderboards[str(interaction.guild.id)][player] == leaderboard[i]:
                print(player)
                published_leaderboard.append(f"{player}: {leaderboard[i]}")
                
    print(published_leaderboard)
    returned_str = ""
    for i, thing in enumerate(published_leaderboard):
        returned_str += f"{i}. {sever_settings_per_guild[str(interaction.guild.id)]['money_symbol']} {published_leaderboard[i]}\n"


    embed = discord.Embed(
        title="Leaderboard",
        description=returned_str,
        colour=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)


client.run(token)

# secret snail 🐌 (thanks enty. really adds some charm to the place.)