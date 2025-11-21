import discord, os, random, requests, json, giphy_client
from giphy_client.rest import ApiException
from pyowm.owm import OWM
from discord.ext import commands
from bs4 import BeautifulSoup
from webserver import keep_alive
import praw
import wikipedia

intents = discord.Intents().default()
intents.members = True
client = commands.Bot(command_prefix='_', intents=intents)

@client.event
async def on_ready():
  print('bot is ready')
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a giraffe"))

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    # def convert(seconds):
    #   seconds = seconds % (24 * 3600)
    #   hour = seconds // 3600
    #   seconds %= 3600
    #   minutes = seconds // 60
    #   seconds %= 60

    #   return "%d:%02d:%02d" % (hour, minutes, seconds)

    def convert(seconds):
      t = seconds
      day = t // (24 * 3600)
      t = t % (24 * 3600)
      hour = t // 3600
      t %= 3600
      minutes = t// 60
      t %= 60
      seconds = t
      return "%d:%d:%d:%d" % (day, hour, minutes, seconds)
    
    # msg = '**Still on cooldown**, please try again in {:.1f}s'.format(error.retry_after)
    msg = f'still on cooldown. TAKE IT SLOOOOW FAM! you will have to wait for `{convert(error.retry_after)}`'
    slowdownmbd = discord.Embed(
      colour = discord.Colour.red(),
      title='Slow it down man!',
      description=msg
    )
    await ctx.send(embed=slowdownmbd)

@client.command(help='returns a meme')
@commands.cooldown(1,15,commands.BucketType.user)
async def meme(ctx, subred=str(random.choice(['memes', 'meme', 'dankmemes']))):
  async with ctx.typing():
    reddit = praw.Reddit(client_id='cyfRCWWtKHgLPQ',
                        client_secret=str(os.getenv('CLIENT_SECRET')),
                        username='Vegetable-History544',
                        password=str(os.getenv('REDDIT')),
                        user_agent='lolGamer',
                         check_for_async=False)

    all_subs_list = []
    sub = reddit.subreddit(subred)

    top = sub.top(limit=10)
    new = sub.new(limit=10)

    for submissions in top:
      all_subs_list.append(submissions)
    
    for new_meme in new:
      all_subs_list.append(new_meme)

    random_meme = random.choice(all_subs_list)

    title = random_meme.title
    url = random_meme.url

    meme_mbd = discord.Embed(colour=0x95efcc, title=title)
    meme_mbd.set_image(url=url)

  await ctx.send(embed=meme_mbd)


@client.command(
    aliases=['tmp'],
    help=
    'returns the temperature about a place only if the country code is given. Ex- London,GB'
)
@commands.cooldown(1,15,commands.BucketType.user)
async def temp(ctx, *, place):
	owm = OWM(str(os.getenv('OWM_API')))
	mgr = owm.weather_manager()
	weather = mgr.weather_at_place(place).weather
	temp_dict_celsius = weather.temperature('celsius')
	temp = temp_dict_celsius.get("temp")
	temp_max = temp_dict_celsius.get("temp_max")
	temp_min = temp_dict_celsius.get("temp_min")
	temp_min = str(temp_min)
	temp = str(temp)
	temp_max = str(temp_max)

	weather_mbd = discord.Embed(
	    colour=0x95efcc,
	    title=f'{place} Weather:',
	    description='Here are the Results for the weather in (celsius):')

	weather_mbd.add_field(name='Temperature:', value=temp)
	weather_mbd.add_field(name='Maximum temperature:', value=temp_max)
	weather_mbd.add_field(name='Minimum temperature:', value=temp_min)
	# weather_mbd.add_field(name='Rain:', value=rain)

	await ctx.send(embed=weather_mbd)


def get_wiki_search(search):
	return str(wikipedia.summary(search, 2))


@client.command(help='returns information of the user input')
@commands.cooldown(1,15,commands.BucketType.user)
async def wiki(ctx, *, search):
	wiki_mbd = discord.Embed(
	    colour=0x95efcc,
	    title=f'{ctx.message.author.name} searched wikipedia:',
	    description=f'About: {search} \n\nResults: \n{get_wiki_search(search)}'
	)
	await ctx.send(embed=wiki_mbd)


