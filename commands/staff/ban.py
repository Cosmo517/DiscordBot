import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from common.database.decorator import database_connect

@database_connect
@has_permissions(ban_members=True)
async def ban(ctx: discord.Interaction, member: discord.Member, reason: str):
    try:    
        await member.ban(reason=reason)
        await ctx.response.send_message(f"{member.mention} has been banned for {reason}")
    except discord.Forbidden:
        await ctx.response.send_message("You don't have permission to ban members.")

# Adds the command to the slash command list
async def setup(bot: commands.Bot):
    async def wrapper(ctx: discord.Interaction, member: discord.Member, reason: str):
        await ban(ctx, member, reason)

    command = discord.app_commands.Command(
        name="ban",
        description="Ban a member from the discord server",
        callback=wrapper
    )
    bot.tree.add_command(command)