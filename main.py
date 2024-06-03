from dotenv import load_dotenv
from datetime import datetime, timezone
import os
import discord
from discord.ext import commands
from constants import *
from channel import Channel
from logger import log
from checkpoint import *

load_dotenv()
updates_checkpoint = UpdatesCheckpoint()
roles_checkpoint = RolesCheckpoint()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='?', intents=intents)
        
@bot.command(name='debug', description='debug stuff etc.')
@commands.has_role(Roles.admin.id)
async def debug(ctx: discord.ApplicationContext, data: int | None):
    try:
        guild = bot.get_guild(GUILD_ID)
        await ctx.send(guild.get_member(data))
    except Exception as e:
        await ctx.send(e)

@bot.command(name='clear', description='clear messages')
@commands.has_role(Roles.admin.id)
async def clear(ctx: discord.ApplicationContext, num: int = 1):
    await ctx.message.delete()
    await ctx.channel.purge(limit=num)

@bot.command(description='Create menu for role selection')
@commands.has_role(Roles.admin.id)
async def roles(ctx: discord.ApplicationContext):
    try:
        await ctx.message.delete()
        if roles_checkpoint.init:
            await ctx.send('App not ready - storage not initialized')
            log('roles command - storage not initialized')
            return
        if roles_checkpoint.channel_id is not None and roles_checkpoint.message_id is not None:
            channel = bot.get_channel(roles_checkpoint.channel_id)
            if channel is not None:
                await channel.get_partial_message(roles_checkpoint.message_id).delete()
        info = 'React to get role:'
        for role in Roles.full_list:
            if role.icon is not None:
                info += f'\n{role.icon} - {ctx.guild.get_role(role.id).mention}'
        sent = await ctx.send(info)
        roles_checkpoint.message_id = sent.id
        roles_checkpoint.channel_id = sent.channel.id
        roles_checkpoint.save_data()
        for role in Roles.full_list:
            if role.icon is not None:
                await sent.add_reaction(role.icon)
    except Exception as e:
        await ctx.send(e)

@bot.slash_command(description='Register app comand usage (badge)')
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond('Thanks for check-in')
    
@bot.listen(once=True)
async def on_ready():
    guild = bot.get_guild(GUILD_ID)
    log('Checking for new data')
    roles_checkpoint.get_data()
    updates_checkpoint.get_data()
    for channel in ChannelId.full_list:
        await check_new_data_by_channel(guild, channel)
    log('Finished checking')
    log('Saving checkpoint')
    updates_checkpoint.save_data()
    log('Finished saving')
    log(f">> Bot is Ready <<")
    await guild.get_channel(ChannelId.bot_info).send(f'<t:{int(datetime.now().timestamp())}> Bot Started')

@bot.listen()
async def on_member_join(member: discord.Member):
    member.add_roles(member.guild.get_role(Roles.member.id))

@bot.listen()
async def on_message(message: discord.Message):
    if message.author != bot.user:
        guild = message.guild
        channel = message.channel
        if(guild.id != GUILD_ID):
            return await channel.send("Guild ID not correct")
        if await ping_by_channel(guild, channel):
            updates_checkpoint.save_data()

@bot.listen()
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if payload.channel_id != roles_checkpoint.channel_id or payload.user_id == bot.application_id:
        return
    for role in Roles.full_list:
        if str(payload.emoji) == role.icon:
            guild = bot.get_guild(GUILD_ID)
            await guild.get_member(payload.user_id).add_roles(guild.get_role(role.id))

@bot.listen()
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    if payload.channel_id != roles_checkpoint.channel_id or payload.user_id == bot.application_id:
        return
    for role in Roles.full_list:
        if str(payload.emoji) == role.icon:
            guild = bot.get_guild(GUILD_ID)
            await guild.get_member(payload.user_id).remove_roles(guild.get_role(role.id))
        
async def ping_by_channel(guild: discord.Guild, channel: discord.TextChannel) -> bool:
    role = guild.get_role(Channel(channel.id).get_role_id())
    if role == None: return False
    all_role = guild.get_role(Roles.all)
    await channel.send("Update: "+all_role.mention+" "+role.mention)
    return True

async def check_new_data_by_channel(guild: discord.Guild, channel_id: int):
    temp_channel = bot.get_channel(channel_id)
    temp_message_id = temp_channel.last_message_id
    log(f'Checking [{updates_checkpoint.get_data_by_channel(channel_id)} < ? > {temp_message_id}]')
    if updates_checkpoint.get_data_by_channel(channel_id) != temp_message_id:
        log(f'New data in channel: {temp_channel.name} - {channel_id}')
        await ping_by_channel(guild, temp_channel)
        updates_checkpoint.set_data_by_channel(channel_id, temp_channel.last_message_id)
        
bot.run(os.getenv("TOKEN"))