@client.command()
@commands.cooldown(1,15,commands.BucketType.user)
async def hug(ctx, user: discord.Member):
	api_instance = giphy_client.DefaultApi()

	try:
		api_response = api_instance.gifs_search_get(os.getenv('GIF_API'),
		                                            'hug',
		                                            limit=1)
		lst = list(api_response.data)
		gif = random.choice(lst)
		hug_mbd = discord.Embed(
		    colour=0x95efcc,
		    title=f'{ctx.message.author.name} hugs {user.name}:')
		await ctx.send(embed=hug_mbd)
		await ctx.channel.send(gif.embed_url)
	except ApiException as e:
		print('Exception when calling API')


@client.command(help='kills the user that is mentioned')
@commands.cooldown(1,15,commands.BucketType.user)
async def kill(ctx, user: discord.Member):

	api_instance = giphy_client.DefaultApi()

	try:
		api_response = api_instance.gifs_search_get(os.getenv('GIF_API'),
		                                            'kill',
		                                            limit=1)
		lst = list(api_response.data)
		gif = random.choice(lst)
		kill_mbd = discord.Embed(
		    colour=0x95efcc,
		    title=f'{ctx.message.author.name} attacks {user.name}:')
		await ctx.send(embed=kill_mbd)
		await ctx.channel.send(gif.embed_url)
	except ApiException as e:
		print('Exception when calling API')


@client.command()
@commands.cooldown(1,15,commands.BucketType.user)
async def kiss(ctx, user: discord.Member):

	api_instance = giphy_client.DefaultApi()

	try:
		api_response = api_instance.gifs_search_get(os.getenv('GIF_API'),
		                                            'kiss',
		                                            rating='g',
		                                            limit=1)
		lst = list(api_response.data)
		gif = random.choice(lst)
		kiss_mbd = discord.Embed(
		    colour=0x95efcc,
		    title=f'{ctx.message.author.name} kisses {user.name}:')
		await ctx.send(embed=kiss_mbd)
		await ctx.channel.send(gif.embed_url)
	except ApiException as e:
		print('Exception when calling API')


@client.command()
@commands.cooldown(1,15,commands.BucketType.user)
async def slap(ctx, user: discord.Member):
	api_instance = giphy_client.DefaultApi()

	try:
		api_response = api_instance.gifs_search_get(os.getenv('GIF_API'),
		                                            'slap',
		                                            limit=1)
		lst = list(api_response.data)
		gif = random.choice(lst)
		slap_mbd = discord.Embed(
		    colour=0x95efcc,
		    title=f'{ctx.message.author.name} attacks {user.name}:')
		await ctx.send(embed=slap_mbd)
		await ctx.channel.send(gif.embed_url)
	except ApiException as e:
		print('Exception when calling API')


@client.command(help='returns a news article')
@commands.cooldown(1,15,commands.BucketType.user)
async def news(ctx):
  async with ctx.typing():
    reddit = praw.Reddit(client_id='cyfRCWWtKHgLPQ',
                        client_secret=str(os.getenv('CLIENT_SECRET')),
                        username='Vegetable-History544',
                        password=str(os.getenv('REDDIT')),
                        user_agent='lolGamer',
                         check_for_async=False)

    all_subs_list = []
    sub = reddit.subreddit('worldnews')

    top = sub.new(limit=25)

    for submissions in top:
      all_subs_list.append(submissions)

    random_news = all_subs_list[0]

    title = random_news.title

    news_mbd = discord.Embed(colour=0x95efcc, title=title)

    await ctx.send(embed=news_mbd)


# mod commands

@client.command()
@commands.has_permissions(ban_members=True)

async def ban(ctx, member: discord.Member, *, reason):
	await member.ban(reason=reason)
	ban_mbd = discord.Embed(colour=0x95efcc,
	                        title=f'{member.name} is Banned from this server',
	                        description='These are the details:')
	ban_mbd.add_field(name='Banned User:', value=f'{member.mention}')
	ban_mbd.add_field(name='Banned By:', value=f'{ctx.message.author.mention}')
	ban_mbd.add_field(name='Reason:', value=f'{reason}')

  
	await ctx.send(embed=ban_mbd)


@client.command(
    aliases=['cl'],
    help='clears a specific number of messages if the user has perms')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount)


@client.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="muted", description=f"{member.mention} was muted ", colour=discord.Colour.purple())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(embed=embed)


