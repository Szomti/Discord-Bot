from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from constants import *
from channel import Channel
from logger import log
from data import MessagesCheckpoint

load_dotenv()
checkpoint = MessagesCheckpoint()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)
        
@bot.command(name='debug', description='debug stuff etc.')
@commands.has_role(RoleId.admin)
async def debug(ctx: discord.ApplicationContext, channel_id: int | None):
    if not isinstance(channel_id, int):
        await ctx.send('Missing channel ID')
        return
    channel = bot.get_channel(channel_id)
    if channel is None:
        await ctx.send('Incorrect channel ID')
    else:
        await ctx.send(f'Last message in {channel.mention}: {channel.last_message_id}')

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
    guild = bot.get_guild(GUILD_ID)
    log('Checking for new data')
    checkpoint.get_data()
    await check_new_data_by_channel(guild, ChannelId.neu)
    await check_new_data_by_channel(guild, ChannelId.skytils)
    await check_new_data_by_channel(guild, ChannelId.skyhanni)
    await check_new_data_by_channel(guild, ChannelId.bazaar_notifier)
    await check_new_data_by_channel(guild, ChannelId.skyblock_addons)
    log('Finished checking')
    log('Saving checkpoint')
    checkpoint.save_data()
    log('Finished saving')
    log(f">> Bot is Ready <<")

@bot.listen()
async def on_message(message: discord.Message):
    if message.author != bot.user:
        guild = message.guild
        channel = message.channel
        if(guild.id != GUILD_ID):
            return await channel.send("Guild ID not correct")
        if await ping_by_channel(guild, channel):
            checkpoint.save_data()
        
async def ping_by_channel(guild: discord.Guild, channel: discord.TextChannel) -> bool:
    role = guild.get_role(Channel(channel.id).get_role_id())
    if role == None: return False
    all_role = guild.get_role(RoleId.all)
    await channel.send("Update: "+all_role.mention+" "+role.mention)
    return True

async def check_new_data_by_channel(guild: discord.Guild, channel_id: int):
    temp_channel = bot.get_channel(channel_id)
    temp_message_id = temp_channel.last_message_id
    log(f'Checking [{checkpoint.get_data_by_channel(channel_id)} < ? > {temp_message_id}]')
    if checkpoint.get_data_by_channel(channel_id) != temp_message_id:
        log(f'New data in channel: {temp_channel.name} - {channel_id}')
        await ping_by_channel(guild, temp_channel)
        checkpoint.set_data_by_channel(channel_id, temp_channel.last_message_id)
        
bot.run(os.getenv("TOKEN"))