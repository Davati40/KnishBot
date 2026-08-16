import os
import logging
import discord
from discord import app_commands
from discord.ext import commands, tasks
from mcstatus import BedrockServer, JavaServer

logger = logging.getLogger("discord_bot")

DEFAULT_MC_SERVER = os.getenv("DEFAULT_MC_SERVER", "localhost")

class MinecraftCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Track channel IDs in memory (Optional: persistent DB/JSON storage can be added)
        self.status_channel_id: int | None = None
        self.update_status_task.start()

    def cog_unload(self):
        self.update_status_task.cancel()

    # --- SETUP COMMAND ---
    @app_commands.command(
        name="mcsetup",
        description="Creates a locked voice channel that displays live MC server status"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def mcsetup(self, interaction: discord.Interaction):
        await interaction.response.defer()

        guild = interaction.guild
        if not guild:
            await interaction.followup.send("This command can only be used in a server.")
            return

        # 1. Lock down connect permissions for @everyone
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                connect=False, # Nobody can join
                view_channel=True # Everyone can see
            ),
            guild.me: discord.PermissionOverwrite(
                connect=True,
                manage_channels=True,
                view_channel=True
            )
        }

        # 2. Create Category and Locked Voice Channel
        category = await guild.create_category("Minecraft Status")
        channel = await guild.create_voice_channel(
            name="MC: Fetching...",
            category=category,
            overwrites=overwrites
        )

        self.status_channel_id = channel.id
        await interaction.followup.send(
            f"✅ Created status channel {channel.mention}! Status will update every 5 minutes."
        )
        
        # Trigger an immediate check
        await self.update_channel_status()

    # --- PING & UPDATE LOGIC ---
    async def fetch_server_status(self, address: str = DEFAULT_MC_SERVER, bedrock: bool = False):
        try:
            if bedrock:
                server = await BedrockServer.async_lookup(address)
                status = await server.async_status()
            else:
                server = await JavaServer.async_lookup(address)
                status = await server.async_status()
            
            return f"MC: 🟢 {status.players.online}/{status.players.max} Online"
        except Exception:
            return "MC: 🔴 Server Offline"

    async def update_channel_status(self):
        if not self.status_channel_id:
            return

        channel = self.bot.get_channel(self.status_channel_id)
        if not channel or not isinstance(channel, discord.VoiceChannel):
            return

        new_name = await self.fetch_server_status()

        # Only update if the channel name actually changed to prevent API fatigue
        if channel.name != new_name:
            try:
                await channel.edit(name=new_name)
                logger.info(f"Updated MC status channel to: {new_name}")
            except discord.HTTPException as e:
                logger.error(f"Failed to edit status channel: {e}")

    # --- BACKGROUND LOOP (Runs every 5 minutes) ---
    @tasks.loop(minutes=5)
    async def update_status_task(self):
        await self.update_channel_status()

    @update_status_task.before_loop
    async def before_status_task(self):
        await self.bot.wait_until_ready()

    # --- MANUAL CHECK COMMAND ---
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
    await bot.add_cog(MinecraftCog(bot))