@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
  try:
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await member.send(f" you have unmuted from: - {ctx.guild.name}")
    embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",colour=discord.Colour.light_gray())
    await ctx.send(embed=embed)
  except Exception:
    await ctx.send(f'{member.mention} is not muted')


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason):
	await member.kick(reason=reason)
	kick_mbd = discord.Embed(colour=0x95efcc,
	                         title=f'{member.name} is Kicked from this server',
	                         description='These are the details:')
	kick_mbd.add_field(name='Kicked User:', value=f'{member.mention}')
	kick_mbd.add_field(name='Kicked By:',
	                   value=f'{ctx.message.author.mention}')
	kick_mbd.add_field(name='Reason:', value=f'{reason}')


	await ctx.send(embed=kick_mbd)
  
def get_data():
  with open('warns.json', 'r') as file:
    users = json.load(file)
  return users


@client.command()
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention}')


@client.command()
@commands.has_permissions(manage_messages=True)
async def bypass(ctx, member: discord.Member):
	bypassmbd = discord.Embed(
	    colour=0x95efcc,
	    title='Bypass Warning:',
	    description=
	    "Please avoid bypassing the Antiswear bot's check. Refrain from using profanity."
	)

	await ctx.send(embed=bypassmbd)

@client.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason='None'):
    warnmbd = discord.Embed(colour=0x95efcc,
                            title=f'{member.mention} is Warned',
                            description='Here are the details:')
    warnmbd.add_field(name='Warned Member:', value=f'{member.mention}')
    warnmbd.add_field(name='Warned By:', value=f'{ctx.message.author.mention}')
    warnmbd.add_field(name='Reason:', value=f'{reason}')
    await ctx.send(embed=warnmbd)
    users = get_data()
    target = member
    users[str(target.id)] += 1

    with open('warns.json', 'w') as file:
        json.dump(users, file)
    print(f'{target.id}')




@client.command()
@commands.has_permissions(manage_messages=True)
async def profile(ctx, member: discord.Member):
	pfpmbd = discord.Embed(
	    colour=0x95efcc,
	    title='PFP Warning:',
	    description=
	    "Please change ur Profile Picture as it doesn't comply with the server rules. This server is a SFW community thus profane or Nsfw profile pictures are not allowed. Not following these actions will lead to a kick being issued."
	)

	await ctx.send(embed=pfpmbd)

@client.command()
@commands.has_permissions(manage_channels=True)
async def masslockdown(ctx):
    for channel in ctx.guild.text_channels:
      await channel.set_permissions(ctx.guild.default_role,send_messages=False)
    await ctx.send('all of the text channels are on lockdown')

@client.command()    
@commands.has_permissions(manage_channels=True)
async def lockdown(ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('Channel locked.')


@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + " ***has been unlocked.***")

@client.command()
@commands.has_permissions(manage_messages=True)
async def poll(ctx, *, message):
  await ctx.message.delete()
  embd=discord.Embed(
    colour = discord.Colour.purple(),
    title='TRACKER YT POLL!!',
    description=str(message)
  )
  msg = await ctx.channel.send(embed=embd)
  await msg.add_reaction('👍')
  await msg.add_reaction('👎')

@client.command(aliases=['ui'])
@commands.has_permissions(manage_messages=True)
async def userinfo(ctx, *, member:discord.Member=None):
  if member is None:
    await ctx.send('pls type in a member to find user info about')
  else:
    about_mbd = discord.Embed(
      title="User Information",
      colour = discord.Colour.purple(),
      description='Here are the details:'
    )

    fields = [('ID:', member.id),
              ('Name:', str(member.name)),
              ('Top Role:', member.top_role.mention),
              ('Status:', str(member.status).title()),
              ('Created At:', member.created_at.strftime("%d/%m/%Y %H:%M:%S")),
              ('Joined At:', member.joined_at.strftime("%d/%m/%Y %H:%M:%S")),
              ]
    for name, value in fields:
      about_mbd.add_field(name=name, value=value)
    
    await ctx.send(embed=about_mbd)

@client.command(aliases=['setslowmode'])
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"the slowmode delay has been set to {seconds} in this channel")

@client.command()
@commands.has_permissions(manage_messages=True)
async def warns(ctx, target:discord.Member=None):
  if target is None:
    with open('warns.json', 'r') as file:
      users=json.load(file)
      await ctx.send(users)
  else:
    with open('warns.json', 'r') as file:
      users = json.load(file)
      ui = users[str(target.id)]
      await ctx.send(f'{target.mention} has **{ui}** warns')





