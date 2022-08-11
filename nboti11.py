import time
import discord
from discord.ext import commands
from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption

bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())
DiscordComponents(bot)

mainchannel = 781186990724743199
serverid= 685363496015495248
automute = 1006581023217295470
banhistorychannel = 1006581147037343744
automutehistorychannel = 1006581231435128892
unmutehistorychannel = 1006581313781899334
mutehistorychannel = 1006581375119413269
words = ["عيرج","عيرك","عير","الكلبه","ks","زب","ازبار","كس","امصك","بطيزي","كلبه","كسهه","طيزهه","خايبه","خايب","بعص","ابعصج","ابعصك","انيجك","انيكك","بعصها","بورن هوب","porn hub","fuke","ثدى","ديك","ديكك","طيزج","كحبه","كحب","كحاب","pussy","PUSSY","kiss","Kiss","Pussy","KISS","ass","Ass","ASS","PuSsY","AsS","duck","DUCK","Duck","DuCk","ASs","aSS","pUssY","kISS","KIss","KISs","KIss","FUKE","Fuke","FukE","الذينه","FuKE","ثديك","جلق","المني","زبك","زبج","كسك","كسج","انيجج","ابوسج","بوسك","Piss"," Dick", "Asshole ‍","b*tch", "Bastard"," Bitch","Damn","DICK","dICk","diCK","BETCH","betch","bitch"]

@bot.listen()
async def on_ready():
    await bot.get_channel(mainchannel).send("online")
    await bot.change_presence(status=discord.Status.idle,activity=discord.activity.Game('!help_me'))

@bot.listen()
async def on_message(message):
    for word in message.content.split():
        if word in words:
            await message.delete()
            g = message.guild
            r = await g.create_role(name=f"{message.author.name} muted")
            await message.author.add_roles(r)
            for channel in g.channels:
                await channel.set_permissions(target=r, speak=False , send_messages=False)
            mn = message.author
            embed = discord.Embed(title =f" تم اسكات {mn} ", color=discord.Color.blue())
            embed.add_field(name="السبب",value="**كلمات مسيئه[سب]**")
            embed.add_field(name="العضو",value=mn.mention,inline=False)
            embed.add_field(name="الكلمه",value=f"**||{word}||**",inline=False)
            embed.add_field(name="ㅤ",value="**اختر احد الاجراىات الاتيه**",inline=False)
            em = await bot.get_channel(int(automute)).send(embed=embed,components=[
                [Button(label="حظر العضو",style=4,custom_id="ban"),
                Button(label="ابقاء الميوت",style=2,custom_id="keep"),
                Button(label="فك الاسكات",style=3,custom_id="un")]
            ])
            intr = await bot.wait_for("Button_click")
            if intr.custom_id == "ban":
                await message.author.ban(reason="**كلمات مسيئه[سب]**")
                band = await bot.get_channel(int(automute)).send("**تم الحظر**")
                time.sleep(5)
                await em.delete()
                await band.delete()
                embed = discord.Embed(title =f" تم حظر {mn} ", color=discord.Color.blue())
                embed.add_field(name="السبب",value="**كلمات مسيئه[سب]**")
                embed.add_field(name="الكلمه",value=f"**||{word}||**",inline=False)
                embed.add_field(name="العضو",value=mn.mention,inline=False)
                embed.add_field(name="الاداري المسؤل",value="<@1005186078480814210>")
                await bot.get_channel(int(banhistorychannel)).send(embed=embed)
            if intr.custom_id == "keep":
                await em.delete()
                embed = discord.Embed(title =f" تم اسكات {mn} ", color=discord.Color.blue())
                embed.add_field(name="السبب",value="**كلمات مسيئه[سب]**")
                embed.add_field(name="الكلمه",value=f"**||{word}||**",inline=False)
                embed.add_field(name="العضو",value=mn.mention,inline=False)
                embed.add_field(name="الاداري المسؤل",value="<@1005186078480814210>")
                await bot.get_channel(int(automutehistorychannel)).send(embed=embed)
            if intr.custom_id == "un":
                name = message.author.name
                g = message.guild
                R =discord.utils.get(g.roles , name=f"{name} muted")
                await R.delete()
                unband = await bot.get_channel(int(automute)).send("**تم فك الاسكات**")
                time.sleep(5)
                await em.delete()
                await unband.delete()
                embed = discord.Embed(title =f" تم فك الاسكات عن {mn} ", color=discord.Color.blue())
                embed.add_field(name="السبب",value="**غير معروف**")
                embed.add_field(name="العضو",value=mn.mention,inline=False)
                embed.add_field(name="الاداري المسؤل",value="<@1005186078480814210>",inline=False)
                await bot.get_channel(int(unmutehistorychannel)).send(embed=embed)
                

