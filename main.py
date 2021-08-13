

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# เริ่มโค้ด github

import discord
from discord.utils import get
from discord import FFmpegPCMAudio
import asyncio
from async_timeout import timeout
from functools import partial
from discord.ext import commands
from datetime import datetime, timedelta
import itertools
from discord.ext.commands import cooldown, BucketType

import json
import os
import random






# wrapper / decorator

message1_lastseen = datetime.now()
message2_lastseen = datetime.now()
message3_lastseen = datetime.now()
message4_lastseen = datetime.now()
message5_lastseen = datetime.now()

bot = commands.Bot(command_prefix='=',help_command=None)
now = datetime.now()


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5" ## song will end if no this line
}



covidnumber = 0
bitcoinnumber = 0

#------------------------------------------------


@bot.event
async def on_message(message):
    global message_lastseen
    global covidnumber
    


    if message.content == '=makima': #คุยกับ makima
        print(str(message.author.name),'plume lonely')
        await message.channel.send(file=discord.File('yesorwoof.jpg'))
        await message.channel.send('say woof woof')

    elif message.content == 'woof woof': #คุยกับ makima ตอบ woof woof
        print(str(message.author.name),'plume lonelyanswer woof woof')
        await message.channel.send(file=discord.File('woof.jpg'))
        await message.channel.send('good boy')


    elif message.content == '=c':
        await message.channel.send('/covid') 



    elif now.hour < 12 and covidnumber == 0:
        print('send covid news')
        channel = bot.get_channel(873057668233834516) #channel id here
        covidnumber = 1
        
        await channel.send('/covid')
        covidnumber = 1




    elif now.hour > 12 and covidnumber == 1:
        covidnumber = 0
        print('set covidnumber = 0')

    await bot.process_commands(message)



############

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def help(ctx):   #ตั้งค่า embed
    emBed = discord.Embed(title='คำสั่งค้าบนายท่าน',Description='โชว์คำสั่งบอท', color= 0x42f5a7)
    emBed.add_field(name='=help', value='ดูคำสั่งบอท', inline=False)
    emBed.add_field(name='=money', value='ดูยอดเงินของคุณ', inline=True)
    emBed.add_field(name='=bag', value='ดูไอเทมที่คุณมี', inline=True)
    emBed.add_field(name='=lb', value='ดูอันดับคนรวยภายในเซิฟ', inline=False)
    emBed.add_field(name='=beg', value='ขอทาน', inline=False)
    emBed.add_field(name='=deposit (จำนวนเงิน)', value='ฝากเงิน', inline=True)
    emBed.add_field(name='=withdraw (จำนวนเงิน)', value='ถอนเงิน', inline=True)
    emBed.add_field(name='=slot (จำนวนเงิน)', value='เล่นslot ชนะได้เงิน2เท่า เเพ้เสียเงินตามที่ลง', inline=False)
    emBed.add_field(name='=rob (@ผู้ใช้)', value='ขโมยเงิน จากผู้เล่นอื่น', inline=False)
    emBed.add_field(name='=shop', value='ดูสินค้าในร้าน', inline=False)   
    emBed.add_field(name='=buy (ชื่อสินค้า)', value='ชื้อสินค้า', inline=True)
    emBed.add_field(name='=sell (ชื่อสินค้า)(จำนวน)', value='ขายสินค้า', inline=True)
    emBed.add_field(name='=send (@ผู้ใช้)(จำนวนเงิน)', value='โอนเงินไปให้ผู้เล่นคนอื่น', inline=False)
    emBed.add_field(name='=c', value='เช็คผู้ติดเชื้อโควิด', inline=False)
    emBed.add_field(name='=bitcoinwork', value='สั่งให้เครื่องขุดbitcoinทำงาน', inline=False)

    emBed.set_thumbnail(url = 'https://i.pinimg.com/736x/ff/59/54/ff595428ca33c592166ac608771e2b5f.jpg')
    await ctx.channel.send(embed = emBed)

##################################################################################################
#ระบบเงิน

mainshop = [{"name":"watch","price":1000, "description":"⌚สำหรับดูเวลา คำสั่ง =watch"},
            {"name":"hammer","price":800, "description":"🛠สามารถทำงานเป็นช่างได้ คำสั่ง =fix"},
            {"name":"motorcycle","price":3900, "description":"🛵ใช้เพื่อทำงานขนส่ง คำสั่ง =pizza,=grab,=lineman"},
            {"name":"rod","price":3000, "description":"🎣ใช้ตกปลา คำสั่ง =fish"},
            {"name":"pickaxe","price":7000, "description":"⛏ สำหรับขุดเหมือง คำสั่ง =mining"},
            {"name":"macbook","price":12000, "description":"💻สามารถใช้ทำงานออนไลน์ได้ =wfh"},
            {"name":"animalslot","price":59000, "description":"🎰slotสัตว์น่ารักคำสั่ง =slotam (จำนวนเงิน)"},
            {"name":"rtx3090","price":17990, "description":"🖥เครื่องขุดbitcoin ได้วันละ 5000บาท"},
            
            ]

        