mainshop = [{"name":"Watch","price":100,"description":"Time"},
            {"name":"Laptop","price":1000,"description":"Work"},
            {"name":"PC","price":10000,"description":"Gaming"},
            {"name":"Ferrari","price":100000,"description":"Sports Car"}]

@client.command(aliases=['bal'])
async def balance(ctx, member:discord.Member = None):
  if member == None:
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title=f'{ctx.author.name} Balance',color = discord.Color.red())
    em.add_field(name="Wallet Balance", value=wallet_amt)
    em.add_field(name='Bank Balance',value=bank_amt)
    await ctx.send(embed= em)
  else:
    await open_account(member)
    user = member

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title=f'{member.name} Balance',color = discord.Color.red())
    em.add_field(name="Wallet Balance", value=wallet_amt)
    em.add_field(name='Bank Balance',value=bank_amt)
    await ctx.send(embed= em)


@client.command(aliases=['give'])
async def send(ctx,member : discord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)
    if amount == 'all':
        amount = bal[0]

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,-1*amount,'wallet')
    await update_bank(member,amount,'wallet')
    await ctx.send(f'{ctx.author.mention} You gave **{member.name}** {amount} coins')


@client.command(aliases=['rb'])
@commands.cooldown(1,45,commands.BucketType.user)
async def rob(ctx,member : discord.Member):
    await open_account(ctx.author)
    await open_account(member)
    bal = await update_bank(member)
    ba = await update_bank(ctx.message.author)


    if bal[0]<100:
        await ctx.send('It is useless to rob him :(')
        return

    
    random_select = random.choice(['rob', 'no'])

    if random_select == 'rob':
      earning = random.randrange(0,bal[0])
      await update_bank(ctx.author,earning)
      await update_bank(member,-1*earning)
      await ctx.send(f'{ctx.author.mention} You robbed {member.name} and got {earning} coins')
    else:
      if ba[0]>500:
        loosing = random.randrange(0,ba[0])
        await update_bank(ctx.author,-1*loosing)
        await update_bank(member,1*loosing)
        await ctx.send(f'{ctx.message.author.mention} hahaha, you got caught. you gave {member.name} {loosing} coins')
      else:
        await ctx.send('you need to have 500 in your wallet')





@client.command()
@commands.cooldown(1,45,commands.BucketType.user)
async def slots(ctx,amount = None):
    await ctx.send(f'{ctx.message.author} you have slotted {amount} please wait for the results')
    await open_account(ctx.author)
    slot_list = ['X','O','Q']
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return
    final = []
    for i in range(3):
        a = random.choice(slot_list)

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
        await update_bank(ctx.author, -1*amount)
        await update_bank(ctx.author,2*amount)
        await ctx.send(f'You won {2*amount}:) {ctx.author.mention}')
    elif len(final)==1:
      await update_bank(ctx.author, -1*amount)
      await ctx.send(f'You won {5*amount}!! DEPOSIT IT OR ELSE SOMEONE WILL ROB YOU!')
    else:
        await update_bank(ctx.author,-1*amount)
        await ctx.send(f'You lost {1*amount} :( {ctx.author.mention}')


@client.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name = name, value = f"${price} | {desc}")

    await ctx.send(embed = em)



@client.command()
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return


    await ctx.send(f"You just bought {amount} {item}")


@client.command()
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title = "Bag")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)    

    await ctx.send(embed = em)


async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]
    

@client.command()
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have {amount} {item} in your bag.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have {item} in your bag.")
            return

    await ctx.send(f"You just sold {amount} {item}.")

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.7* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]


