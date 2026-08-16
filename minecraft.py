import os
import json
import logging
import discord
from discord import app_commands
from discord.ext import commands, tasks
from mcstatus import BedrockServer, JavaServer

logger = logging.getLogger("discord_bot")

DEFAULT_MC_SERVER = os.getenv("DEFAULT_MC_SERVER", "localhost")
DATA_FILE = "servers.json"

class MinecraftCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Structure: { channel_id_str: {"address": "play.hypixel.net", "bedrock": False, "category_id": 123456} }
        self.monitored_servers = self.load_servers()
        self.update_status_task.start()

    def cog_unload(self):
        self.update_status_task.cancel()

    # --- PERSISTENCE LOGIC ---
    def load_servers(self) -> dict:
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load {DATA_FILE}: {e}")
        return {}

    def save_servers(self):
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(self.monitored_servers, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save {DATA_FILE}: {e}")

    # --- SETUP COMMAND ---
    @app_commands.command(
        name="mcsetup",
        description="Create a category and status channel for a Minecraft server"
    )
    @app_commands.describe(
        address="The IP/domain of the server (e.g., play.hypixel.net)",
        bedrock="Set to True if this is a Bedrock server (default: False)"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def mcsetup(self, interaction: discord.Interaction, address: str = DEFAULT_MC_SERVER, bedrock: bool = False):
        await interaction.response.defer()

        guild = interaction.guild
        if not guild:
            await interaction.followup.send("This command can only be used in a server.")
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                connect=False,    # Nobody can join
                view_channel=True # Everyone can see
            ),
            guild.me: discord.PermissionOverwrite(
                connect=True,
                manage_channels=True,
                view_channel=True
            )
        }

        # 1. Create Category titled with the IP
        category_name = f"IP: {address}"
        category = await guild.create_category(name=category_name)

        # 2. Create Locked Voice Channel under the category
        channel = await guild.create_voice_channel(
            name="MC: Fetching...",
            category=category,
            overwrites=overwrites
        )

        # 3. Store server configuration
        self.monitored_servers[str(channel.id)] = {
            "address": address,
            "bedrock": bedrock,
            "category_id": category.id
        }
        self.save_servers()

        await interaction.followup.send(
            f"✅ Created category **{category_name}** and channel {channel.mention}! Status will update every 5 minutes."
        )

        # Immediately update the new channel
        await self.update_single_channel(str(channel.id), address, bedrock)

    # --- REMOVE COMMAND ---
    @app_commands.command(
        name="mcremove",
        description="Stop monitoring a Minecraft server and remove its category/channel"
    )
    @app_commands.describe(address="The IP address of the server to remove")
    @app_commands.checks.has_permissions(administrator=True)
    async def mcremove(self, interaction: discord.Interaction, address: str):
        await interaction.response.defer()

        to_delete = None
        for channel_id, data in self.monitored_servers.items():
            if data["address"].lower() == address.lower():
                to_delete = channel_id
                break

        if not to_delete:
            await interaction.followup.send(f"No monitored server found with IP `{address}`.")
            return

        data = self.monitored_servers.pop(to_delete)
        self.save_servers()

        # Delete channel and category from Discord
        channel = self.bot.get_channel(int(to_delete))
        if channel:
            await channel.delete()

        category = self.bot.get_channel(data.get("category_id"))
        if category:
            await category.delete()

        await interaction.followup.send(f"🗑️ Stopped monitoring **{address}** and removed its category/channel.")

    # --- STATUS UPDATE LOGIC ---
    async def fetch_server_status(self, address: str, bedrock: bool = False) -> str:
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

    async def update_single_channel(self, channel_id_str: str, address: str, bedrock: bool):
        channel = self.bot.get_channel(int(channel_id_str))
        if not channel or not isinstance(channel, discord.VoiceChannel):
            return

        new_name = await self.fetch_server_status(address, bedrock)

        if channel.name != new_name:
            try:
                await channel.edit(name=new_name)
                logger.info(f"Updated status for [{address}] in channel {channel.id} -> {new_name}")
            except discord.HTTPException as e:
                logger.error(f"Failed to edit status channel for {address}: {e}")

    # --- BACKGROUND LOOP (Every 5 Minutes) ---
    @tasks.loop(minutes=5)
    async def update_status_task(self):
        for channel_id_str, data in list(self.monitored_servers.items()):
            await self.update_single_channel(
                channel_id_str, 
                data["address"], 
                data.get("bedrock", False)
            )

    @update_status_task.before_loop
    async def before_status_task(self):
        await self.bot.wait_until_ready()

    # --- ON-DEMAND CHECK COMMAND ---
    @app_commands.command(
        name="mcstatus",
        description="Check the status of a Minecraft server on demand"
    )
    @app_commands.describe(
        address="The IP/domain of the server (Leave blank for default server)",
        bedrock="Set to True if this is a Bedrock server (default: False)"
    )
    async def mcstatus(self, interaction: discord.Interaction, address: str = DEFAULT_MC_SERVER, bedrock: bool = False):
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
