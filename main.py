from dotenv import load_dotenv
from datetime import datetime
import os
import discord
from discord.ext import commands
from constants import *
from channel import Channel
from logger import log
from checkpoint import *
import asyncio

load_dotenv()
updates_checkpoint = UpdatesCheckpoint()
roles_checkpoint = RolesCheckpoint()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

app_running = True

bot = commands.Bot(command_prefix='?', intents=intents)
        
@bot.command(name='debug', description='debug stuff etc.')
@commands.has_role(Roles.admin.id)
async def debug(ctx: discord.ApplicationContext, data: int | None):
    description = 'It\'s basically server for me to have every mod update in one place and get notified about it.\n'
    description += '\nJust a heads-up, the bot is running on my pc, so it won\'t be always online'
    description += '\n*(when it comes back online, it will ping the respective role if there were updates in the meantime)*'
    embed = discord.Embed(
        title = 'Welcome to Skyblock Mods server!',
        description = description,
        color = discord.Colour.blue(),
    )
    await ctx.send(embed=embed)

@bot.command(name='welcome_info', description='Create embed with basic server info')
@commands.has_role(Roles.admin.id)
async def welcome_info(ctx: discord.ApplicationContext, data: int | None):
    description = 'It\'s basically server for me to have every hypixel skyblock mod update in one place and get notified about it.\n'
    description += '\nJust a heads-up, the bot is running on my pc, so it won\'t be always online'
    description += '\n*(when it comes back online, it will ping the respective role if there were updates in the meantime)*'
    embed = discord.Embed(
        title = 'Welcome to Skyblock Mods server!',
        description = description,
        color = discord.Colour.blue(),
    )
    embed.add_field(name='Rules', value='Don\'t break [discord\'s ToS](https://discord.com/terms/)')
    await ctx.send(embed=embed)

@bot.command(name='clear', description='clear messages')
@commands.has_role(Roles.admin.id)
async def clear(ctx: discord.ApplicationContext, num: int = 1):
    await ctx.message.delete()
    await ctx.channel.purge(limit=num)

@bot.command(name='force_stop', description='force stop the app')
@commands.has_role(Roles.admin.id)
async def force_stop(ctx: discord.ApplicationContext):
    try:
        if ctx.author.id != OWNER_ID:
            log(f'user: [{ctx.author.id}] tried to force stop the app')
            return
        global app_running
        app_running = False
        log('App force stopped')
        await ctx.message.delete()
        await bot.close()
        exit(1)
    except Exception as e:
        log(e)

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
                try:
                    await channel.get_partial_message(roles_checkpoint.message_id).delete()
                except:
                    pass
        description='React to get role!'
        embed = discord.Embed(
            title = 'Want to be notified about mod updates?',
            description = description,
            color = discord.Colour.blue(),
        )
        info =''
        for role in Roles.full_list:
            if role.icon is not None:
                info += f'\n{role.icon} - {ctx.guild.get_role(role.id).mention}'
        embed.add_field(name='Available roles:', value=info)
        sent = await ctx.send(embed=embed)
        roles_checkpoint.message_id = sent.id
        roles_checkpoint.channel_id = sent.channel.id
        roles_checkpoint.save_data()
        for role in Roles.full_list:
            if role.icon is not None:
                await sent.add_reaction(role.icon)
    except Exception as e:
        log(e)
        await ctx.send(e)

@bot.slash_command(description='Register app comand usage (badge)')
async def hello(ctx: discord.ApplicationContext):
    embed = discord.Embed(
        title='Hello fellow member!',
        description='Thanks for checking in and for using this command. Usage of this command allows me to have developer badge!',
        color=discord.Colour.blue(),
    )
    await ctx.respond(embed=embed)
    
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
    await moderate_on_ready()
    log(f'>> Bot is Ready <<')
    date = datetime.now()
    await guild.get_channel(ChannelId.bot_info).send(f'<t:{int(date.timestamp())}:d><t:{int(date.timestamp())}:T> Bot Started')
    try:
        task = asyncio.create_task(log_uptime())
        asyncio.gather(task, return_exceptions=True)
    except Exception as e:
        if e is not KeyboardInterrupt:
            log(e)
        

@bot.listen()
async def on_member_join(member: discord.Member):
    await member.add_roles(member.guild.get_role(Roles.member.id))

@bot.listen()
async def on_message(message: discord.Message):
    if message.author != bot.user:
        guild = message.guild
        channel = message.channel
        if(guild.id != GUILD_ID):
            return await channel.send('Guild ID not correct')
        if channel.id == ChannelId.hello:
            await message.delete()
            return
        if await ping_by_channel(guild, channel):
            updates_checkpoint.save_data()

async def moderate_on_ready():
    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(ChannelId.hello)
    async for message in channel.history(limit=200):
        if message.author != bot.user:
            await message.delete()

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
    all_role = guild.get_role(Roles.all.id)
    await channel.send('Update: '+all_role.mention+' '+role.mention)
    return True

async def check_new_data_by_channel(guild: discord.Guild, channel_id: int):
    temp_channel = bot.get_channel(channel_id)
    temp_message_id = temp_channel.last_message_id
    log(f'Checking [{updates_checkpoint.get_data_by_channel(channel_id)} < ? > {temp_message_id}]')
    if updates_checkpoint.get_data_by_channel(channel_id) != temp_message_id:
        log(f'New data in channel: {temp_channel.name} - {channel_id}')
        await ping_by_channel(guild, temp_channel)
        updates_checkpoint.set_data_by_channel(channel_id, temp_channel.last_message_id)

async def log_uptime():
    message = None
    start = datetime.now()
    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(ChannelId.bot_info)
    global app_running
    while(True):
        await asyncio.sleep(10)
        if not app_running:
            message = None
            break
        now = datetime.now()
        diff = now - start
        total_seconds = int(diff.total_seconds())
        hours, remaining = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remaining, 60)
        text = f'Bot alive for: {'{} hrs {} mins {} secs'.format(hours,minutes,seconds)}'
        if message is None:
            message = await channel.send(text)
        else:
            await message.edit(text)
        
bot.run(os.getenv('TOKEN'))