@client.command(aliases = ["lb"])
async def leaderboard(ctx,x = 1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = discord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open('mainbank.json','w') as f:
        json.dump(users,f)

    return True


async def get_bank_data():
    with open('mainbank.json','r') as f:
        users = json.load(f)

    return users


async def update_bank(user,change=0,mode = 'wallet'):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open('mainbank.json','w') as f:
        json.dump(users,f)
    bal = users[str(user.id)]['wallet'],users[str(user.id)]['bank']
    return bal



@client.command()
@commands.cooldown(1,45,commands.BucketType.user)
async def beg(ctx):
  amount = random.randint(0,1000)
  await open_account(ctx.author)
  user = ctx.author
  users = await get_bank_data()

  users[str(user.id)]["wallet"] += amount

  if amount == 0:
    await ctx.send("lol you didnt get anything. Sucks to be you")

  else:
    begmbd = discord.Embed(
      title=f"{ctx.message.author.name}'s begging results",
      description=f'Some random dude gave {ctx.message.author.mention} {amount} coins',
      colour = discord.Colour.red()
    )
    await ctx.send(embed=begmbd)
  
  with open("mainbank.json",'w') as f:
    json.dump(users,f)

@client.command(aliases=['dep'])
async def deposit(ctx, amount=None):
  if amount.strip().isdigit():
    try:
      await open_account(ctx.author)
      users = await get_bank_data()
      user = ctx.author

      wallet_amt_user = users[str(user.id)]["wallet"]
      
      users[str(user.id)]["wallet"] -= int(amount)
      if users[str(user.id)]["wallet"] >= 0:
        users[str(user.id)]["bank"] += int(amount)
        bank_amt = users[str(user.id)]["bank"]
        

        with open("mainbank.json",'w') as f:
          json.dump(users,f)
        
        depmdb = discord.Embed(
          title=f'{ctx.message.author.name} Deposited {amount}',
          description=f'you now have {bank_amt} in your bank',
          colour = discord.Colour.red()
        )
        await ctx.send(embed=depmdb)
      else:
        await ctx.send('you dont even have that much money in your wallet')
    except Exception:
      await ctx.send('a valid number must be given to deposit.')

  elif amount.lower()=='all':
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author

    wallet_amt_user = users[str(user.id)]["wallet"]
    
    users[str(user.id)]["bank"] += users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]
    users[str(user.id)]["wallet"] = 0

    with open("mainbank.json",'w') as f:
      json.dump(users,f)
    
    depmdb = discord.Embed(
      title=f'{ctx.message.author.name} Deposited {wallet_amt_user}',
      description=f'you now have {bank_amt} in your bank',
      colour = discord.Colour.red()
    )
    await ctx.send(embed=depmdb)
  
  
  else:
    await ctx.send("bruh, you need to type in 'all' or some other number along with the command")


@client.command(aliases=['with'])
async def withdraw(ctx, amount):
  if amount.strip().isdigit():
    try:
      await open_account(ctx.author)
      users = await get_bank_data()
      user = ctx.author

      wallet_amt_user = users[str(user.id)]["wallet"]
      users[str(user.id)]["bank"] -= int(amount)
      if users[str(user.id)]["bank"] >= 0:
        users[str(user.id)]["wallet"] += int(amount)
        wallet_amt_user = users[str(user.id)]["wallet"]
        

        with open("mainbank.json",'w') as f:
          json.dump(users,f)
        
        depmdb = discord.Embed(
          title=f'{ctx.message.author.name} Has Withdrawn {amount}',
          description=f'you have {wallet_amt_user} in your wallet',
          colour = discord.Colour.red()
        )
        await ctx.send(embed=depmdb)
      else:
        await ctx.send('you dont even have that much money in your bank')
    except Exception:
      await ctx.send('a valid number must be given to witdrawn.')

  elif amount.lower()=='all' or amount.lower()=='max':
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    

    bank_amt_user = users[str(user.id)]["bank"]
    users[str(user.id)]["bank"] -= bank_amt_user
    users[str(user.id)]["wallet"] += bank_amt_user
    wallet_amt_user = users[str(user.id)]["wallet"]

    with open("mainbank.json",'w') as f:
      json.dump(users,f)
    
    depmdb = discord.Embed(
      title=f'{ctx.message.author.name} Has Withdrawn {bank_amt_user}',
      description=f'you have {wallet_amt_user} in your wallet',
      colour = discord.Colour.red()
    )
    await ctx.send(embed=depmdb)
  
  
  else:
    await ctx.send("bruh, you need to type in 'all' or some other number along with the command")

# @client.command(aliases=['with'])
# async def withdraw(ctx, amount):
#   amount = int(amount)
#   await open_account(ctx.author)
#   users = await get_bank_data()
#   user = ctx.author

#   bank_mt = users[str(user.id)]["bank"]

#   if amount > bank_mt:
#     await ctx.send(f'{ctx.message.author.mention}, What are you thinking tbh; you dont even have that much money')
  
#   elif amount < 0:
#     await ctx.send('dont even try to trick me. you cant withdraw negative money')
#   else:
#     users[str(user.id)]["bank"] -= amount
#     users[str(user.id)]["wallet"] += amount

#     with open("mainbank.json",'w') as f:
#       json.dump(users,f)
    
