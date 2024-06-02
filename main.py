from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from datetime import datetime
from constants import *
from channel import Channel

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)
        
@bot.command(name='debug', description='debug stuff etc.')
@commands.has_role(RoleId.admin)
async def debug(ctx: discord.ApplicationContext):
    await ctx.send('test')

@bot.command(name='clear', description='clear messages')
@commands.has_role(RoleId.admin)
async def clear(ctx: discord.ApplicationContext, num: int = 1):
    await ctx.message.delete()
    await ctx.channel.purge(limit=num)

@bot.command(description='Create menu for role selection')
@commands.has_role(RoleId.admin)
async def roles(ctx: discord.ApplicationContext):
    await ctx.send(f"React to get role:\n:infinity: - {ctx.guild.get_role(RoleId.all).mention}\n:one: - {ctx.guild.get_role(RoleId.neu).mention}\n:two: - {ctx.guild.get_role(RoleId.skytils).mention}\n:three: - {ctx.guild.get_role(RoleId.skyhanni).mention}\n:four: - {ctx.guild.get_role(RoleId.bazaar_notifier).mention}\n:five: - {ctx.guild.get_role(RoleId.skyblock_addons).mention}")

@bot.slash_command(description='Register app comand usage (badge)')
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond('Thanks for check-in')
    
@bot.listen(once=True)
async def on_ready():
    print(f">> Bot is Ready <<\n[{datetime.now()}]")

@bot.listen()
async def on_message(message: discord.Message):
    if message.author != bot.user:
        guild = message.guild
        if(guild.id != GUILD_ID):
            return await message.channel.send("Guild ID not correct")
        role = guild.get_role(Channel(message.channel.id).get_role_id())
        if role == None: return
        all_role = guild.get_role(RoleId.all)
        await message.channel.send("Update: "+all_role.mention+" "+role.mention)
        
bot.run(os.getenv("TOKEN"))