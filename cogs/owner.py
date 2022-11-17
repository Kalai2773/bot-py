import json

import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands
from helpers import checks
from helpers import db_manager


class Owner(commands.Cog, name="owner"):
    def __init__(self, bot):
        self.bot = bot
      
    @commands.command(
        name="sync",
        description="Synchronizes the slash commands.",
    )
    @app_commands.describe(scope="The scope of the sync. Can be `global` or `guild`")
    @checks.is_owner()
    async def sync(self, context: Context, scope: str) -> None:
        """
        Synchonizes the slash commands.
        :param context: The command context.
        :param scope: The scope of the sync. Can be `global` or `guild`.
        """

        if scope == "global":
            await context.bot.tree.sync()
            embed = discord.Embed(
                title="Slash Commands Sync",
                description="Slash commands have been globally synchronized.",
                color=0x9C84EF
            )
            await context.send(embed=embed)
            return
        elif scope == "guild":
            context.bot.tree.copy_global_to(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                title="Slash Commands Sync",
                description="Slash commands have been synchronized in this guild.",
                color=0x9C84EF
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            title="Invalid Scope",
            description="The scope must be `global` or `guild`.",
            color=0xE02B2B
        )
        await context.send(embed=embed)

    @commands.command(
        name="unsync",
        description="Unsynchonizes the slash commands.",
    )
    @app_commands.describe(scope="The scope of the sync. Can be `global`, `current_guild` or `guild`")
    @checks.is_owner()
    async def unsync(self, context: Context, scope: str) -> None:
        """
        Unsynchonizes the slash commands.
        :param context: The command context.
        :param scope: The scope of the sync. Can be `global`, `current_guild` or `guild`.
        """

        if scope == "global":
            context.bot.tree.clear_commands(guild=None)
            await context.bot.tree.sync()
            embed = discord.Embed(
                title="Slash Commands Unsync",
                description="Slash commands have been globally unsynchronized.",
                color=0x9C84EF
            )
            await context.send(embed=embed)
            return
        elif scope == "guild":
            context.bot.tree.clear_commands(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                title="Slash Commands Unsync",
                description="Slash commands have been unsynchronized in this guild.",
                color=0x9C84EF
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            title="Invalid Scope",
            description="The scope must be `global` or `guild`.",
            color=0xE02B2B
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="load",
        description="Load a cog",
    )
    @app_commands.describe(cog="The name of the cog to load")
    @checks.is_owner()
    async def load(self, context: Context, cog: str) -> None:
        """
        The bot will load the given cog.
        :param context: The hybrid command context.
        :param cog: The name of the cog to load.
        """
        try:
            await self.bot.load_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                title="Error!",
                description=f"Could not load the `{cog}` cog.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            title="Load",
            description=f"Successfully loaded the `{cog}` cog.",
            color=0x9C84EF
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="unload",
        description="Unloads a cog.",
    )
    @app_commands.describe(cog="The name of the cog to unload")
    @checks.is_owner()
    async def unload(self, context: Context, cog: str) -> None:
        """
        The bot will unload the given cog.
        :param context: The hybrid command context.
        :param cog: The name of the cog to unload.
        """
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                title="Error!",
                description=f"Could not unload the `{cog}` cog.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            title="Unload",
            description=f"Successfully unloaded the `{cog}` cog.",
            color=0x9C84EF
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="reload",
        description="Reloads a cog.",
    )
    @app_commands.describe(cog="The name of the cog to reload")
    @checks.is_owner()
    async def reload(self, context: Context, cog: str) -> None:
        """
        The bot will reload the given cog.
        :param context: The hybrid command context.
        :param cog: The name of the cog to reload.
        """
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                title="Error!",
                description=f"Could not reload the `{cog}` cog.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            title="Reload",
            description=f"Successfully reloaded the `{cog}` cog.",
            color=0x9C84EF
        )
        await context.send(embed=embed)
      
    @commands.hybrid_command(
        name="shutdown",
        description="Make the bot shutdown.",
    )
    @checks.is_owner()
    async def shutdown(self, context: Context) -> None:
        """
        Shuts down the bot.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description="Shutting down. Bye! :wave:",
            color=0xDA004E
        )
        await context.send(embed=embed)
        await self.bot.close()

    @commands.hybrid_command(
        name="say",
        description="The bot will say anything you want.",
    )
    @commands.has_permissions(manage_messages=True)
    async def say(self, context: Context, *,message:str) -> None:
        await context.send(message,allowed_mentions = discord.AllowedMentions(everyone = False,roles=False))

    @commands.hybrid_command(
        name="embed",
        description="The bot will say anything you want, but within embeds.",
    )
    @commands.has_permissions(manage_messages=True)
    async def embed(self, context: Context, * ,message: str) -> None:
        embed = discord.Embed(
            description=message,
            color=0xDA004E
        )
        await context.send(embed=embed)
      
    @commands.hybrid_group(
        name="blacklist",
        description="Get the list of all blacklisted users.",
    )
    @checks.is_owner()
    async def blacklist(self, context: Context) -> None:

        pass

    @blacklist.command(
        base="blacklist",
        name="add",
        description="Lets you add a user from not being able to use the bot.",
    )
    @checks.is_owner()
    async def blacklist_add(self, context: Context, user: discord.User) -> None:
        """
        Lets you add a user from not being able to use the bot.

        :param context: The hybrid command context.
        :param user: The user that should be added to the blacklist.
        """
        user_id = user.id
        if db_manager.is_blacklisted(user_id):
            embed = discord.Embed(
                title="Error!",
                description=f"**{user.name}** is not in the blacklist.",
                color=0xE02B2B
            )
            return await context.send(embed=embed)
        total = db_manager.add_user_to_blacklist(user_id)
        embed = discord.Embed(
            title="User Blacklisted",
            description=f"**{user.name}** has been successfully added to the blacklist",
            color=0xDA004E
        )
        embed.set_footer(
            text=f"There are now {total} {'user' if total == 1 else 'users'} in the blacklist"
        )
        await context.send(embed=embed)

    @blacklist.command(
        base="blacklist",
        name="remove",
        description="Lets you remove a user from not being able to use the bot.",
    )
    
    @checks.is_owner()
    async def blacklist_remove(self, context: Context, user: discord.User):
        """
        Lets you remove a user from not being able to use the bot.

        :param context: The hybrid command context.
        :param user: The user that should be removed from the blacklist.
        """
        user_id = user.id
        if not db_manager.is_blacklisted(user_id):
            embed = discord.Embed(
                title="Error!",
                description=f"**{user.name}** is already in the blacklist.",
                color=0xE02B2B
            )
            return await context.send(embed=embed)
        total = db_manager.remove_user_from_blacklist(user_id)
        embed = discord.Embed(
            title="User removed from blacklist",
            description=f"**{user.name}** has been successfully removed from the blacklist",
            color=0xDA004E
        )
        embed.set_footer(
            text=f"There are now {total} {'user' if total == 1 else 'users'} in the blacklist"
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="listserver",
        description="Get all the server name of bot.",
    )
    @checks.is_owner()
    async def list_guilds(self, context:Context):       
      kk=[f"{guild.name} - {guild.owner}"for guild in self.bot.guilds]
      jk="\n".join(kk)
        
      await context.send(f"**```{jk}```**")
           

    @commands.command(
      name="leaveserver",
                             description="A developer only command that makes the bot leave the given server when a Guild ID is provided."
    )
    @checks.is_owner()
    async def leave(self,context:Context,id:str):
        guild = await self.bot.fetch_guild(int(id))
        await guild.leave()
        await context.send(f"left - {guild.name} ")

async def setup(bot):
    await bot.add_cog(Owner(bot))