@bot.command()
async def money(ctx):
    await open_account(ctx.author)
    
    users = await get_bank_data()
    user = ctx.author


    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title=f"{ctx.author.name}'s balance",color = discord.Color.red())
    em.add_field(name = "Wallet balance",value = wallet_amt)
    em.add_field(name = "Bank balance",value = bank_amt)
    await ctx.send(embed = em)

@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def beg(ctx): 
        
    await open_account(ctx.author)
    
    users = await get_bank_data()
    user= ctx.author

    earnings = random.randrange(51)

        

    await ctx.send(f"มีคนให้คุณ {earnings} บาท!!")

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json","w") as f:
        json.dump(users,f)

@bot.command()
@beg.error
async def begerror(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"ใจเย็นนะ ไอขอทาน",description=f"ต้องรอ {error.retry_after:.2f}s.")
        await ctx.send(embed=em)


@bot.command()
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("กรอกจำนวนเงิน")
        return

    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("นายท่านจำนวนเงินไม่พอนะ")
        return
    if amount<0:
        await ctx.send("นายท่าน อย่าล้อเล่นสิ ขอตัวเลขที่เป็นไปได้น้า")
        return

    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,"bank")

    await ctx.send(f":bangbang::bangbang:นายท่าน ถอนเงิน {amount} บาท!")


@bot.command()
async def deposit(ctx,amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("กรอกจำนวนเงิน")
        return

    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("นายท่านจำนวนเงินไม่พอนะ")
        return
    if amount<0:
        await ctx.send("นายท่าน อย่าล้อเล่นสิ ขอตัวเลขที่เป็นไปได้น้า")
        return

    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,"bank")

    await ctx.send(f":white_check_mark::white_check_mark: นายท่าน ฝากเงิน {amount} บาท!")

@bot.command()
async def send(ctx,member:discord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)

    if amount == None:
        await ctx.send("กรอกจำนวนเงิน")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("นายท่านจำนวนเงินไม่พอนะ")
        return
    if amount<0:
        await ctx.send("นายท่าน อย่าล้อเล่นสิ ขอตัวเลขที่เป็นไปได้น้า")
        return

    await update_bank(ctx.author,-1*amount,"bank")
    await update_bank(member,amount,"bank")

    await ctx.send(f"โอนเงิน {amount} บาท!")

