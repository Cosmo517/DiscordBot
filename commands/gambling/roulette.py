# /commands/basic/help.py
import discord
from discord.ext import commands
from typing import Literal
import random as rand
from common.database.database import SessionLocal
from common.database.models import Users, ServerToUsers


# Define the slash command
async def roulette_command(interaction: discord.Interaction, amount: int, color: Literal["🔴Red", "⚫Black"]):
    discord_id = str(interaction.user.id)
    server_id = str(interaction.guild.id)

    # Open a new session to interact with the database
    session = SessionLocal()

    try:
        # Ensure the user exists in the 'users' table
        user = session.query(Users).filter_by(discord_id=discord_id).first()

        if not user:
            new_user = Users(discord_id=discord_id)
            session.add(new_user)
            session.commit()  # Commit to ensure the user is added before proceeding

        # Now check if the user is already in the servertousers table
        user_entry = session.query(ServerToUsers).filter_by(discord_id=discord_id, server_id=server_id).first()

        if not user_entry:
            user_entry = ServerToUsers(discord_id=discord_id, server_id=server_id, money=500)
            session.add(user_entry)
            session.commit()

        current_balance = user_entry.money
        if amount > current_balance:
            await interaction.response.send_message(f"Insufficient funds! Your current balance is ${current_balance}.", ephemeral=True)
            return

        # Roulette logic
        red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        black_numbers = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
        green_numbers = {0, 37}
        rand_num = rand.randint(0, 37)
        color_val = discord.Color.blurple()
        color_name = "default"

        # Determine the result color
        if rand_num in green_numbers:
            color_val = discord.Color.green()
            color_name = "🍏Green"
        elif rand_num in red_numbers:
            color_val = discord.Color.red()
            color_name = "🔴Red"
        else:
            color_val = discord.Color.dark_grey()
            color_name = "⚫Black"

        # Determine win or loss
        if color == color_name:
            winnings = amount
            user_entry.money += winnings
        else:
            losses = amount
            user_entry.money -= losses

        # Commit the updated balance to the database
        session.commit()

        # Prepare the embed message
        embed = discord.Embed(
            title="🛞Roulette Game",
            description=f"Amount Bet: ${amount} on {color}",
            color=color_val
        )
        embed.add_field(name="RESULTS:", value=f"{rand_num} {color_name}", inline=False)

        if color == color_name:
            embed.add_field(name="WINNINGS:", value=f"${amount}")
        else:
            embed.add_field(name="LOSSES:", value=f"${amount}")

        embed.set_footer(text="One gamble away from winning!")

        # Send the embedded message
        await interaction.response.send_message(embed=embed)

    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)
    finally:
        session.close()


# Adds the command to the slash command list
async def setup(bot: commands.Bot):
    command = discord.app_commands.Command(
        name="roulette",
        description="ALL ON BLACK",
        callback=roulette_command
    )
    bot.tree.add_command(command)