@bot.command()
@commands.has_role('admin')
async def unmute(ctx , member : discord.Member,*,reason):
    name = member.name
    g = ctx.guild
    R =discord.utils.get(g.roles , name=f"{name} muted")
    if R is not None:
        await R.delete()
        await ctx.reply("**تم فك الاسكات**")
        embed = discord.Embed(title =f" تم فك الاسكات عن {member.name} ", color=discord.Color.blue())
        embed.add_field(name="السبب",value=reason)
        embed.add_field(name="العضو",value=member.mention,inline=False)
        embed.add_field(name="الاداري المسؤل",value=ctx.author.mention,inline=False)
        await bot.get_channel(int(unmutehistorychannel)).send(embed=embed)
        await member.send("**لقد تم فك الاسكات عنك**")
    if R == None:
        await ctx.reply("**العضو لم ياخذ ميوت لكي تستطيع فكه**")
    
    
@bot.command()
@commands.has_role('admin')
async def mute(ctx , member : discord.Member,*,reason):
    name = member.name
    g = ctx.guild
    R =discord.utils.get(g.roles , name=f"{name} muted")
    if R is not None:
        await ctx.reply("**هذا العضو سبق وان اخذ ميوت لا تستطيع ان تسكته مرتين**")
    g = ctx.guild
    if R == None:
        r = await g.create_role(name=f"{member.name} muted")
        await member.add_roles(r)
        for channel in g.channels:
            await channel.set_permissions(target=r, speak=False , send_messages=False)
        await ctx.reply(f" تم اسكات {member.mention}")
        embed = discord.Embed(title =f" تم  اسكات  {member.name} ", color=discord.Color.blue())
        embed.add_field(name="السبب",value=reason)
        embed.add_field(name="العضو",value=member.mention,inline=False)
        embed.add_field(name="الاداري المسؤل",value=ctx.author.mention,inline=False)
        await bot.get_channel(int(mutehistorychannel)).send(embed=embed)
        await member.send("**لقد تم اسكاتك**")

@bot.command()
@commands.has_role('admin')
async def ban(ctx , member : discord.Member,*,reason):
    name = member.name
    g = ctx.guild
    R =discord.utils.get(g.roles , name=f"{name} muted")
    await R.delete()
    embed = discord.Embed(title =f" تم حظر {member.name} ", color=discord.Color.blue())
    embed.add_field(name="السبب",value=reason)
    embed.add_field(name="العضو",value=member.mention,inline=False)
    embed.add_field(name="الاداري المسؤل",value=ctx.author.mention,inline=False)
    await bot.get_channel(int(banhistorychannel)).send(embed=embed)
    await member.send("**لقد تم حظرك من السيرفر**")
    time.sleep(1)
    await member.ban(reason=reason)

@bot.command()
async def help_me(ctx):
    embed = discord.Embed(title =f"الاوامر", color=discord.Color.blue(),description="+=مسافه")
    embed.add_field(name="!ban",value="هذا الامر يطرد العضو من السيرفر :\n!ban+السبب+منشن العضو")
    embed.add_field(name="!mute",value="هذا الامر يسكت العضو  :\n!mute+السبب+منشن العضو",inline=False)
    embed.add_field(name="!unmute",value="هذا الامر يفك الاسكات من العضو  :\n!unmute+السبب+منشن العضو",inline=False)
    await ctx.send(embed=embed)

@bot.listen()
async def on_command_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("**هنالك شى ما نقص في الكود**")
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply("**هذا الامر غير متوفر**")
    if isinstance(error, commands.MissingRole):
        await ctx.reply("**ليس لديك الصلاحيه**")
    if isinstance(error, commands.MemberNotFound):
        await ctx.reply("**هذا العضو غير موجود**")

@bot.command()
@commands.has_role('admin')
async def send(ctx,chan,*,message):
    await bot.get_channel(int(chan)).send(message)


bot.run("MTAwNTE4NjA3ODQ4MDgxNDIxMA.GZQlq-.TSORf4HVgzKW8879JTx3dwlg0eKdddSxuUcOYo")
