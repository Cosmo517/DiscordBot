import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from common.database.decorator import database_connect
from commands.common.staff_functions import banUser
from common.database.datatypes import BansBase

@database_connect
@has_permissions(ban_members=True)
async def ban(ctx: discord.Interaction, member: discord.Member, reason: str, session=None):
    try:
        banned = banUser(BansBase(server_id=str(ctx.guild_id), discord_id=str(member.id), reason=reason), session=session)
        if banned:
            await member.kick(reason=reason)
            embed = discord.Embed(
            title="Ban Hammer",
            description=f"User Banned: {member.mention}",
            color=discord.Color.red()
            )
            embed.add_field(name="Reason:", value=f"{reason}", inline=False)
            await ctx.response.send_message(embed=embed)
        else:
            await ctx.response.send_message(f"Couldn't ban user {member.mention}")
            
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