import os
import discord
from discord import app_commands
from discord.ext import commands
from mcstatus import BedrockServer, JavaServer

DEFAULT_MC_SERVER = os.getenv("DEFAULT_MC_SERVER", "localhost")

class MinecraftCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="mcstatus",
        description="Check the status of a Minecraft server"
    )
    @app_commands.describe(
        address="The IP/domain of the server (Leave blank for default server)",
        bedrock="Set to True if this is a Bedrock/MCPE server (default: False)"
    )
    async def mcstatus(
        self, 
        interaction: discord.Interaction, 
        address: str = DEFAULT_MC_SERVER, 
        bedrock: bool = False
    ):
        await interaction.response.defer()

        try:
            if bedrock:
                server = await BedrockServer.async_lookup(address)
                status = await server.async_status()
            else:
                server = await JavaServer.async_lookup(address)
                status = await server.async_status()

            embed = discord.Embed(
                title=f"Minecraft Server Status: {address}",
                color=discord.Color.green()
            )
            embed.add_field(name="Status", value="🟢 Online", inline=True)
            embed.add_field(name="Version", value=str(status.version.name), inline=True)
            embed.add_field(name="Players", value=f"{status.players.online}/{status.players.max}", inline=True)
            embed.add_field(name="Latency", value=f"{round(status.latency)} ms", inline=True)

            if hasattr(status, "motd") and status.motd:
                motd_text = status.motd.to_plain() if hasattr(status.motd, "to_plain") else str(status.motd)
                embed.description = f"```\n{motd_text.strip()}\n```"

            await interaction.followup.send(embed=embed)

        except Exception:
            embed = discord.Embed(
                title=f"Minecraft Server Status: {address}",
                description="Failed to ping server. The server might be offline or the address is incorrect.",
                color=discord.Color.red()
            )
            embed.add_field(name="Status", value="🔴 Offline / Unreachable", inline=False)
            await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    cog = MinecraftCog(bot)
    await bot.add_cog(cog)
    # Explicitly add the command to the bot's slash command tree
    bot.tree.add_command(cog.mcstatus)
