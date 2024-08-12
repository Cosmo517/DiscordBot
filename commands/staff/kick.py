import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

@has_permissions(kick_members=True)
async def kick(ctx: discord.Interaction, member: discord.Member, reason: str):
    try:    
        await member.kick(reason=reason)
        await ctx.response.send_message(f"{member.mention} has been kicked for {reason}")
    except discord.Forbidden:
        await ctx.response.send_message("You don't have permission to kick members.")

# Adds the command to the slash command list
async def setup(bot: commands.Bot):
    async def wrapper(ctx: discord.Interaction, member: discord.Member, reason: str):
        await kick(ctx, member, reason)

    command = discord.app_commands.Command(
        name="kick",
        description="Kick a member from the discord server",
        callback=wrapper
    )
    bot.tree.add_command(command)