@bot.command()
async def slot(ctx, amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("กรอกจำนวนเงิน")
        return

    bal = await update_bank(ctx.author)
    amount = int(amount)
    print("slot ",amount)
    if amount>bal[0]:
        await ctx.send("นายท่านจำนวนเงินไม่พอนะ")
        return
    if amount<0:
        await ctx.send("นายท่าน อย่าล้อเล่นสิ ขอตัวเลขที่เป็นไปได้น้า")
        return
    final = []
    for i in range(3):
        a = random.choice(["🍒","🍎","🍇","🍉","🎱","🌈","⭐"])

        final.append(a)

    await ctx.send(str(final))

    if final[0]== final[1] or final[0]== final[2]  or final[1]==final[2] :

        await update_bank(ctx.author,2*amount)
        await ctx.send(":smiley::smiley:นายท่าน ชนะ!!!")
    else:
        await update_bank(ctx.author,-1*amount)
        await ctx.send(":sob::sob:นายท่านเเพ้ ลองใหม่นะ~~")

@bot.command()
async def slotam(ctx, amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("กรอกจำนวนเงิน")
        return

    bal = await update_bank(ctx.author)
    amount = int(amount)
    amountslot = amount

    user = ctx.author
    users = await get_bank_data()
    slotrun = 0
    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    
    for item in bag:
        name = item["item"]
        amount = item["amount"]
        now = datetime.now()

        if name == "animalslot" and amount == 1:
            slotrun = 1

    print(amountslot)
    if amountslot>bal[0]:
        await ctx.send("นายท่านจำนวนเงินไม่พอนะ")
        return
    if amountslot<0:
        await ctx.send("นายท่าน อย่าล้อเล่นสิ ขอตัวเลขที่เป็นไปได้น้า")
        return
    final = []
    for i in range(3):
        a = random.choice(["🐮","🦁","🐯","🐼","🐻","🐭"])

        final.append(a)

    await ctx.send(str(final))

    if final[0]== final[1] or final[0]== final[2]  or final[1]==final[2] :
        if slotrun == 1:

            await update_bank(ctx.author,2*amountslot)
            await ctx.send("🏆โฮ่งโฮ่ง ชนะ!!!")
    elif slotrun == 0:
        await ctx.send("... นายท่านยังไม่มีไอเทมนะ")
    else:
        await update_bank(ctx.author,-1*amountslot)
        await ctx.send(":🗿โดนเสือค้าบเงิน ลองใหม่นะ~~")

# mainshop = [{"name":"⌚Watch","price":10000, "description":"สำหรับดูเวลา"},
#             {"name":"💻Mac-book","price":900000, "description":"สามารถใช้ทำงานออนไลน์ได้"},
#             {"name":"🕹Nintendo switch","price":100000, "description":"สามารถเล่นเกมได้"}]
                
                
@bot.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name=name,value = f"{price}| {desc}")

    await ctx.send(embed = em)

@bot.command()
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("มอคค่าไม่มีสินค้านั้นขายน้า~~~")
            return
        if res[1]==2:
            await ctx.send(f"นายท่านเงินไม่พอน้า {amount} {item}")
            return


    await ctx.send(f"นายท่านพึ่งชื้อ {amount} {item}")

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


@bot.command()
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

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def fish(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    
    for item in bag:
        name = item["item"]
        amount = item["amount"]
        now = datetime.now()

        if name == "rod":
    
                users = await get_bank_data()

                user= ctx.author

                a = random.choice(["x","o","o","x","x","x","u","t","t","x","x","p","l","g","v","a"])
                if a == 'x':

                    earnings = 400

                    print(type(earnings))
                    await open_account(ctx.author)
    
                    users = await get_bank_data()

                    user= ctx.author

                    users[str(user.id)]["wallet"] += earnings
                    

                    await ctx.send(f" 🐟 ได้ปลากระพง ได้รับ {earnings}")
                
                elif a == 'g':

                    earnings = 0
                    print(type(earnings))
                    await open_account(ctx.author)
    
                    users = await get_bank_data()

                    user= ctx.author

                    users[str(user.id)]["wallet"] += earnings
                    

                    await ctx.send(f" *** ได้ ขยะ ได้รับ {earnings}")

                elif a == 'p':

                    earnings = 380
                    print(type(earnings))

                    await open_account(ctx.author)
    
                    users = await get_bank_data()

                    user= ctx.author

                    users[str(user.id)]["wallet"] += earnings
                    

                    await ctx.send(f" 🐟 ได้ปลาทู ได้รับ {earnings}")

                elif a == 'l':

                    earnings = 320
                    print(type(earnings))


                    await open_account(ctx.author)
    
                    users = await get_bank_data()

                    user= ctx.author

                    users[str(user.id)]["wallet"] += earnings
                    

                    await ctx.send(f" 🐟 ได้ปลาสิ่ว ได้รับ {earnings}")

                elif a == "o":
                    earnings = 1000
                    print(type(earnings))

                    await open_account(ctx.author)
    
                    users = await get_bank_data()

                    user= ctx.author


                    users[str(user.id)]["wallet"] += earnings
                    
                    await ctx.send(f"🐠 ได้เเซลมอน ได้รับ {earnings}")
                elif a == "t":
                    earnings = 1200
                    print(type(earnings))

                    await open_account(ctx.author)
    
                    users = await get_bank_data()

                    user= ctx.author


                    users[str(user.id)]["wallet"] += earnings
                    
                    await ctx.send(f"🐙 ได้ปลาหมึก ได้รับ {earnings}")

                elif a == "v":
                    
                    earnings = 50


                    await open_account(ctx.author)
    
                    users = await get_bank_data()

                    user= ctx.author


                    users[str(user.id)]["wallet"] += earnings
                    
                    await ctx.send(f" ได้รับสาหร่าย {earnings}")

                elif a == "u":
                    
                    earnings = 1500
                    print(type(earnings))

                    await open_account(ctx.author)
    
                    users = await get_bank_data()

                    user= ctx.author


                    users[str(user.id)]["wallet"] += earnings
                    
                    await ctx.send(f"🦪 ได้อูนิ ได้รับ {earnings}")

                elif a == "a":
                    
                    earnings = 0
                    print(type(earnings))

                    await open_account(ctx.author)
    
                    users = await get_bank_data()

                    user= ctx.author


                    users[str(user.id)]["wallet"] += earnings
                    
                    await ctx.send(f"เจอ ปลาโลมา เเต่เป็นสัตว์ อนุรักษ์ เลยโดนเจ้าหน้าที่เก็บไป ได้รับ {earnings}")


                

        with open("mainbank.json","w") as f:
            json.dump(users,f)

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def mining(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    
    for item in bag:
        name = item["item"]
        amount = item["amount"]
        now = datetime.now()

        if name == "pickaxe":

                await open_account(ctx.author)
    
                users = await get_bank_data()

                user= ctx.author

                a = random.choice(["x","o","o","x","x","x","x","t","x","x","s","i","r","m","q"])
                if a == 'x':

                    earnings = 500

                    users[str(user.id)]["wallet"] += earnings
                    

                    await ctx.send(f" 💿 ได้ เเร่เงิน ได้รับ {earnings}")

                elif a == "o":
                    earnings = 1500


                    users[str(user.id)]["wallet"] += earnings
                    
                    await ctx.send(f"📀ได้ ทองคำ ได้รับ {earnings}")
                elif a == "s":
                    earnings = 2000


                    users[str(user.id)]["wallet"] += earnings
                    
                    await ctx.send(f"💍 ได้ เพรช ได้รับ {earnings}")
                
                elif a == "i":
                    earnings = 500


                    users[str(user.id)]["wallet"] += earnings
                    
                    await ctx.send(f"เจอเงินตกในเหมือง ได้รับ {earnings}")

                elif a == "r":
                    earnings = 450


                    users[str(user.id)]["wallet"] += earnings
                    
                    await ctx.send(f"📿 เจอสร้อยคอ ได้รับ {earnings}")

                elif a == "c":
                    earnings = 50


                    users[str(user.id)]["wallet"] += earnings
                    
                    await ctx.send(f".... เจอหิน ได้รับ {earnings}")
                
                elif a == "m":
                    earnings = 0


                    users[str(user.id)]["wallet"] += earnings
                    
                    await ctx.send(f"เจอ slime เลยวิ่งหนี ได้รับ {earnings}")
                elif a == "q":
                    earnings = 0


                    users[str(user.id)]["wallet"] += earnings
                    
                    await ctx.send(f"เจอ ฟอสซิลหายาก ราคา 100,000 บาท เเต่เเกะไม่ออก ")
                


                

        with open("mainbank.json","w") as f:
            json.dump(users,f)


@bot.command()
@mining.error
async def miningerror(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"ใจเย็นนะ นายท่าน",description=f"ต้องรอ {error.retry_after:.2f}s.")
        await ctx.send(embed=em)


@bot.command()
@fish.error
async def fisherror(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"ใจเย็นนะ นายท่าน",description=f"ต้องรอ {error.retry_after:.2f}s.")
        await ctx.send(embed=em)


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def fix(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    
    for item in bag:
        name = item["item"]
        amount = item["amount"]
        now = datetime.now()

        if name == "hammer":
                await open_account(ctx.author)
    
                users = await get_bank_data()

                user= ctx.author

                earnings = random.randrange(101)

                await ctx.send(f"ทำงานได้ {earnings} บาท!!")

                users[str(user.id)]["wallet"] += earnings

                with open("mainbank.json","w") as f:
                    json.dump(users,f)



@bot.command()
@fix.error
async def fixerror(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"ใจเย็นนะ คุณช่าง",description=f"ต้องรอ {error.retry_after:.2f}s.")
        await ctx.send(embed=em)


@bot.command()
@commands.cooldown(1, 40, commands.BucketType.user)
async def wfh(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    
    for item in bag:
        name = item["item"]
        amount = item["amount"]
        now = datetime.now()

        if name == "macbook":
            global message3_lastseen

            await open_account(ctx.author)
    
            users = await get_bank_data()

            user= ctx.author

            earnings = random.randrange(2001)

            await ctx.send(f"ขายของออนไลน์ได้ {earnings} บาท!!")

            users[str(user.id)]["wallet"] += earnings

        with open("mainbank.json","w") as f:
                    json.dump(users,f)

@bot.command()
@wfh.error
async def wfherror(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"ใจเย็นนะ เเม่ค้าออนไลน์",description=f"ต้องรอ {error.retry_after:.2f}s.")
        await ctx.send(embed=em)



@bot.command()
async def watch(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    
    for item in bag:
        name = item["item"]
        amount = item["amount"]
        now = datetime.now()

        if name == "watch":
            await ctx.send(now) 
        

@bot.command()
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
                price = 0.9* item["price"]
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

@bot.command(aliases = ["lb"])
async def leaderboard(ctx,x = 3):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = discord.Embed(title = f"Top {x} รวยที่สุดในเซิฟ" , description = "ยอดเงินมาจากbankเเละwallet",color = discord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = bot.get_user(id_) 
        memberstr= await bot.fetch_user(id_)
        
 
        em.add_field(name = f"{index}. {memberstr}" , value = f"{amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)

@bot.command()
@commands.cooldown(1, 1440,commands.BucketType.guild)
async def bitcoinwork(ctx):

    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        print(user)
        idbitcoin = user

        try:
            bag = users[str(user)]["bag"]
        except:
            bag = []

        for item in bag:
            name = item["item"]
            amount = item["amount"]
            

            if name == "rtx3090":
                    memberbitcoin = await bot.fetch_user(user)
                    await open_account(memberbitcoin)
                    
                    
                    users = await get_bank_data()

                    user= memberbitcoin

                    earnings = 5000*amount

                    await ctx.send(f"bitcoin ได้ {earnings} บาท!!")

                    users[str(idbitcoin)]["wallet"] += earnings

            with open("mainbank.json","w") as f:
                json.dump(users,f)
        
    
    await ctx.send("เครื่องขุดbitcoinกำลังทำงาน")

@bot.command()
@bitcoinwork.error
async def bitcoinworkerror(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"เครื่องขุดbitcoinทำงานไปเเล้ว",description=f"ต้องรอ {error.retry_after:.2f}s.")
        await ctx.send(embed=em)





@bot.command()
async def rob(ctx,member:discord.Member):
    await open_account(ctx.author)
    await open_account(member)

    bal = await update_bank(member)
    bal2 = await update_bank(ctx.author)

    if bal[0]<100:
        await ctx.send("คู่กรณีเงินไม่พอ")
        return
    if bal2[0]<100:
        await ctx.send("คุณเงินไม่พอ")
        return
    a = random.choice(["o","x","p"])
    if a == 'x':

        earnings = random.randrange(0, bal[0])

        await update_bank(ctx.author,earnings)
        await update_bank(member,-1*earnings)

        await ctx.send(f":sunglasses::sunglasses:คุณ ขโมย สำเร็จ ได้รับ {earnings}")

    elif a == 'p':

        earnings = random.randrange(0, bal2[0])


        await update_bank(ctx.author,-1*earnings)
        await update_bank(member,earnings)
        await ctx.send(f"ว้า...โดนจับได้ ต้องให้เงินคนที่โดนปล้น จำนวน {earnings}")
    

    else:
        
        earnings = random.randrange(0, bal2[0])


        await update_bank(ctx.author,-1*earnings)
        await update_bank(member,earnings)
        await ctx.send(f"ว้า...โดนจับได้ ต้องให้เงินคนที่โดนปล้น จำนวน {earnings}")




    
    


        
    


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json","w") as f:
        json.dump(users,f)
    return True

async def get_bank_data():
    with open("mainbank.json","r") as f:
        users = json.load(f)
    return users

async def update_bank(user,change = 0,mode = "wallet",):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return bal

@bot.command()
async def pizza(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    
    for item in bag:
        name = item["item"]
        amount = item["amount"]
        now = datetime.now()

        if name == "motorcycle":
                await open_account(ctx.author)
    
                users = await get_bank_data()

                user= ctx.author

                earnings = random.randrange(151)

                await ctx.send(f"ส่งพิซซ่าได้ {earnings} บาท!!")

                users[str(user.id)]["wallet"] += earnings

                with open("mainbank.json","w") as f:
                    json.dump(users,f)
@bot.command()
async def grab(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    
    for item in bag:
        name = item["item"]
        amount = item["amount"]
        now = datetime.now()

        if name == "motorcycle":
                await open_account(ctx.author)
    
                users = await get_bank_data()

                user= ctx.author

                earnings = random.randrange(101)

                await ctx.send(f"ส่งอาหารได้ {earnings} บาท!!")

                users[str(user.id)]["wallet"] += earnings

                with open("mainbank.json","w") as f:
                    json.dump(users,f)

@bot.command()
async def lineman(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    
    for item in bag:
        name = item["item"]
        amount = item["amount"]
        now = datetime.now()

        if name == "motorcycle":
                await open_account(ctx.author)
    
                users = await get_bank_data()

                user= ctx.author

                earnings = random.randrange(121)

                await ctx.send(f"เป็นlinemanได้ {earnings} บาท!!")

                users[str(user.id)]["wallet"] += earnings

                with open("mainbank.json","w") as f:
                    json.dump(users,f)





#####################################################
bot.run('Token')