#     withmbd = discord.Embed(
#       title=f'{ctx.message.author.name} withdrew {amount}',
#       description='Type **<prefix>bal** to check the balance that you have in your account!',
#       colour = discord.Colour.red()
#     )
    
#     await ctx.send(embed = withmbd)

@client.command()
@commands.cooldown(1,86400,commands.BucketType.user)
async def daily(ctx):
  await open_account(ctx.author)
  users = await get_bank_data()
  user = ctx.author

  random_bonus = random.randint(1000, 20000)

  total = random_bonus + 20000
  
  users[str(user.id)]["wallet"] += total

  with open("mainbank.json",'w') as f:
      json.dump(users,f)
  
  dailymbd = discord.Embed(
    title=f'{ctx.message.author.mention} got {total}',
    description='Noice',
    colour = discord.Colour.red()
  )
  await ctx.send(embed=dailymbd)

@client.command()
@commands.cooldown(1,3600,commands.BucketType.user)
async def hourly(ctx):
  await open_account(ctx.author)
  users = await get_bank_data()
  user = ctx.author

  random_bonus = random.randint(1000, 2000)

  total = random_bonus + 500
  
  users[str(user.id)]["wallet"] += total

  with open("mainbank.json",'w') as f:
      json.dump(users,f)
  
  dailymbd = discord.Embed(
    title=f'{ctx.message.author.mention} got {total}',
    description='Noice',
    colour = discord.Colour.red()
  )
  await ctx.send(embed=dailymbd)

@client.command()
@commands.cooldown(1,604800,commands.BucketType.user)
async def weekly(ctx):
  await open_account(ctx.author)
  users = await get_bank_data()
  user = ctx.author

  random_bonus = random.randint(1000, 40000)

  total = random_bonus + 50000
  
  users[str(user.id)]["wallet"] += total

  with open("mainbank.json",'w') as f:
      json.dump(users,f)
  
  dailymbd = discord.Embed(
    title=f'{ctx.message.author.mention} got {total}',
    description='Noice',
    colour = discord.Colour.red()
  )
  await ctx.send(embed=dailymbd)

@client.command()
async def fun(ctx):
  string='_meme : returns a meme from a specified subreddit \n\n_temp : returns the temperature of any place specific. ex: _temp London, GB \n\n_wiki : returns 2 lines about a specific thing. \n\n_hug : returns appropriate messages. \n\n_kill : returns appropriate messages. \n\n_kiss : returns appropriate messages. \n\n_slap : returns appropriate messages.\n\n_news : returns news'

  fun_mbd = discord.Embed(
    colour = 0x95efcc,
    title='Fun Commands:',
    description=string
  )
  await ctx.send(embed=fun_mbd)

@client.command()
async def mod(ctx):
  string="_warn : warns the user specified. \n\n_mute : mutes the member specified. \n\n_unmute : unmutes the member specified. \n\n_kick : kicks the member specified. \n\n_ban : bans the member specified. \n\n_clear : clears the amount of messages specified. \n\n_nick : changes the user's nick name. \n\n_profile : warns the user about their pfp. \n\n_bypass : warns the user for bypassing the black-listed words. \n\n_lockdown : specified channel goes on lockdown. \n\n_unlock : unlocks the specified channel. \n\n_userinfo : returns all the important information of the user. \n\n_masslockdown : the entire server goes on lockdown. \n\n_massunlock : entire server unlocks."
  mod_mbd = discord.Embed(
    colour = 0x95efcc,
    title='Moderation Commands:',
    description=string
  )
  await ctx.send(embed=mod_mbd)

@client.command()
async def currency(ctx):
  string='_bag : shows your inventory.\n\n_balance : shows balance. \n\n_beg : begs people for coins. \n\n_buy : buys an item from the shop. \n\n_deposit : deposits money into the users bank. \n\n_lb : show the leaderboard for the richest people in the server. \n\n_rob : robs a specified user. \n\n_sell : sells a specific item. \n\n_send : sends money to a specified user. \n\n_shop : shows the shop. \n\n_slots : does a random spin for rewards. \n\n_with : withdraws money from the bank. \n\n_daily : gives daily rewards. \n\n_weekly, _daily, _hourly : gives coins to users on time intervals'
  curr_mbd = discord.Embed(
    colour = 0x95efcc,
    title='Currency Commands:',
    description=string
  )
  await ctx.send(embed=curr_mbd)

keep_alive()
client.run(os.getenv('TOKEN'))