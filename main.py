import discord
from datetime import datetime
from constants import * 
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def role_for_channel(channel: int, guild: discord.Guild) -> discord.Role:
    match channel:
        case ChannelsIds.neu:
            return guild.get_role(RolesIds.neu)
        case ChannelsIds.skytils:
            return guild.get_role(RolesIds.skytils)
        case ChannelsIds.skyhanni:
            return guild.get_role(RolesIds.skyhanni)
        case ChannelsIds.bazaar_notifier:
            return guild.get_role(RolesIds.bazaar_notifier)
        case ChannelsIds.skyblock_addons:
            return guild.get_role(RolesIds.skyblock_addons)
        case _:
            return None
        
@bot.hybrid_command()
async def hello(ctx):
    await ctx.send('Thanks for check-in', ephemeral=True)

@bot.hybrid_command()
async def roles(ctx):
    await ctx.send(f"React to get role:\n:infinity: - {ctx.guild.get_role(RolesIds.everything).mention}\n:one: - {ctx.guild.get_role(RolesIds.neu).mention}\n:two: - {ctx.guild.get_role(RolesIds.skytils).mention}\n:three: - {ctx.guild.get_role(RolesIds.skyhanni).mention}\n:four: - {ctx.guild.get_role(RolesIds.bazaar_notifier).mention}\n:five: - {ctx.guild.get_role(RolesIds.skyblock_addons).mention}")

    
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(">> Bot is Ready <<\n[" + str(datetime.now()) + "]")

@bot.event
async def on_message(message):
    if message.author != bot.user:
        await bot.process_commands(message)
        guild = message.guild
        if(guild.id != GUILD_ID):
            return await message.channel.send("Server ID not correct")
        role = role_for_channel(message.channel.id, guild)
        if role == None: return
        everything_role = guild.get_role(RolesIds.everything)
        await message.channel.send("Update: "+everything_role.mention+" "+role.mention)
        
bot.run("MTA4Nzg1ODA1ODI2MjIzNzI2NA.GdcdgF.moytbhZP7R5ux8B3hsmLcsLZ85VRaXXp6J3FGM")