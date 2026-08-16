import discord
from discord import app_commands
from discord.ext import commands
from mcstatus import BedrockServer, JavaServer

class MinecraftCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        bot = bot

    @app_commands.command(
        name="mcstatus",
        description="Check the online status and player count of a Minecraft server"
    )
    @app_commands.describe(
        address="The IP address or domain of the server (e.g. play.hypixel.net)",
        bedrock="Set to True if this is a Bedrock/MCPE server (default: False)"
    )
    async def mcstatus(self, interaction: discord.Interaction, address: str, bedrock: bool = False):
        # Defer response since querying a server over network can take a second
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
                # Clean up MOTD formatting if present
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
    await bot.add_cog(MinecraftCog(bot))
