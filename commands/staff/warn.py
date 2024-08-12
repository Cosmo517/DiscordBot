import discord
from discord.ext import commands
from commands.common.staff_functions import addUserWarn, returnUserWarnings
from common.database.datatypes import WarnsBase
from common.database.decorator import database_connect

# TODO: Add role checks to make sure user can warn people
@database_connect
async def warn(ctx: discord.Interaction, member: discord.Member, reason: str, session=None):
    warning = addUserWarn(WarnsBase(server_id=str(ctx.guild_id), discord_id=str(member.id), reason=reason), session=session)
    total_warns = len(returnUserWarnings(WarnsBase(server_id=str(ctx.guild_id), discord_id=str(member.id), reason=reason), session=session))
    if warning:
        embed = discord.Embed(
        title="Warning",
        description=f"User Warned: {member.mention}",
        color=discord.Color.red()
        )
        embed.add_field(name="Total Warnings:", value=f"{total_warns}", inline=False)
        await ctx.response.send_message(embed=embed)
    else:
        ctx.response.send_message(f"Failed to add warning for user {member.mention}")

# Adds the command to the slash command list
async def setup(bot: commands.Bot):
    async def wrapper(ctx: discord.Interaction, member: discord.Member, reason: str):
        await warn(ctx, member, reason)

    command = discord.app_commands.Command(
        name="warn",
        description="Give a warning to a discord member",
        callback=wrapper
    )
    bot.tree.add_command(command)